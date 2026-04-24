import pandas as pd
import numpy as np
from pathlib import Path
import glob

class RecipeConsolidator:    
    def __init__(self, products_csv="data/products.csv", recipes_input_dir="data/recipes_input"):
        self.products_df = pd.read_csv(products_csv)
        self.recipes_input_dir = Path(recipes_input_dir)
        
        # Create PID-indexed map for quick lookup
        self.products_by_pid = {}
        for _, row in self.products_df.iterrows():
            self.products_by_pid[int(row['PID'])] = {
                'PID': row['PID'],
                'Name': row['Name'],
                'Price': row['Price'],
                'Nutritional Unit': row['Nutritional Unit'],
                'Calories (g)': row['Calories (g)'],
                'Protein (g)': row['Protein (g)'],
                'Total_Fat (g)': row['Total_Fat (g)'],
                'Carbohydrates (g)': row['Carbohydrates (g)'],
                'Quantity': row['Quantity'],
                'Category': row['Category']
            }
        
        self.recipes_list = []
        self.validation_errors = []
        self.validation_warnings = []
    
    def load_individual_recipes(self):
        if not self.recipes_input_dir.exists():
            self.recipes_input_dir.mkdir(exist_ok=True)
            print(f"Created {self.recipes_input_dir} directory")
            return
        
        recipe_files = glob.glob(str(self.recipes_input_dir / "*.csv"))
        
        if not recipe_files:
            print(f"No recipe files found in {self.recipes_input_dir}")
            return
        
        print(f"Found {len(recipe_files)} recipe file(s)")
        
        for file in sorted(recipe_files):
            try:
                df = pd.read_csv(file)
                person_name = Path(file).stem
                self._process_recipe_file(df, person_name)
            except Exception as e:
                self.validation_errors.append(f"Error reading {file}: {str(e)}")
    
    def _process_recipe_file(self, df, person_name):
        required_cols = ['Name', 'Type', 'Category', 'PIDs', 'Quantities']
        
        # Check required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            self.validation_errors.append(
                f"{person_name}: Missing columns: {missing_cols}"
            )
            return
        
        for idx, row in df.iterrows():
            recipe_name = str(row['Name']).strip()
            recipe_type = str(row['Type']).strip()
            category = str(row['Category']).strip()
            pids_str = str(row['PIDs']).strip()
            quantities_str = str(row['Quantities']).strip()
            
            # Parse PIDs and quantities
            try:
                pids = [int(p.strip()) for p in pids_str.split(';')]
                quantities = [q.strip() for q in quantities_str.split(';')]
            except ValueError as e:
                self.validation_warnings.append(
                    f"{person_name} - {recipe_name}: Invalid PID format: {e}"
                )
                continue
            
            if len(pids) != len(quantities):
                self.validation_warnings.append(
                    f"{person_name} - {recipe_name}: "
                    f"Mismatch between PIDs ({len(pids)}) and quantities ({len(quantities)})"
                )
                continue
            
            # Validate and collect ingredients
            recipe_details = {
                'name': recipe_name,
                'type': recipe_type,
                'category': category,
                'person': person_name,
                'ingredients': []
            }
            
            valid_recipe = True
            for pid, quantity in zip(pids, quantities):
                if pid not in self.products_by_pid:
                    self.validation_warnings.append(
                        f"{person_name} - {recipe_name}: PID {pid} not found in products"
                    )
                    valid_recipe = False
                    continue
                
                product_info = self.products_by_pid[pid]
                recipe_details['ingredients'].append({
                    'PID': pid,
                    'product_name': product_info['Name'],
                    'quantity': quantity,
                    'price': product_info['Price'],
                    'nutritional_unit': product_info['Nutritional Unit'],
                    'calories_per_unit': product_info['Calories (g)'],
                    'protein_per_unit': product_info['Protein (g)'],
                    'fat_per_unit': product_info['Total_Fat (g)'],
                    'carbs_per_unit': product_info['Carbohydrates (g)']
                })
            
            if valid_recipe and recipe_details['ingredients']:
                self.recipes_list.append(recipe_details)
    
    def calculate_totals(self):
        for recipe in self.recipes_list:
            total_price = 0
            total_calories = 0
            total_protein = 0
            total_fat = 0
            total_carbs = 0
            
            for ingredient in recipe['ingredients']:
                try:
                    qty_value = float(ingredient['quantity'].split()[0])
                except:
                    self.validation_warnings.append(
                        f"Could not parse quantity '{ingredient['quantity']}' "
                        f"in recipe '{recipe['name']}'"
                    )
                    continue
        
                product_qty_value = float(
                    self.products_by_pid[ingredient['PID']]['Quantity'].split()[0]  # Extract number from "100 g/ml"
                
                )
                
                price = ingredient['price'] * (qty_value / product_qty_value)
                total_price += price
                
                product_nutritional_unit = float(
                    ingredient['nutritional_unit'].split()[-2]  # Extract number from "100 g/ml"
                )

                calories = ingredient['calories_per_unit'] * (qty_value / product_nutritional_unit)
                total_calories += calories

                protein = ingredient['protein_per_unit'] * (qty_value / product_nutritional_unit)
                total_protein += protein

                fat = ingredient['fat_per_unit'] * (qty_value / product_nutritional_unit)
                total_fat += fat

                carbs = ingredient['carbs_per_unit'] * (qty_value / product_nutritional_unit)
                total_carbs += carbs
            total_protein *= 4
            total_fat *= 9
            total_carbs *= 4
            recipe['total_price'] = round(total_price, 2)
            recipe['provided_calories'] = round(total_calories, 2)
            recipe['provided_protein'] = round(total_protein, 2)
            recipe['provided_fat'] = round(total_fat, 2)
            recipe['provided_carbs'] = round(total_carbs, 2)
    
    def consolidate(self):
        print("=" * 60)
        print("RECIPE CONSOLIDATION PROCESS")
        print("=" * 60)
        
        print("\n1. Loading individual recipe files...")
        self.load_individual_recipes()
        print(f"   Loaded {len(self.recipes_list)} recipes")
        
        print("\n2. Calculating totals for each recipe...")
        self.calculate_totals()
        
        print("\n3. Generating output CSVs...")
        recipes_df, recipe_ingredient_df = self._generate_output_dfs()
        
        self._print_validation_report()
        
        return recipes_df, recipe_ingredient_df
    
    def _generate_output_dfs(self):
        recipes_data = []
        recipe_ingredients_data = []
        
        for rid, recipe in enumerate(self.recipes_list, start=1):
            recipes_data.append({
                'RID': rid,
                'Name': recipe['name'],
                'type': recipe['type'],
                'Category': recipe['category'],
                'total_price': recipe.get('total_price', 0),
                'provided_calories': recipe.get('provided_calories', 0),
                'provided_protein': recipe.get('provided_protein', 0),
                'provided_fat': recipe.get('provided_fat', 0),
                'provided_carbs': recipe.get('provided_carbs', 0)
            })
            
            for ingredient in recipe['ingredients']:
                recipe_ingredients_data.append({
                    'PID': ingredient['PID'],
                    'RID': rid,
                    'Quantity': ingredient['quantity']
                })
        
        recipes_df = pd.DataFrame(recipes_data)
        recipe_ingredients_df = pd.DataFrame(recipe_ingredients_data)
        
        return recipes_df, recipe_ingredients_df
    
    def _print_validation_report(self):
        print("\n4. Validation Report:")
        print(f"   ✓ Recipes consolidated: {len(self.recipes_list)}")
        print(f"   ⚠ Warnings: {len(self.validation_warnings)}")
        print(f"   ✗ Errors: {len(self.validation_errors)}")
        
        if self.validation_warnings:
            print("\n   Warnings:")
            for warning in self.validation_warnings[:10]:
                print(f"   - {warning}")
            if len(self.validation_warnings) > 10:
                print(f"   ... and {len(self.validation_warnings) - 10} more")
        
        if self.validation_errors:
            print("\n   Errors:")
            for error in self.validation_errors:
                print(f"   - {error}")
    
    def export_csv(self, recipes_df, recipe_ingredients_df, 
                   recipes_output="data/recipes.csv",
                   ingredients_output="data/recipe_ingredient.csv"):
        recipes_df.to_csv(recipes_output, index=False, encoding='utf-8-sig')
        recipe_ingredients_df.to_csv(ingredients_output, index=False, encoding='utf-8-sig')
        
        print(f"\n5. Export Complete:")
        print(f"   ✓ {recipes_output} ({len(recipes_df)} recipes)")
        print(f"   ✓ {ingredients_output} ({len(recipe_ingredients_df)} items)")


def run_consolidation(products_csv="data/products.csv", 
                     recipes_input_dir="data/recipes_input"):
                     
    consolidator = RecipeConsolidator(products_csv, recipes_input_dir)
    recipes_df, recipe_ingredients_df = consolidator.consolidate()
    consolidator.export_csv(recipes_df, recipe_ingredients_df)
    
    return recipes_df, recipe_ingredients_df
