import pandas as pd

EXCEL_RECIPE_PATH = r'C:\Users\moric\Documents\CS\year4\B\Food-Planner\dataset\recipes_with_product_tuples_.xlsx' # TODO change

class RecipeFinder:
    def __init__(self, excel_path = EXCEL_RECIPE_PATH):
        """
        Initializes the RecipeFinder with data loaded from the provided Excel file.

        :param excel_path: The path to the Excel file containing the recipe data.
        """
        self.excel_path = excel_path
        self.data = pd.read_excel(self.excel_path)
        self.data['Products'] = self.data['Products'].apply(lambda x: {item.strip() for item in x.split(',')})
        self.product_to_recipes = self._build_product_index()

    def _build_product_index(self):
        """
        Builds an index mapping products to recipes for quick lookup.

        :return: A dictionary where keys are products and values are sets of Recipe IDs that contain the product.
        """
        product_index = {}
        for _, row in self.data.iterrows():
            recipe_id = row['Recipe ID']
            for product in row['Products']:
                if product not in product_index:
                    product_index[product] = set()
                product_index[product].add(recipe_id)
        return product_index

    def find_recipes_by_product(self, product_name):
        """
        Finds recipes that contain the specified product.

        :param product_name: The name of the product to search for.
        :return: A list of Recipe IDs that include the product.
        """
        product_name = product_name.strip()
        recipes = self.product_to_recipes.get(product_name, set())
        return list(recipes)

    def find_recipes_by_multiple_products(self, product_names):
        """
        Finds recipes that contain all of the specified products.

        :param product_names: A list of product names to search for.
        :return: A list of Recipe IDs that include all of the specified products.
        """
        product_names = [name.strip() for name in product_names]
        recipe_sets = [self.product_to_recipes.get(product, set()) for product in product_names]
        common_recipes = set.intersection(*recipe_sets) if recipe_sets else set()
        return list(common_recipes)

    def get_recipe_details(self, recipe_id):
        """
        Retrieves the details of a recipe by its Recipe ID.

        :param recipe_id: The Recipe ID to search for.
        :return: A pandas Series containing the recipe details or None if not found.
        """
        recipe = self.data[self.data['Recipe ID'] == recipe_id]
        return recipe.iloc[0] if not recipe.empty else None

# Usage example
def main():
    finder = RecipeFinder()

    # Find recipes that contain a specific product
    product = 'Pine Nuts (gr)'
    recipes_with_product = finder.find_recipes_by_product(product)
    print(f"Recipes containing '{product}': {recipes_with_product}")

    # Find recipes that contain multiple specific products
    products = ['Pine Nuts (gr)', 'Pesto Sauce (ml)']
    recipes_with_multiple_products = finder.find_recipes_by_multiple_products(products)
    print(f"Recipes containing {products}: {recipes_with_multiple_products}")

    # Get details of a specific recipe
    if recipes_with_product:
        recipe_id = recipes_with_product[0]  # Example: Get the first recipe ID from the list
        recipe_details = finder.get_recipe_details(recipe_id)
        print(f"Details of Recipe {recipe_id}:\n{recipe_details}")

if __name__ == "__main__":
    main()
