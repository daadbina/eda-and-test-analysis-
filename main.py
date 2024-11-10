import logging
from services.data_loader import DataLoader
from services.data_cleaner import DataCleaner
from controllers.report_generator import ReportGenerator  
from models.database import Database
from config.settings import DB_PATH, INVOICES_CSV_PATH, PRODUCTS_CSV_PATH, TEST_CSV_PATH
from logger import setup_logger
import sqlite3
from controllers.plot_generator import PlotGenerator
# from controllers.pdf_generator import PDFGenerator


def main():
    logger = setup_logger() 
    logger = logging.getLogger(__name__)

    try:
        logger.info("Program started. Loading database...")

        # Load data
        data_loader = DataLoader()
        raw_data = data_loader.load_data()

        # Clean data
        data_cleaner = DataCleaner(raw_data)
        cleaned_data = data_cleaner.clean_all()

        # Load the database
        try:
            db = Database(DB_PATH)

            # Load cleaned data into the database
            with sqlite3.connect(db.db_path) as conn:
                cleaned_data["invoices"].to_sql("invoices", conn, if_exists="replace", index=False)
                cleaned_data["products"].to_sql("products", conn, if_exists="replace", index=False)
                cleaned_data["test"].to_sql("test_analysis", conn, if_exists="replace", index=False)

            # Log CSV loading
            logger.debug(f"Loading CSV file: {INVOICES_CSV_PATH}")
            db.load_csv_to_db(INVOICES_CSV_PATH, 'invoices')

            logger.debug(f"Loading CSV file: {PRODUCTS_CSV_PATH}")
            db.load_csv_to_db(PRODUCTS_CSV_PATH, 'products')

            logger.debug(f"Loading CSV file: {TEST_CSV_PATH}")
            db.load_csv_to_db(TEST_CSV_PATH, 'test_analysis')
        except Exception as e:
            logger.error(f"Error loading CSV files: {str(e)}")

        # Generate report using ReportGenerator
        try:
            logger.info("Generating full report using ReportGenerator...")
            report_generator = ReportGenerator()
            report_data = report_generator.generate_summary()  # Run analyses and get report data
            report_generator.save_report(report_data)  # Save the report to file
                        
            plot_generator = PlotGenerator()
            plot_generator.generate_plots()


            # pdff_generator = PDFGenerator()
            # pdff_generator.generate_reports()

        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")

    except Exception as e:
        logger.error(f"An error occurred during the main execution: {str(e)}")

if __name__ == "__main__":
    main()
