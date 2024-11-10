import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
import numpy as np
from services.eda_service import EDAService

# Turn off DEBUG messages in matplotlib and Pillow
logging.getLogger('matplotlib').setLevel(logging.WARNING)  # Disable debug messages from matplotlib
logging.getLogger('PIL').setLevel(logging.WARNING)  # Disable debug messages from Pillow
logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)  # Disable font-related debug messages

class PlotGenerator:
    def __init__(self):
        # Initialize the logger
        self.logger = logging.getLogger(__name__)  # Initialize logger
        self.logger.setLevel(logging.INFO)  # Set log level to INFO

        # Add a console handler to the logger
        ch = logging.StreamHandler()  # Log output to console
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Initialize the EDAService to fetch data
        self.eda_service = EDAService()

        # Create the output directory if it doesn't exist
        self.output_dir = 'output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def plot_histogram(self, data, column_name, title, file_name):
        """Plot a histogram for a specific column and save it to a file"""
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(data[column_name], kde=True, bins=20, color='blue')
            plt.title(title)
            plt.xlabel(column_name)
            plt.ylabel("Frequency")
            plt.savefig(os.path.join(self.output_dir, file_name))  # Save the plot
            plt.close()  # Close the plot to avoid memory issues
        except Exception as e:
            self.logger.error(f"Error plotting histogram for {column_name}: {e}")

    def plot_boxplot(self, data, column_name, title, file_name):
        """Plot a boxplot to visualize the distribution and save it to a file"""
        try:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=data[column_name], color='orange')
            plt.title(title)
            plt.xlabel(column_name)
            plt.savefig(os.path.join(self.output_dir, file_name))  # Save the plot
            plt.close()  # Close the plot to avoid memory issues
        except Exception as e:
            self.logger.error(f"Error plotting boxplot for {column_name}: {e}")

    def plot_scatter(self, data, x_column, y_column, title, file_name):
        """Plot a scatter plot to explore the relationship between two columns and save it to a file"""
        try:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=data[x_column], y=data[y_column], color='green')
            plt.title(title)
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.savefig(os.path.join(self.output_dir, file_name))  # Save the plot
            plt.close()  # Close the plot to avoid memory issues
        except Exception as e:
            self.logger.error(f"Error plotting scatter plot for {x_column} vs {y_column}: {e}")

    def plot_heatmap(self, data, title, file_name):
        """Plot a heatmap of correlations and save it to a file"""
        try:
            # Select only numeric columns for heatmap and drop rows with NaN values
            numeric_data = data.select_dtypes(include=[float, int]).dropna()
            
            # If the numeric data is empty after dropping NaNs, log a warning
            if numeric_data.empty:
                self.logger.warning("No valid numeric data available for the heatmap.")
                return

            
            # Calculate correlation matrix
            correlation_matrix = numeric_data.corr()  # Correlation matrix of numeric columns
            plt.figure(figsize=(12, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
            plt.title(title)
            plt.savefig(os.path.join(self.output_dir, file_name))  # Save the plot
            plt.close()  # Close the plot to avoid memory issues
        except Exception as e:
            self.logger.error(f"Error plotting heatmap: {e}")

    def plot_average_sales_by_group(self, data, file_name):
        """Plot the average sales amount for each group (UI and Description) and save it to a file"""
        try:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='ui_change', y='amount', hue='desc_change', data=data, estimator=np.mean)
            plt.title('Average Sales Amount by UI and Description Changes')
            plt.xlabel('UI Change')
            plt.ylabel('Average Sales Amount')
            plt.legend(title='Description Change')
            plt.savefig(os.path.join(self.output_dir, file_name))  # Save the plot
            plt.close()  # Close the plot to avoid memory issues
        except Exception as e:
            self.logger.error(f"Error plotting average sales by group: {e}")

    def plot_sales_distribution(self, data, file_name):
        """Plot sales distribution across different groups and save it to a file"""
        try:
            plt.figure(figsize=(12, 6))
            sns.boxplot(x='event_name', y='amount', data=data)
            plt.title("Sales Distribution by Event Type")
            plt.savefig(os.path.join(self.output_dir, file_name))  # Save the plot
            plt.close()  # Close the plot to avoid memory issues
        except Exception as e:
            self.logger.error(f"Error plotting sales distribution: {e}")

    # def generate_group_sales_summary(self, data):
    #     """Group sales by UI and Description changes to find mean, sum, and count"""
    #     try:
    #         group_sales = data.groupby(['ui_change', 'desc_change']).agg({
    #             'amount': ['mean', 'sum', 'count']
    #         }).reset_index()
    #         return group_sales
    #     except Exception as e:
    #         self.logger.error(f"Error generating group sales summary: {e}")
    #         return None


    def generate_monthly_sales_plot(self, file_name):
        """Generate monthly sales plot"""
        try:
            # Get data
            result = self.eda_service.execute_query('monthly_sales_query')
            if result:
                # query to df                
                invoices_df = pd.DataFrame(result, columns=['amount', 'datepaid'])

                # Change date format
                invoices_df['datepaid'] = pd.to_datetime(invoices_df['datepaid'], format='%m/%d/%Y')

                # Add month_year_column
                invoices_df['month_year'] = invoices_df['datepaid'].dt.to_period('M')

                # Number of sales
                monthly_purchases = invoices_df.groupby('month_year').size()

                # Save chart
                plt.figure(figsize=(12, 6))
                monthly_purchases.plot(kind='line', marker='o')
                plt.title("Monthly Purchases Over Time")
                plt.xlabel("Month-Year")
                plt.ylabel("Number of Purchases")
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.savefig(os.path.join(self.output_dir, file_name))  # Save the plot
                plt.close()  # Close the plot to avoid memory issues

        except Exception as e:
            self.logger.error(f"Error generating monthly sales plot: {e}")

    def plot_sales_by_group(self, sales_data, file_name):
        """Generate a bar plot for sales by group"""
        try:
            # Extract groups and total sales from the query result
            groups = [entry['Group'] for entry in sales_data]
            total_sales = [entry['Total Sales'] for entry in sales_data]

            # Create the plot with a specific size
            plt.figure(figsize=(10, 6))  # Set figure size
            
            # Use seaborn to create a bar plot with 'hue' set to 'Group'
            sns.barplot(x=groups, y=total_sales, hue=groups, palette='viridis', legend=False)

            # Set plot title and labels for axes
            plt.title("Total Sales by Group", fontsize=16)
            plt.xlabel("Group", fontsize=14)
            plt.ylabel("Total Sales", fontsize=14)

            plt.savefig(os.path.join(self.output_dir, file_name))  # Save the plot
            plt.close()  # Close the plot to avoid memory issues

        except Exception as e:
            # Handle any exception that may occur during the plot generation
            print(f"Error generating plot: {e}")

    def generate_plots(self):
        """Generate all required plots for EDA"""
        try:
            report = self.eda_service.generate_report()  # Fetching the full EDA report

            # Example data (replace with actual data)
            final_data = self.eda_service.execute_query('final_data_query')  # Replace with actual query for the final data
            # Convert your list of tuples to a pandas DataFrame
            final_data_df = pd.DataFrame(final_data, columns=['product_name', 'amount', 'ui_change', 'desc_change'])

            # Plot histograms for relevant columns (e.g., 'amount')
            if final_data_df is not None and 'amount' in final_data_df.columns:
                self.plot_histogram(final_data_df, 'amount', 'Distribution of Sales Amount', 'sales_amount_histogram.png')

            # Plot histograms and box plot for z score
            if report['z_scores'] is not None :
                self.plot_histogram(report['z_scores'] , 'z_scores', 'Z-Score histogram', 'z_score_histogram.png')
                self.plot_boxplot(report['z_scores'], 'z_scores', 'Boxplot of Z-Score', 'z_score_boxplot.png')

            # Plot summery of groups
            if report['group_sales_summary'] is not None :
                self.plot_sales_by_group(report['group_sales_summary'], 'group_sale_summery.png')

            # Plot boxplots for relevant columns (e.g., 'amount')
            if final_data_df is not None and 'amount' in final_data_df.columns:
                self.plot_boxplot(final_data_df, 'amount', 'Boxplot of Sales Amount', 'sales_amount_boxplot.png')

            # Plot scatter plots for relevant columns (e.g., 'ui_change' vs 'amount')
            if final_data_df is not None and 'ui_change' in final_data_df.columns and 'amount' in final_data_df.columns:
                self.plot_scatter(final_data_df, 'ui_change', 'amount', 'Scatter Plot of UI Change vs Sales', 'ui_change_vs_sales_scatter.png')

            # Plot heatmap for correlations in the data
            # if final_data_df is not None:
            #     self.plot_heatmap(final_data_df, 'Correlation Heatmap of Sales Data', 'sales_data_heatmap.png')

            # Plot average sales amount for each group (UI and Description)
            if final_data_df is not None and 'ui_change' in final_data_df.columns and 'desc_change' in final_data_df.columns:
                self.plot_average_sales_by_group(final_data_df, 'average_sales_by_ui_desc.png')

            # Plot sales distribution across different groups
            if final_data_df is not None and 'event_name' in final_data_df.columns and 'amount' in final_data_df.columns:
                self.plot_sales_distribution(final_data_df, 'sales_distribution_by_event.png')

            # Generate group sales summary (mean, sum, count)
            # if final_data_df is not None:
            #     group_sales = self.generate_group_sales_summary(final_data_df)

            # Plot monthly sales
            self.generate_monthly_sales_plot('monthly_trend.png')  # اضافه کردن نمودار خریدهای ماهانه


        except Exception as e:
            self.logger.error(f"Error generating plots: {e}")
