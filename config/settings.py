ENV = 'DEBUG'
LOG_FILE_PATH = 'app.log'

DATA_PATH = "data/"
INVOICES_FILE = DATA_PATH + "tbl_invoices.csv"
PRODUCTS_FILE = DATA_PATH + "tbl_products.csv"
TEST_FILE = DATA_PATH + "tbl_test.csv"
REPORT_OUTPUT_FILE = 'output/summary_report.md'

# Column names
COLUMN_USER_ID = 'userid'
COLUMN_DATE_PAID = 'datepaid'
COLUMN_EVENT_ID = 'event_id'
COLUMN_AMOUNT = 'amount'
COLUMN_PRODUCT_NAME = 'product_name'
COLUMN_UI_CHANGE = 'ui_change'
COLUMN_DESC_CHANGE = 'desc_change'

# Tables output
PRODUCT_SALES_SUMMARY_TITLE = "### Product Sales Summary\n"
EVENT_SALES_SUMMARY_TITLE = "### Event Sales Summary\n"
UI_CHANGE_IMPACT_TITLE = "### UI Change Impact\n"
DESC_CHANGE_IMPACT_TITLE = "### Description Change Impact\n"
GROUP_COMPARISON_TITLE = "### Average Purchase Amount by UI and Description Change\n"
PRODUCT_SPECIFIC_ANALYSIS_TITLE = "### Average Purchase Amount by Product, UI, and Description Change\n"

# Start/Finish date
ANALYSIS_START_DATE = "2020-05-01"
ANALYSIS_END_DATE = "2020-09-01"


# Database path
DB_PATH = 'database.db'

# CSV file paths
INVOICES_CSV_PATH = 'data/tbl_invoices.csv'
PRODUCTS_CSV_PATH = 'data/tbl_products.csv'
TEST_CSV_PATH = 'data/tbl_test.csv'


