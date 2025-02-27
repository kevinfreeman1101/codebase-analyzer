# codebase_analyzer/visualizations/metric_visualizer.py
from typing import Dict, List, Any, Tuple
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pathlib import Path
import seaborn as sns
from datetime import datetime

class MetricVisualizer:
    """Generates visual representations of codebase metrics."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set style
        plt.style.use('seaborn')
        sns.set_palette("husl")

        # Track generated files
        self.generated_files: List[Path] = []

    def generate_visualizations(self, metrics: Dict[str, Any]) -> List[Path]:
        """Generate all visualizations for the metrics."""
        self.generated_files = []

        # Generate each type of visualization
        self._generate_score_dashboard(metrics)
        self._generate_complexity_heatmap(metrics['complexity'])
        self._generate_dependency_graph(metrics['dependencies'])
        self._generate_security_radar(metrics['security'])
        self._generate_performance_timeline(metrics['performance'])
        self._generate_quality_metrics_sunburst(metrics['quality'])
        self._generate_pattern_distribution(metrics['patterns'])

        return self.generated_files

    def _generate_score_dashboard(self, metrics: Dict[str, Any]) -> None:
        """Generate a dashboard of key metric scores."""
        plt.figure(figsize=(12, 6))

        scores = {
            'Overall': metrics['overall_score'],
            'Quality': metrics['quality'].quality_score,
            'Security': metrics['security'].security_score,
            'Performance': metrics['performance'].performance_score,
            'Maintainability': metrics['complexity'].maintainability_index
        }

        # Create horizontal bar chart
        categories = list(scores.keys())
        values = list(scores.values())

        colors = ['#2ecc71' if v >= 80 else '#f1c40f' if v >= 60 else '#e74c3c' 
                 for v in values]

        y_pos = np.arange(len(categories))
        plt.barh(y_pos, values, color=colors)
        plt.yticks(y_pos, categories)

        # Add value labels
        for i, v in enumerate(values):
            plt.text(v + 1, i, f'{v:.1f}', va='center')

        plt.xlabel('Score (0-100)')
        plt.title('Codebase Health Dashboard')

        # Save the figure
        output_path = self.output_dir / 'score_dashboard.png'
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

        self.generated_files.append(output_path)

    def _generate_complexity_heatmap(self, complexity_metrics: Any) -> None:
        """Generate a heatmap of code complexity across the codebase."""
        plt.figure(figsize=(12, 8))

        # Prepare complexity data
        complexity_data = []
        for func in complexity_metrics.complex_functions:
            module_path = func.location.split(':')[0]
            complexity_data.append({
                'module': module_path,
                'function': func.name,
                'complexity': func.complexity
            })

        # Create matrix for heatmap
        if complexity_data:
            df = pd.DataFrame(complexity_data)
            pivot_table = df.pivot_table(
                values='complexity',
                index='module',
                columns='function',
                fill_value=0
            )

            # Generate heatmap
            sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd')
            plt.title('Code Complexity Heatmap')
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)

            # Save the figure
            output_path = self.output_dir / 'complexity_heatmap.png'
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
            plt.close()

            self.generated_files.append(output_path)

    def _generate_dependency_graph(self, dependency_metrics: Any) -> None:
        """Generate a network graph of project dependencies."""
        G = nx.DiGraph()

        # Add nodes and edges
        for dep in dependency_metrics.direct_dependencies:
            G.add_edge(dep['source'], dep['target'])
            if 'weight' in dep:
                G[dep['source']][dep['target']]['weight'] = dep['weight']

        plt.figure(figsize=(12, 12))

        # Calculate node sizes based on degree
        node_sizes = [3000 * (1 + G.degree(node)) for node in G.nodes()]

        # Calculate edge weights
        edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]

        # Layout
        pos = nx.spring_layout(G, k=1, iterations=50)

        # Draw the graph
        nx.draw(G, pos,
                node_color='lightblue',
                node_size=node_sizes,
                edge_color='gray',
                width=edge_weights,
                with_labels=True,
                font_size=8,
                font_weight='bold',
                arrows=True,
                arrowsize=20)

        plt.title('Project Dependency Graph')

        # Save the figure
        output_path = self.output_dir / 'dependency_graph.png'
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

        self.generated_files.append(output_path)

    def _generate_security_radar(self, security_metrics: Any) -> None:
        """Generate a radar chart of security metrics."""
        # Prepare security metrics
        categories = [
            'Vulnerability Score',
            'Pattern Coverage',
            'Authentication',
            'Authorization',
            'Data Protection',
            'Code Safety'
        ]

        values = [
            100 - len(security_metrics.vulnerabilities),  # Inverse of vulnerability count
            security_metrics.pattern_coverage * 100,
            security_metrics.auth_score,
            security_metrics.authz_score,
            security_metrics.data_protection_score,
            security_metrics.code_safety_score
        ]

        # Number of variables
        num_vars = len(categories)

        # Compute angle for each axis
        angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
        angles += angles[:1]

        # Initialize the spider plot
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

        # Plot data
        values += values[:1]
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)

        # Set the labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        # Add title
        plt.title('Security Metrics Radar')

        # Save the figure
        output_path = self.output_dir / 'security_radar.png'
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

        self.generated_files.append(output_path)

    def _generate_performance_timeline(self, performance_metrics: Any) -> None:
        """Generate a timeline of performance metrics."""
        plt.figure(figsize=(12, 6))

        # Prepare performance data
        hotspots = performance_metrics.hotspots
        hotspots.sort(key=lambda x: x.severity)

        # Create timeline
        y_positions = range(len(hotspots))
        labels = [f"{h.type}\n({h.severity})" for h in hotspots]

        # Create color map for severity
        colors = {
            'HIGH': '#e74c3c',
            'MEDIUM': '#f1c40f',
            'LOW': '#2ecc71'
        }

        plt.hlines(y_positions, 0, [h.impact_score for h in hotspots], 
                  color=[colors[h.severity] for h in hotspots], alpha=0.7)
        plt.scatter([h.impact_score for h in hotspots], y_positions,
                   color=[colors[h.severity] for h in hotspots], alpha=0.7)

        plt.yticks(y_positions, labels)
        plt.xlabel('Impact Score')
        plt.title('Performance Hotspots Timeline')

        # Save the figure
        output_path = self.output_dir / 'performance_timeline.png'
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

        self.generated_files.append(output_path)

    def _generate_quality_metrics_sunburst(self, quality_metrics: Any) -> None:
        """Generate a sunburst chart of code quality metrics."""
        plt.figure(figsize=(12, 12))

        # Prepare data structure for sunburst
        data = {
            'Documentation': {
                'Coverage': quality_metrics.documentation_coverage,
                'Quality': quality_metrics.documentation_quality
            },
            'Testing': {
                'Coverage': quality_metrics.test_coverage,
                'Quality': quality_metrics.test_quality
            },
            'Code Style': {
                'Consistency': quality_metrics.style_consistency,
                'Standards': quality_metrics.style_standards
            }
        }

        # Create sunburst chart
        def plot_sunburst(data, radius=1, center=(0, 0), start_angle=0):
            total = sum(
                value if isinstance(value, (int, float)) 
                else sum(subvalue for subvalue in value.values())
                for value in data.values()
            )

            current_angle = start_angle
            for category, values in data.items():
                if isinstance(values, dict):
                    # Draw parent segment
                    category_total = sum(values.values())
                    angle = 2 * np.pi * category_total / total

                    # Draw children
                    plot_sunburst(values, radius=radius*0.7, 
                                center=center, start_angle=current_angle)
                    current_angle += angle
                else:
                    angle = 2 * np.pi * values / total

                    # Create wedge
                    wedge = plt.matplotlib.patches.Wedge(
                        center, radius, 
                        current_angle*180/np.pi, 
                        (current_angle + angle)*180/np.pi,
                        alpha=0.7
                    )
                    plt.gca().add_patch(wedge)

                    # Add label
                    text_angle = current_angle + angle/2
                    text_x = center[0] + (radius*0.5) * np.cos(text_angle)
                    text_y = center[1] + (radius*0.5) * np.sin(text_angle)
                    plt.text(text_x, text_y, f'{category}\n{values:.1%}', 
                            ha='center', va='center')

                    current_angle += angle

        # Plot the sunburst
        plt.gca().set_aspect('equal')
        plot_sunburst(data)
        plt.title('Code Quality Metrics Sunburst')

        # Save the figure
        output_path = self.output_dir / 'quality_sunburst.png'
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

        self.generated_files.append(output_path)

    def _generate_pattern_distribution(self, pattern_metrics: Any) -> None:
        """Generate a treemap of detected code patterns."""
        plt.figure(figsize=(12, 8))

        # Prepare pattern data
        patterns = pattern_metrics.design_patterns

        # Group patterns by category
        pattern_groups = {}
        for pattern in patterns:
            if pattern.category not in pattern_groups:
                pattern_groups[pattern.category] = []
            pattern_groups[pattern.category].append(pattern)

        # Create treemap data
        sizes = []
        labels = []
        colors = []

        color_map = plt.cm.get_cmap('Set3')
        for i, (category, category_patterns) in enumerate(pattern_groups.items()):
            base_color = color_map(i / len(pattern_groups))
            for pattern in category_patterns:
                sizes.append(pattern.confidence * 100)
                labels.append(f'{pattern.name}\n{pattern.confidence:.1%}')
                colors.append(base_color)

        # Create treemap
        squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.7)
        plt.title('Design Pattern Distribution')
        plt.axis('off')

        # Save the figure
        output_path = self.output_dir / 'pattern_distribution.png'
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

        self.generated_files.append(output_path)

    def generate_html_report(self) -> Path:
        """Generate an HTML report containing all visualizations."""
        html_content = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "    <title>Codebase Analysis Report</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; margin: 20px; }",
            "        .visualization { margin: 20px 0; text-align: center; }",
            "        img { max-width: 100%; height: auto; }",
            "        h1, h2 { color: #333; }",
            "    </style>",
            "</head>",
            "<body>",
            "    <h1>Codebase Analysis Report</h1>",
            f"    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        ]

        # Add each visualization
        for file_path in self.generated_files:
            section_name = file_path.stem.replace('_', ' ').title()
            html_content.extend([
                f"    <div class='visualization'>",
                f"        <h2>{section_name}</h2>",
                f"        <img src='{file_path.name}' alt='{section_name}'>",
                f"    </div>"
            ])

        html_content.extend([
            "</body>",
            "</html>"
        ])

        # Save HTML report
        report_path = self.output_dir / 'analysis_report.html'
        report_path.write_text('\n'.join(html_content))
        self.generated_files.append(report_path)

        return report_path