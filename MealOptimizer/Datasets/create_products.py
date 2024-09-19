import pandas as pd
import random
from datetime import datetime, timedelta
import sys
import os


def extract_products_from_recipes(recipes_df, num_recipes):
    # Randomly select recipes
    selected_recipes = recipes_df.sample(n=num_recipes)

    # Extract products from selected recipes
    all_products = []
    for _, row in selected_recipes.iterrows():
        product_list = row['Products'].split(',')
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
    return products_df, selected_recipes['Recipe ID'].tolist()


def generate_additional_products(num_additional):
    additional_products = []
    for _ in range(num_additional):
        additional_products.append({
            'Product Name': f"Random Product {_ + 1}",
            'Quantity': random.randint(1, 1000),
            'Unit': random.choice(['gr', 'ml', 'pieces'])
        })
    return pd.DataFrame(additional_products)


def generate_random_date():
    today = datetime.now()
    one_month_later = today + timedelta(days=30)
    random_date = today + timedelta(days=random.randint(0, 30))
    return random_date.strftime('%Y-%m-%d')


def create_csv_with_products(products_df, output_file):
    # Add ID and Date columns
    products_df['ID'] = [f'P{i:03d}' for i in range(1, len(products_df) + 1)]
    products_df['Date'] = [generate_random_date() for _ in range(len(products_df))]

    # Reorder columns
    products_df = products_df[['ID', 'Product Name', 'Quantity', 'Unit', 'Date']]

    # Save the DataFrame as CSV
    products_df.to_csv(output_file, index=False)
    print(f"CSV file created: {output_file}")


# Main execution
if __name__ == "__main__":

    recipes_file = r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\100_reciepes\reciepes.csv"
    # Read the recipes CSV file
    recipes_df = pd.read_csv(recipes_file)

    for i in range(10):
        num_recipes = i
        num_additional_rows = 10


        # Extract products from randomly selected recipes
        products_df, selected_recipe_ids = extract_products_from_recipes(recipes_df, num_recipes)

        # Generate additional random products
        additional_products_df = generate_additional_products(num_additional_rows)

        # Combine products from recipes and additional products
        all_products_df = pd.concat([products_df, additional_products_df], ignore_index=True)

        # Create the output file name
        output_filename = f"products_{'_'.join(selected_recipe_ids)}.csv"

        # Get the directory of the input file and construct the full output path
        output_directory = os.path.dirname(os.path.abspath(recipes_file))
        output_file = os.path.join(output_directory, output_filename)

        # Create the CSV file
        create_csv_with_products(all_products_df, output_file)

        print(f"Selected recipes: {', '.join(selected_recipe_ids)}")
        print(f"Total products: {len(all_products_df)}")