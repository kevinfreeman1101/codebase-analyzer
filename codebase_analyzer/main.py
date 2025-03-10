import sys
import logging
from codebase_analyzer.analyzer import CodebaseAnalyzer
from codebase_analyzer.formatters.comprehensive_formatter import ComprehensiveFormatter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("Starting main execution")
    analyzer = CodebaseAnalyzer(sys.argv[1] if len(sys.argv) > 1 else ".")
    logging.info("Analyzer initialized")
    try:
        result = analyzer.analyze_project(sys.argv[1] if len(sys.argv) > 1 else ".")
        logging.info("Analysis completed with keys: %s", list(result.keys()))
    except Exception as e:
        logging.error("Analysis failed: %s", str(e))
        return
    if not result:
        logging.warning("No analysis result returned")
        return
    formatter = ComprehensiveFormatter()
    logging.info("Starting format_analysis")
    try:
        formatted_output = formatter.format_analysis(result)
        logging.info("Finished format_analysis")
        print(formatted_output)
    except Exception as e:
        logging.error("Formatting failed: %s", str(e))

if __name__ == "__main__":
    main()
