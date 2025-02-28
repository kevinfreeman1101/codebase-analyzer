# codebase_analyzer/formatters/comprehensive_formatter.py
from typing import List, Dict, Any, Optional
import datetime
from pathlib import Path
from dataclasses import dataclass
from ..metrics import (
    ComplexityMetrics,
    QualityMetrics,
    DependencyMetrics,
    PatternMetrics,
    SecurityMetrics,
    PerformanceMetrics
)

@dataclass
class FormattingOptions:
    """Configuration options for output formatting."""
    include_timestamps: bool = True
    detail_level: str = 'medium'  # 'low', 'medium', 'high'
    max_items_per_section: int = 5
    include_code_snippets: bool = True
    format_type: str = 'text'  # 'text', 'markdown', 'html'
    color_output: bool = True

class ComprehensiveFormatter:
    """Formats analysis results into various output formats with customizable detail levels."""

    def __init__(self, options: Optional[FormattingOptions] = None):
        self.options = options or FormattingOptions()
        self.colors = self._setup_colors()

    def _setup_colors(self) -> Dict[str, str]:
        """Setup ANSI color codes for terminal output."""
        if not self.options.color_output:
            return {k: '' for k in ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'reset']}

        return {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'reset': '\033[0m'
        }

    def format_analysis(self, metrics: Dict[str, Any]) -> str:
        """Format complete analysis results."""
        sections = []

        # Project Overview
        sections.append(self._format_project_overview(metrics))

        # Executive Summary
        sections.append(self._format_executive_summary(metrics))

        # Detailed Analysis Sections
        sections.extend([
            self._format_complexity_analysis(metrics['complexity']),
            self._format_quality_analysis(metrics['quality']),
            self._format_security_analysis(metrics['security']),
            self._format_performance_analysis(metrics['performance']),
            self._format_dependency_analysis(metrics['dependencies']),
            self._format_pattern_analysis(metrics['patterns'])
        ])

        # Recommendations
        sections.append(self._format_recommendations(metrics))

        return '\n\n'.join(sections)

    def _format_project_overview(self, metrics: Dict[str, Any]) -> str:
        """Format project overview section."""
        lines = [
            self._format_header("Project Overview", level=1),
            "",
            f"Project Path: {metrics['project_path']}",
            f"Analysis Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Files: {metrics['total_files']}",
            f"Total Lines: {metrics['total_lines']:,}",
            "",
            "Overall Health Metrics:",
            f"└── Overall Score: {self._format_score(metrics['overall_score'])}",
            f"└── Health Index: {self._format_score(metrics['health_index'])}",
            f"└── Technical Debt Ratio: {metrics['tech_debt_ratio']:.1%}"
        ]
        return '\n'.join(lines)

    def _format_executive_summary(self, metrics: Dict[str, Any]) -> str:
        """Format executive summary with key findings."""
        lines = [
            self._format_header("Executive Summary", level=1),
            "",
            "Key Metrics:",
            f"└── Code Quality: {self._format_score(metrics['quality'].quality_score)}",
            f"└── Security: {self._format_score(metrics['security'].security_score)}",
            f"└── Performance: {self._format_score(metrics['performance'].performance_score)}",
            "",
            "Critical Findings:",
        ]

        # Add critical findings
        critical_findings = self._get_critical_findings(metrics)
        if critical_findings:
            lines.extend([f"└── {finding}" for finding in critical_findings])
        else:
            lines.append("└── No critical issues found")

        return '\n'.join(lines)

    def _format_complexity_analysis(self, metrics: ComplexityMetrics) -> str:
        """Format complexity analysis section."""
        lines = [
            self._format_header("Complexity Analysis", level=2),
            "",
            f"Maintainability Index: {self._format_score(metrics.maintainability_index)}",
            f"Average Cyclomatic Complexity: {metrics.avg_complexity:.2f}",
            "",
            "Complex Components:",
        ]

        # Add complex functions
        for func in sorted(metrics.complex_functions, 
                         key=lambda x: x.complexity, 
                         reverse=True)[:self.options.max_items_per_section]:
            lines.append(
                f"└── {func.name} (complexity: {func.complexity})"
                f" at {func.location}"
            )

        return '\n'.join(lines)

    def _format_quality_analysis(self, metrics: QualityMetrics) -> str:
        """Format code quality analysis section."""
        lines = [
            self._format_header("Code Quality Analysis", level=2),
            "",
            f"Overall Quality Score: {self._format_score(metrics.quality_score)}",
            f"Documentation Coverage: {metrics.documentation_coverage:.1%}",
            f"Test Coverage: {metrics.test_coverage:.1%}",
            "",
            "Quality Issues:",
        ]

        # Add quality issues
        for issue in metrics.issues[:self.options.max_items_per_section]:
            lines.append(
                f"└── {issue.type}: {issue.description}"
                f" at {issue.location}"
            )

        return '\n'.join(lines)

    def _format_security_analysis(self, metrics: SecurityMetrics) -> str:
        """Format security analysis section."""
        lines = [
            self._format_header("Security Analysis", level=2),
            "",
            f"Security Score: {self._format_score(metrics.security_score)}",
            "",
            "Vulnerabilities:",
        ]

        # Add vulnerabilities grouped by severity
        vulnerabilities_by_severity = self._group_by_severity(metrics.vulnerabilities)
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if severity in vulnerabilities_by_severity:
                lines.append(f"\n{severity} Severity:")
                for vuln in vulnerabilities_by_severity[severity][:self.options.max_items_per_section]:
                    lines.append(
                        f"└── {vuln.type}: {vuln.description}"
                        f"\n    Location: {vuln.location}"
                        f"\n    Recommendation: {vuln.recommendation}"
                    )

        return '\n'.join(lines)

    def _format_performance_analysis(self, metrics: PerformanceMetrics) -> str:
        """Format performance analysis section."""
        lines = [
            self._format_header("Performance Analysis", level=2),
            "",
            f"Performance Score: {self._format_score(metrics.performance_score)}",
            "",
            "Performance Hotspots:",
        ]

        # Add performance hotspots
        for hotspot in metrics.hotspots[:self.options.max_items_per_section]:
            lines.append(
                f"└── {hotspot.type} ({hotspot.severity})"
                f"\n    Location: {hotspot.location}"
                f"\n    Impact: {hotspot.impact}"
                f"\n    Recommendation: {hotspot.recommendation}"
            )

        return '\n'.join(lines)

    def _format_dependency_analysis(self, metrics: DependencyMetrics) -> str:
        """Format dependency analysis section."""
        lines = [
            self._format_header("Dependency Analysis", level=2),
            "",
            f"Total Dependencies: {metrics.total_dependencies}",
            f"Direct Dependencies: {len(metrics.direct_dependencies)}",
            f"Dependency Health Score: {self._format_score(metrics.health_score)}",
            "",
            "Outdated Dependencies:",
        ]

        # Add outdated dependencies
        for dep in metrics.outdated_dependencies[:self.options.max_items_per_section]:
            lines.append(
                f"└── {dep['name']}: {dep['current']} → {dep['latest']}"
                f"\n    Security implications: {dep['security_implications']}"
            )

        return '\n'.join(lines)

    def _format_pattern_analysis(self, metrics: PatternMetrics) -> str:
        """Format code pattern analysis section."""
        lines = [
            self._format_header("Code Pattern Analysis", level=2),
            "",
            f"Architectural Style: {metrics.architectural_style.name}"
            f" ({metrics.architectural_style.confidence:.1%} confidence)",
            "",
            "Design Patterns Detected:",
        ]

        # Add detected patterns
        for pattern in metrics.design_patterns[:self.options.max_items_per_section]:
            lines.append(
                f"└── {pattern.name} ({pattern.confidence:.1%} confidence)"
                f"\n    Location: {pattern.location}"
            )

        return '\n'.join(lines)

    def _format_recommendations(self, metrics: Dict[str, Any]) -> str:
        """Format recommendations section."""
        lines = [
            self._format_header("Recommendations", level=1),
            "",
            "High Priority:",
        ]

        # Add prioritized recommendations
        recommendations = self._get_prioritized_recommendations(metrics)
        for priority in ['high', 'medium', 'low']:
            if priority in recommendations:
                lines.append(f"\n{priority.title()} Priority:")
                for rec in recommendations[priority][:self.options.max_items_per_section]:
                    lines.append(f"└── {rec}")

        return '\n'.join(lines)

    def _format_score(self, score: float) -> str:
        """Format a score with color coding."""
        if not self.options.color_output:
            return f"{score:.1f}/100"

        color = (
            self.colors['red'] if score < 50 else
            self.colors['yellow'] if score < 80 else
            self.colors['green']
        )
        return f"{color}{score:.1f}/100{self.colors['reset']}"

    def _format_header(self, text: str, level: int = 1) -> str:
        """Format section headers."""
        if self.options.format_type == 'markdown':
            return f"{'#' * level} {text}"

        if level == 1:
            return f"\n{text}\n{'=' * len(text)}"
        return f"\n{text}\n{'-' * len(text)}"

    def _get_critical_findings(self, metrics: Dict[str, Any]) -> List[str]:
        """Extract critical findings from all metrics."""
        findings = []

        # Security findings
        critical_vulns = [v for v in metrics['security'].vulnerabilities 
                         if v.severity == 'CRITICAL']
        findings.extend([f"Security: {v.description}" for v in critical_vulns])

        # Performance findings
        critical_hotspots = [h for h in metrics['performance'].hotspots 
                           if h.severity == 'HIGH']
        findings.extend([f"Performance: {h.description}" for h in critical_hotspots])

        # Quality findings
        critical_quality = [i for i in metrics['quality'].issues 
                          if i.severity == 'HIGH']
        findings.extend([f"Quality: {i.description}" for i in critical_quality])

        return findings

    def _get_prioritized_recommendations(self, metrics: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate prioritized recommendations based on all metrics."""
        recommendations = {
            'high': [],
            'medium': [],
            'low': []
        }

        # Security recommendations
        for vuln in metrics['security'].vulnerabilities:
            priority = 'high' if vuln.severity in ['CRITICAL', 'HIGH'] else 'medium'
            recommendations[priority].append(f"Security: {vuln.recommendation}")

        # Performance recommendations
        for opt in metrics['performance'].optimization_opportunities:
            priority = 'high' if opt.estimated_impact.startswith('High') else 'medium'
            recommendations[priority].append(f"Performance: {opt.suggested_pattern}")

        # Quality recommendations
        if hasattr(metrics['quality'], 'improvement_suggestions'):
            for suggestion in metrics['quality'].improvement_suggestions:
                recommendations['medium'].append(f"Quality: {suggestion}")

        return recommendations

    def _group_by_severity(self, items: List[Any]) -> Dict[str, List[Any]]:
        """Group items by severity level."""
        grouped = {}
        for item in items:
            if not hasattr(item, 'severity'):
                continue
            if item.severity not in grouped:
                grouped[item.severity] = []
            grouped[item.severity].append(item)
        return grouped