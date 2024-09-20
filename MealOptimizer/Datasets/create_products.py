import pandas as pd
import random
from datetime import datetime, timedelta
import sys
import os
import re
import ast  # Import the ast module


def add_random_column(input_csv, output_csv, column_name="random_number"):
    # Read the input CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # Generate a list of random numbers between 1 and 10 for each row
    df["Taste Rating"] = [random.randint(1, 10) for _ in range(len(df))]
    df["Shelf Time"] = [random.randint(2, 30) for _ in range(len(df))]


    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)

    print(f"New column '{column_name}' with random numbers between 1-10 added and saved to {output_csv}")




def select_random_rows(input_csv, num_rows, output_csv):
    # Read the input CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # Check if num_rows is less than or equal to the number of rows in the DataFrame
    if num_rows > len(df):
        print(f"Number of rows requested exceeds total rows in the file. Selecting all {len(df)} rows.")
        num_rows = len(df)

    # Randomly select the specified number of rows
    selected_rows = df.sample(n=num_rows, random_state=random.randint(0, 1000))

    # Save the selected rows to a new CSV file
    selected_rows.to_csv(output_csv, index=False)

    print(f"{num_rows} rows selected and saved to {output_csv}")

def remove_less_then_given_number_of(input_csv, num_rows, output_csv):
    # Read the input CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # Check if num_rows is less than or equal to the number of rows in the DataFrame
    if num_rows > len(df):
        print(f"Number of rows requested exceeds total rows in the file. Selecting all {len(df)} rows.")
        num_rows = len(df)
    # remove rows with less then num_rows in Number of Products
    df = df[df['Number of Products'] >= num_rows]

    # Save the selected rows to a new CSV file
    df.to_csv(output_csv, index=False)




def extract_all_products_from_recipes(recipes_df):
    # Extract products from all recipes
    all_products = []
    for _, row in recipes_df.iterrows():
        # Use ast.literal_eval to parse the 'Products' string into a list
        try:
            product_list = ast.literal_eval(row['Products'])
        except (ValueError, SyntaxError):
            # Handle the case where 'Products' is not a valid list string
            print(f"Error parsing products for recipe ID {row['Recipe ID']}. Skipping this recipe.")
            continue  # Skip to the next recipe

        for product in product_list:
            name = product.strip()
            quantity = 1  # Default quantity
            all_products.append({
                'Product Name': name,
                'Quantity': float(quantity)
            })

    # Convert to DataFrame and remove duplicates
    products_df = pd.DataFrame(all_products).drop_duplicates(subset=['Product Name'])
    return products_df

def select_random_products_with_quantities(products_df, num_products):
    # Randomly select product names
    selected_products = products_df.sample(n=num_products).copy()

    # Assign random quantities between 1 and 5
    selected_products['Quantity'] = [random.randint(1, 5) for _ in range(num_products)]

    # Reset index if necessary
    selected_products.reset_index(drop=True, inplace=True)
    return selected_products

def extract_products_from_recipes(recipes_df, num_recipes):
    # Randomly select recipes
    selected_recipes = recipes_df.sample(n=num_recipes)

    # Extract products from selected recipes
    all_products = []
    for _, row in selected_recipes.iterrows():
        product_list = re.findall(r"'([^']*)'", row['Products'])
        product_list = [product.strip() for product in product_list]
        for product in product_list:
            # Remove leading/trailing whitespace and single/double quotes
            name = product.strip().strip("'\"")
            quantity = 1
            all_products.append({
                'Product Name': name,
                'Quantity': float(quantity)
            })

    # Convert to DataFrame and remove duplicates
    products_df = pd.DataFrame(all_products).drop_duplicates(subset=['Product Name'])
    return products_df, selected_recipes['Recipe ID'].tolist()

def generate_additional_products(num_additional):
    additional_products = []
    for _ in range(num_additional):
        additional_products.append({
            'Product Name': f"Random Product {_ + 1}",
            'Quantity': random.randint(1, 5)
        })
    return pd.DataFrame(additional_products)

def generate_random_date():
    today = datetime.now()
    random_date = today + timedelta(days=random.randint(0, 30))
    return random_date.strftime('%Y-%m-%d')

def create_csv_with_products(products_df, output_file):
    # Add ID and Date columns
    products_df['ID'] = [f'P{i:03d}' for i in range(1, len(products_df) + 1)]
    products_df['Date'] = [generate_random_date() for _ in range(len(products_df))]

    # Reorder columns
    products_df = products_df[['ID', 'Product Name', 'Quantity', 'Date']]

    # Save the DataFrame as CSV
    products_df.to_csv(output_file, index=False)
    print(f"CSV file created: {output_file}")



# Main execution
if __name__ == "__main__":

    recipes_file = r"C:\Users\moric\Documents\CS\year4\B\Food-Planner\MealOptimizer\Datasets\recipes.csv"
    # Read the recipes CSV file
    recipes_df = pd.read_csv(recipes_file)

    all_products_df = extract_all_products_from_recipes(recipes_df)

    for i in [0,50,100,200,300,400]:
        num_recipes = i
        num_additional_rows = 1000


        # Extract products from randomly selected recipes
        products_df, selected_recipe_ids = extract_products_from_recipes(recipes_df, num_recipes)

        # Generate additional random products

        random_products_df = select_random_products_with_quantities(all_products_df, num_additional_rows)


        # Combine products from recipes and additional products
        final_products_df = pd.concat([products_df, random_products_df], ignore_index=True)

        # Create the output file name
        st = str(num_recipes)
        # output_filename = f"{st}_{'_'.join(map(str, selected_recipe_ids))}.csv"
        output_filename = f"known_{st}.csv"

        # Get the directory of the input file and construct the full output path
        output_directory = os.path.dirname(os.path.abspath(recipes_file))
        output_file = os.path.join(output_directory, output_filename)

        # Create the CSV file
        create_csv_with_products(final_products_df, output_file)

        # print(f"Selected recipes: {', '.join(selected_recipe_ids)}")
        print(f"Total products: {len(final_products_df)}")