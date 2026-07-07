# 🇩🇿 Nutri Mlih

An AI-powered meal planning system built around **real Algerian grocery market data**. The project scrapes product prices from local market websites, builds a nutrition-mapped product database, links it to a curated recipe dataset, and then uses **four different search/optimization algorithms** (Genetic Algorithm, A\*, Greedy Best-First, and CSP) to generate 7–30 day meal plans that satisfy a user's **budget**, **calorie (TDEE)**, and **macronutrient** goals.

---

## 📌 Project Overview

The pipeline is organized into four major stages, all contained in `main.ipynb`:

1. **Data Scraping & Pre-Processing** — Collects real product prices, names, and categories from two Algerian market websites.
2. **Nutritional Enrichment** — Maps each product to a standardized nutritional profile (calories, protein, fat, carbs, sugar, fiber, sodium), normalized per 100 g / 100 ml.
3. **Recipe Consolidation** — Builds a recipe database where each recipe is linked to real products via Product IDs (PIDs) and quantities, then aggregates cost and nutrition per recipe.
4. **Meal Plan Optimization** — Frames "generate an N-day meal plan" as a search/optimization problem and solves it four different ways for comparison:
   - **Genetic Algorithm** (population-based, exhaustive pairwise crossover + mutation)
   - **A\*** (informed graph search with cost + heuristic)
   - **Greedy Best-First Search** (heuristic-only, faster/less precise)
   - **Constraint Satisfaction Problem (CSP)** with AC-3 arc-consistency pruning + backtracking

Each approach is benchmarked and visualized in terms of **cost**, **calories**, **macronutrient distribution**, and **meal variety**.

---

## 🗂️ Data Pipeline

### 1. Scraping
- `modules/data_collection` scrapes two market sources into:
  - `data/products1.csv`
  - `data/products2.csv`

### 2. Cleaning & Standardization
- Duplicate removal (handles duplicate mobile/desktop scraped entries)
- Price normalization to numeric floats (including imputing interval prices, e.g. `"50-70"`, by their mean)
- Regex-based **quantity extraction** from product names (grams, kilograms, milliliters, centiliters, liters) with category-specific rules (e.g., produce defaults to per-kg)
- Manual correction pass (`data/products_manually_modified.csv`) for products where quantity couldn't be parsed automatically, plus manually added items (fish, honey, prepared meals, etc.)

### 3. Nutritional Mapping
- `data/nutrition_data.py` provides `NUTRITION_DB` and `PRODUCE_NAME_MAP`
- A rule-based classifier (`map_product_to_key`) matches each product name/category to a nutrition key (oils, dairy, legumes, spices, condiments, drinks, etc.)
- Missing nutritional values are imputed using the category mean
- Final output: `data/products.csv` — the consolidated, nutrition-enriched product catalog with a unique `PID`

### 4. Recipe Dataset
- Recipes are authored manually using a standardized CSV template referencing product `PID`s and quantities:
  ```
  Name,Type,Category,PIDs,Quantities
  Breakfast Omelette,Breakfast,Vegetarian,"3;191;200;162;152","3;100 g;50 g;15 ml;1 g"
  ```
- Contributor recipe files live in `data/recipes_input/`
- `modules/recipe_consolidation.run_consolidation()` merges all contributor files, resolves PIDs against `products.csv`, and computes each recipe's total price and nutritional totals
- Output: `recipes.csv` and `recipe_ingredient.csv`

### 5. Transition Model
A dictionary-based lookup structure mapping `meal_type → recipe_name → (category, price, calories, protein, carbs, fat)`, used as the shared "world model" for every search algorithm below.

---

## 🧠 Meal Planning Algorithms

All four algorithms solve variations of the same problem: **choose Breakfast/Lunch/Dinner for each day such that total cost stays within budget, total calories stay within ±10% of TDEE × days, and macronutrient ratios follow the user's goal** (`maintain`, `gain`, or `loss`).

| Algorithm | Strategy | Notes |
|---|---|---|
| **Genetic Algorithm** | Population of 80 random 30-day plans → keep top 20 → exhaustive pairwise crossover + mutation over up to 200 generations | Fitness = weighted sum of cost, calorie, macro, and diversity penalties; early exit above a fitness threshold |
| **A\*** | `f(n) = g(n) + h(n)` over a priority-queue frontier | Cost-aware; goal requires calories within ±10% of TDEE |
| **Greedy Best-First** | `f(n) = h(n)` only | Faster, ignores accumulated cost, less nutritionally precise |
| **CSP** | Domain pruning (per-slot calorie/budget caps) + **AC-3** arc-consistency + day-by-day backtracking | Cheapest search since infeasible options are eliminated before backtracking begins |

Diversity is enforced across all approaches so the same meal isn't repeated more than twice within any 7-day window (with periodic resets to allow long-term repetition).

---

## 📊 Visualizations

The notebook generates comparative plots at every stage, including:
- Price distribution (overall and per category) via boxplots
- Product count and average calories per category
- Macronutrient distribution pie charts (Protein / Fat / Carbs) per algorithm
- Cost vs. nutrition-error trade-off scatter plots across budget ranges
- Variety-score comparison between the Genetic Algorithm and Greedy Search over 30-day plans

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Data handling:** `pandas`, `numpy`
- **Visualization:** `matplotlib`
- **Text processing:** `re` (regex-based quantity/keyword extraction)
- **Search & Optimization:** custom-built
  - Genetic Algorithm (custom crossover/mutation)
  - A* / Greedy Best-First Search (`queue.PriorityQueue`)
  - CSP with AC-3 arc-consistency
- **Web scraping:** custom scraper module (`modules/data_collection`)
- **Notebook environment:** Jupyter Notebook (`main.ipynb`)
