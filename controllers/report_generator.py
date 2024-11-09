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
                f.write("### Product Sales Summary:\n")
                for row in report_data['eda_results']['product_sales_summary']:
                    f.write(f"- Product: {row['Product']}, Total Sales: {row['Total Sales']}\n")
                
                f.write("\n### Event Sales Summary:\n")
                for row in report_data['eda_results']['event_sales_summary']:
                    f.write(f"- Event ID: {row['Event ID']}, Total Sales: {row['Total Sales']}\n")
                
                f.write("\n## Test Analysis Results\n")
                f.write("### UI and Description Changes:\n")
                for row in report_data['test_analysis_results']['ui_desc_changes']:
                    f.write(f"- UI Change: {row['UI Change']}, Description Change: {row['Description Change']}, Average Purchase: {row['Average Purchase']}\n")

                f.write("\n### Product, UI, and Description Changes:\n")
                for row in report_data['test_analysis_results']['product_ui_desc_changes']:
                    f.write(f"- Product: {row['Product']}, UI Change: {row['UI Change']}, Description Change: {row['Description Change']}, Average Purchase: {row['Average Purchase']}\n")

            self.logger.info(f"Report saved successfully to {file_path}")

        except Exception as e:
            error_message = f"Unexpected error occurred while saving report: {e}"
            self.logger.error(error_message)

