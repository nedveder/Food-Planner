import pandas as pd
import random
from datetime import datetime, timedelta

EXCEL_PRODUCT_PATH = r'C:\Users\moric\Documents\CS\year4\B\Food-Planner\Datasets\products_data.csv'  # TODO change


# will set the future date to a month from now if not filled
class ProductDataProcessor:
    def __init__(self, sample_size, future_date=None, excel_path=EXCEL_PRODUCT_PATH):
        self.excel_path = excel_path
        self.products_df = pd.read_csv(self.excel_path)
        self.random_data_set = self.create_smaller_dataset(sample_size, future_date)

    def create_smaller_dataset(self, sample_size, future_date=None):
        """
        Creates a smaller dataset with random dates up to the given future date.

        :param sample_size: The number of rows for the smaller dataset.
        :param future_date: The latest possible date for the 'Date' column (format: 'YYYY-MM-DD').
        :return: A pandas DataFrame with the smaller dataset.
        """
        # Convert future date to datetime (if needed)

        # Remove duplicates based on the 'Product Name' column
        unique_products_df = self.products_df.drop_duplicates(subset=['Product Name'])

        # Select a random subset of the unique data
        smaller_df = unique_products_df.sample(n=min(sample_size, len(unique_products_df))).reset_index(drop=True)

        # Assign random dates between now and the future_date
        smaller_df['Date'] = smaller_df['Date'].apply(lambda x: self.generate_random_date(future_date))

        return smaller_df

    def get_products_df(self):
        return self.random_data_set

    def generate_random_date(self, future_date):
        """
        Generates a random date between today and the specified future date.

        :param future_date: The future date limit.
        :return: A random date as a string.
        """
        start_date = datetime.now()
        future_date = datetime.strptime(future_date, '%Y-%m-%d') if future_date else start_date + timedelta(days=30)
        random_days = random.randint(0, (future_date - start_date).days)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime('%Y-%m-%d')

    def save_to_excel(self, output_path):
        """
        Saves the DataFrame to an Excel file.

        :param df: The DataFrame to save.
        :param output_path: The file path for the output Excel file.
        """
        self.random_data_set.to_excel(output_path, index=False)
        print(f"Dataset saved to {output_path}")


def main():
    sample_size = 100  # Number of products in the smaller dataset
    # future_date = '2024-12-31'  # Example future date
    processor = ProductDataProcessor(sample_size)

    # Create a smaller dataset with random dates
    smaller_dataset = processor.create_smaller_dataset(sample_size)

    # Save the smaller dataset to a new Excel file
    output_path = 'smaller_products_data.xlsx'  # Define your output path
    processor.save_to_excel(output_path)


if __name__ == "__main__":
    main()
