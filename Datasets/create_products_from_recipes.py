import pandas as pd
import random
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def extract_products(recipes_file):
    # Read the recipes CSV file
    df = pd.read_csv(recipes_file)

    # Extract all products from the 'Products' column
    all_products = []
    for products in df['Products']:
        product_list = products.split(',')
        for product in product_list:
            name, info = product.rsplit('(', 1)
            quantity, unit = info[:-1].split(' ', 1)
            all_products.append({
                'Product Name': name.strip(),
                'Quantity': float(quantity),
                'Unit': unit.strip()
            })

    # Convert to DataFrame and remove duplicates
    products_df = pd.DataFrame(all_products).drop_duplicates(subset=['Product Name'])
    return products_df


def generate_random_date():
    # Generate a random date between today and a month from now
    today = datetime.now()
    one_month_later = today + timedelta(days=30)
    random_date = today + timedelta(days=random.randint(0, 30))
    return random_date.strftime('%Y-%m-%d')


def create_excel_with_products(products_df, output_file):
    # Add ID and Date columns
    products_df['ID'] = [f'P{i:03d}' for i in range(1, len(products_df) + 1)]
    products_df['Date'] = [generate_random_date() for _ in range(len(products_df))]

    # Reorder columns
    products_df = products_df[['ID', 'Product Name', 'Quantity', 'Unit', 'Date']]

    # Create a new workbook and select the active sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Products"

    # Write the DataFrame to the Excel sheet
    for r in dataframe_to_rows(products_df, index=False, header=True):
        ws.append(r)

    # Save the workbook
    wb.save(output_file)
    print(f"Excel file created: {output_file}")


# Main execution
if __name__ == "__main__":
    recipes_file = "recipes.csv"  # Replace with your actual recipes CSV file path
    output_file = "products_inventory.xlsx"

    products_df = extract_products(recipes_file)
    create_excel_with_products(products_df, output_file)