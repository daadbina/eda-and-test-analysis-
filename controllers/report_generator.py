from services.eda_service import EDAService
from services.test_analysis_service import TestAnalysisService
from config.settings import INVOICES_FILE, PRODUCTS_FILE, TEST_FILE
import logging

class ReportGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.eda_service = EDAService()
            self.test_analysis_service = TestAnalysisService()
            self.logger.info("ReportGenerator initialized successfully.")
        except Exception as e:
            self.logger.error(f"Error initializing ReportGenerator: {e}")
            raise

    def generate_summary(self):
        """Run analyses and generate a summary report"""
        try:
            self.logger.info("Generating EDA and test analysis summaries for report...")
            eda_results = self.eda_service.generate_report()
            test_analysis_results = self.test_analysis_service.generate_report()
            self.logger.info("Summary report generation completed successfully.")
            return {"eda_results": eda_results, "test_analysis_results": test_analysis_results}

        except Exception as e:
            error_message = f"Error generating summary report: {e}"
            self.logger.error(error_message)
            return None

    def save_report(self, report_data, file_path='output/summary_report.md'):
        """Save the final report in a Markdown file"""
        try:
            self.logger.info(f"Saving report to {file_path}...")
            with open(file_path, 'w') as f:
                f.write("# Summary Report\n\n")
                f.write("## Exploratory Data Analysis (EDA) Results\n")
                
                # Product Sales Summary
                f.write("### Product Sales Summary:\n")
                if 'product_sales_summary' in report_data['eda_results']:
                    for row in report_data['eda_results']['product_sales_summary']:
                        f.write(f"- Product: {row['Product']}, Total Sales: {row['Total Sales']}\n")
                else:
                    f.write("No product sales data available.\n")
                
                # Event Sales Summary
                f.write("\n### Event Sales Summary:\n")
                if 'event_sales_summary' in report_data['eda_results']:
                    for row in report_data['eda_results']['event_sales_summary']:
                        f.write(f"- Event ID: {row['Event ID']}, Total Sales: {row['Total Sales']}\n")
                else:
                    f.write("No event sales data available.\n")

                # Product Sales Statistics
                f.write("\n### Product Sales Statistics:\n")
                if 'product_sales_statistics' in report_data['eda_results']:
                    stats = report_data['eda_results']['product_sales_statistics']
                    f.write(f"- Mean Sales: {stats.get('mean', 'N/A')}\n")
                    f.write(f"- Std Dev: {stats.get('std', 'N/A')}\n")
                    f.write(f"- Min Sales: {stats.get('min', 'N/A')}\n")
                    f.write(f"- Max Sales: {stats.get('max', 'N/A')}\n")
                else:
                    f.write("No statistics data available.\n")

                # Percentage Changes in Sales
                f.write("\n### Percentage Changes in Sales:\n")
                if 'percentage_changes' in report_data['eda_results']:
                    changes = report_data['eda_results']['percentage_changes']
                    f.write(f"- Change from A to B: {changes.get('B_A', 'N/A')}%\n")
                    f.write(f"- Change from A to C: {changes.get('C_A', 'N/A')}%\n")
                    f.write(f"- Change from A to D: {changes.get('D_A', 'N/A')}%\n")
                else:
                    f.write("No percentage change data available.\n")
                
                f.write("\n## Test Analysis Results\n")
                
                # UI and Description Changes
                f.write("### UI and Description Changes:\n")
                if 'ui_desc_changes' in report_data['test_analysis_results']:
                    for row in report_data['test_analysis_results']['ui_desc_changes']:
                        f.write(f"- UI Change: {row['UI Change']}, Description Change: {row['Description Change']}, Average Purchase: {row['Average Purchase']}\n")
                else:
                    f.write("No UI and Description changes data available.\n")
                
                # Product, UI, and Description Changes
                f.write("\n### Product, UI, and Description Changes:\n")
                if 'product_ui_desc_changes' in report_data['test_analysis_results']:
                    for row in report_data['test_analysis_results']['product_ui_desc_changes']:
                        f.write(f"- Product: {row['Product']}, UI Change: {row['UI Change']}, Description Change: {row['Description Change']}, Average Purchase: {row['Average Purchase']}\n")
                else:
                    f.write("No product, UI, and description changes data available.\n")

            self.logger.info(f"Report saved successfully to {file_path}")

        except Exception as e:
            error_message = f"Unexpected error occurred while saving report: {e}"
            self.logger.error(error_message)
