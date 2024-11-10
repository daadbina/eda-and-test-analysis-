import os
import logging
from PIL import Image
from fpdf import FPDF
from config.settings import PDF_OUTPUT_PATH, REPORT_MARKDOWN_PATH

class PDFGenerator:
    def __init__(self):
        """Initializes the report generator with image paths and descriptions"""
        self.images = [
            "output\\average_sales_by_ui_desc.png", "output\\monthly_trend.png",
            "output\\sales_amount_boxplot.png", "output\\sales_amount_histogram.png",
            "output\\sales_data_heatmap.png", "output\\ui_change_vs_sales_scatter.png",
            "output\\z_score_boxplot.png", "output\\z_score_histogram.png"
        ]
        self.descriptions = [
            "Description for the first image.",
            "Description for the second image.",
            "Description for the third image.",
            "Description for the fourth image.",
            "Description for the fifth image.",
            "Description for the sixth image.",
            "Description for the seventh image.",
            "Description for the eighth image."
        ]
        self.pdf_output_path = PDF_OUTPUT_PATH
        self.markdown_output_path = REPORT_MARKDOWN_PATH
        self.logger = logging.getLogger(__name__)

        # Setup logger configuration
        logging.basicConfig(level=logging.INFO)

    def _generate_pdf(self):
        """Generates a PDF file with images and descriptions"""
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            image_width = 60  # Width of image in PDF
            image_height = 60  # Height of image in PDF

            for i in range(len(self.images)):
                # Load image
                img = Image.open(self.images[i])
                
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize image
                img.thumbnail((image_width, image_height))

                # Temporary save resized image as PNG to preserve transparency (if any)
                temp_img_path = f"temp_img_{i}.png"
                img.save(temp_img_path, "PNG")  # Save as PNG to preserve transparency

                # Add image to PDF
                x_position = 10 + (i % 4) * (image_width + 10)
                y_position = 30 + (i // 4) * (image_height + 30)
                pdf.image(temp_img_path, x=x_position, y=y_position, w=image_width, h=image_height)

                # Add description below the image
                pdf.ln(image_height + 5)
                pdf.multi_cell(0, 10, self.descriptions[i])

                # Remove temporary image file
                os.remove(temp_img_path)

            # Output the PDF to the specified path
            pdf.output(self.pdf_output_path)
            self.logger.info(f"PDF report generated successfully at {self.pdf_output_path}")

        except Exception as e:
            self.logger.error(f"Error generating PDF report: {e}")
            raise


    def _generate_markdown(self):
        """Generates a markdown file with images and descriptions"""
        try:
            markdown_content = "# Summary Report\n\n"

            for i in range(len(self.images)):
                markdown_content += f"## Image {i+1}\n"
                markdown_content += f"![Image {i+1}]({self.images[i]})\n"
                markdown_content += f"{self.descriptions[i]}\n\n"

            # Save the markdown content to a file
            with open(self.markdown_output_path, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)

            self.logger.info(f"Markdown report generated successfully at {self.markdown_output_path}")

        except Exception as e:
            self.logger.error(f"Error generating markdown report: {e}")
            raise

    def generate_reports(self):
        """Generates both the PDF and markdown reports"""
        try:
            self.logger.info("Starting report generation...")

            # Generate PDF and Markdown reports
            self._generate_pdf()
            self._generate_markdown()

            self.logger.info("Report generation completed successfully.")

        except Exception as e:
            self.logger.error(f"Error generating reports: {e}")
            raise
