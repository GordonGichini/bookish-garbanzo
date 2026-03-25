"""
============================================================
  Recipe Manager & Meal Planner
  FC308 - Programming Assignment Part 2
  Author: [Student Name]
============================================================
"""

import json
import os
import hashlib

# ─────────────────────────────────────────────
#  FILE PATHS  (all data stored as JSON files)
# ─────────────────────────────────────────────
USERS_FILE    = "users.json"
RECIPES_FILE  = "recipes.json"
PLAN_FILE     = "meal_plan.json"

DAYS_OF_WEEK  = ["Monday", "Tuesday", "Wednesday",
                 "Thursday", "Friday", "Saturday", "Sunday"]


# ══════════════════════════════════════════════
#  FILE I/O HELPERS
# ══════════════════════════════════════════════

def load_json(filepath):
    """Load data from a JSON file. Returns empty dict if file does not exist."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}


def save_json(filepath, data):
    """Save data to a JSON file with readable indentation."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


# ══════════════════════════════════════════════
#  AUTHENTICATION
# ══════════════════════════════════════════════

def hash_password(password):
    """Return a SHA-256 hash of the given password string."""
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    """Register a new user. Checks for duplicate usernames."""
    print("\n── Register ──")
    users = load_json(USERS_FILE)

    username = input("Choose a username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None

    if username in users:
        print("That username is already taken. Please try a different one.")
        return None

    password = input("Choose a password: ").strip()
    if len(password) < 4:
        print("Password must be at least 4 characters.")
        return None

    users[username] = hash_password(password)
    save_json(USERS_FILE, users)
    print(f"Account created for '{username}'. You can now log in.")
    return None


def login():
    """
    Prompt for username and password.
    Returns the username string on success, or None on failure.
    """
    print("\n── Log In ──")
    users = load_json(USERS_FILE)

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username in users and users[username] == hash_password(password):
        print(f"Welcome back, {username}!")
        return username

    print("Incorrect username or password.")
    return None


# ══════════════════════════════════════════════
#  RECIPE MANAGEMENT
# ══════════════════════════════════════════════

def get_user_recipes(username):
    """Return the recipe dictionary for a specific user."""
    all_recipes = load_json(RECIPES_FILE)
    return all_recipes.get(username, {})


def save_user_recipes(username, recipes):
    """Save the recipe dictionary back to file for the given user."""
    all_recipes = load_json(RECIPES_FILE)
    all_recipes[username] = recipes
    save_json(RECIPES_FILE, all_recipes)


def add_recipe(username):
    """
    Guide the user through entering a new recipe:
    name, list of ingredients, and step-by-step preparation instructions.
    """
    print("\n── Add New Recipe ──")
    recipes = get_user_recipes(username)

    name = input("Recipe name: ").strip().title()
    if not name:
        print("Recipe name cannot be empty.")
        return

    if name in recipes:
        print(f"A recipe named '{name}' already exists. Use Edit to update it.")
        return

    print("Enter ingredients (type 'done' when finished):")
    ingredients = []
    while True:
        item = input("  Ingredient: ").strip()
        if item.lower() == "done":
            break
        if item:
            ingredients.append(item)

    if not ingredients:
        print("A recipe must have at least one ingredient.")
        return

    print("Enter preparation steps (type 'done' when finished):")
    steps = []
    step_num = 1
    while True:
        step = input(f"  Step {step_num}: ").strip()
        if step.lower() == "done":
            break
        if step:
            steps.append(step)
            step_num += 1

    if not steps:
        print("A recipe must have at least one step.")
        return

    recipes[name] = {
        "ingredients": ingredients,
        "steps": steps
    }
    save_user_recipes(username, recipes)
    print(f"Recipe '{name}' saved successfully.")


def view_recipes(username):
    """Display all stored recipes for the current user."""
    print("\n── Your Recipes ──")
    recipes = get_user_recipes(username)

    if not recipes:
        print("No recipes saved yet. Use 'Add Recipe' to get started.")
        return

    for i, name in enumerate(recipes, start=1):
        print(f"\n  [{i}] {name}")
        print("      Ingredients:")
        for ing in recipes[name]["ingredients"]:
            print(f"        - {ing}")
        print("      Preparation:")
        for j, step in enumerate(recipes[name]["steps"], start=1):
            print(f"        {j}. {step}")


def search_recipes(username):
    """
    Search recipes by keyword.
    Matches against recipe name AND ingredients.
    """
    print("\n── Search Recipes ──")
    recipes = get_user_recipes(username)

    if not recipes:
        print("No recipes saved yet.")
        return

    keyword = input("Enter a keyword or ingredient to search: ").strip().lower()
    if not keyword:
        print("Search term cannot be empty.")
        return

    results = {}
    for name, data in recipes.items():
        # Check name
        if keyword in name.lower():
            results[name] = data
            continue
        # Check ingredients
        for ing in data["ingredients"]:
            if keyword in ing.lower():
                results[name] = data
                break

    if not results:
        print(f"No recipes found matching '{keyword}'.")
        return

    print(f"\nFound {len(results)} result(s):")
    for name, data in results.items():
        print(f"\n  {name}")
        print("    Ingredients: " + ", ".join(data["ingredients"]))


def edit_recipe(username):
    """Allow the user to update the ingredients or steps of an existing recipe."""
    print("\n── Edit Recipe ──")
    recipes = get_user_recipes(username)

    if not recipes:
        print("No recipes to edit.")
        return

    print("Available recipes:")
    names = list(recipes.keys())
    for i, n in enumerate(names, 1):
        print(f"  [{i}] {n}")

    choice = input("Enter the number of the recipe to edit: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(names)):
        print("Invalid selection.")
        return

    name = names[int(choice) - 1]
    print(f"\nEditing '{name}'. Press Enter to keep existing values.")

    # Edit ingredients
    print(f"Current ingredients: {', '.join(recipes[name]['ingredients'])}")
    update_ing = input("Re-enter all ingredients? (yes/no): ").strip().lower()
    if update_ing == "yes":
        print("Enter new ingredients (type 'done' when finished):")
        new_ingredients = []
        while True:
            item = input("  Ingredient: ").strip()
            if item.lower() == "done":
                break
            if item:
                new_ingredients.append(item)
        if new_ingredients:
            recipes[name]["ingredients"] = new_ingredients

    # Edit steps
    print(f"Current steps: {len(recipes[name]['steps'])} step(s)")
    update_steps = input("Re-enter all steps? (yes/no): ").strip().lower()
    if update_steps == "yes":
        print("Enter new steps (type 'done' when finished):")
        new_steps = []
        step_num = 1
        while True:
            step = input(f"  Step {step_num}: ").strip()
            if step.lower() == "done":
                break
            if step:
                new_steps.append(step)
                step_num += 1
        if new_steps:
            recipes[name]["steps"] = new_steps

    save_user_recipes(username, recipes)
    print(f"Recipe '{name}' updated.")


def delete_recipe(username):
    """Delete a recipe after asking for confirmation."""
    print("\n── Delete Recipe ──")
    recipes = get_user_recipes(username)

    if not recipes:
        print("No recipes to delete.")
        return

    names = list(recipes.keys())
    for i, n in enumerate(names, 1):
        print(f"  [{i}] {n}")

    choice = input("Enter the number of the recipe to delete: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(names)):
        print("Invalid selection.")
        return

    name = names[int(choice) - 1]
    confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        del recipes[name]
        save_user_recipes(username, recipes)
        # Remove from meal plan too if it was assigned
        _remove_recipe_from_plan(username, name)
        print(f"Recipe '{name}' deleted.")
    else:
        print("Deletion cancelled.")


def _remove_recipe_from_plan(username, recipe_name):
    """Internal helper: remove a deleted recipe from the user's meal plan."""
    all_plans = load_json(PLAN_FILE)
    plan = all_plans.get(username, {})
    updated = False
    for day, assigned in plan.items():
        if assigned == recipe_name:
            plan[day] = None
            updated = True
    if updated:
        all_plans[username] = plan
        save_json(PLAN_FILE, all_plans)


# ══════════════════════════════════════════════
#  MEAL PLANNING
# ══════════════════════════════════════════════

def get_user_plan(username):
    """Return the current weekly meal plan for a user."""
    all_plans = load_json(PLAN_FILE)
    # Initialise with None for each day if not set
    plan = all_plans.get(username, {day: None for day in DAYS_OF_WEEK})
    return plan


def save_user_plan(username, plan):
    """Save the updated meal plan to file."""
    all_plans = load_json(PLAN_FILE)
    all_plans[username] = plan
    save_json(PLAN_FILE, all_plans)


def plan_meals(username):
    """
    Let the user assign a saved recipe to each day of the week.
    Days can also be cleared (set to None).
    """
    print("\n── Plan Your Week ──")
    recipes = get_user_recipes(username)

    if not recipes:
        print("You have no saved recipes to plan with. Add some recipes first.")
        return

    plan = get_user_plan(username)
    recipe_names = list(recipes.keys())

    print("\nCurrent plan:")
    for day in DAYS_OF_WEEK:
        assigned = plan.get(day) or "Not set"
        print(f"  {day:<12}: {assigned}")

    print("\nAssign meals day by day (press Enter to skip a day):")
    for day in DAYS_OF_WEEK:
        print(f"\n  {day}")
        print("  Available recipes:")
        for i, rname in enumerate(recipe_names, 1):
            print(f"    [{i}] {rname}")
        print("    [0] Clear this day")

        choice = input(f"  Choose for {day}: ").strip()
        if choice == "":
            continue  # keep existing
        elif choice == "0":
            plan[day] = None
        elif choice.isdigit() and 1 <= int(choice) <= len(recipe_names):
            plan[day] = recipe_names[int(choice) - 1]
        else:
            print("  Invalid choice — day unchanged.")

    save_user_plan(username, plan)
    print("\nMeal plan saved!")


def view_meal_plan(username):
    """Display the full weekly meal plan."""
    print("\n── Weekly Meal Plan ──")
    plan = get_user_plan(username)

    for day in DAYS_OF_WEEK:
        assigned = plan.get(day) or "—"
        print(f"  {day:<12}: {assigned}")


# ══════════════════════════════════════════════
#  SHOPPING LIST
# ══════════════════════════════════════════════

def generate_shopping_list(username):
    """
    Build a shopping list by collecting all ingredients from
    recipes assigned in the current meal plan.
    Combines duplicate ingredients and shows total count.
    """
    print("\n── Shopping List ──")
    plan   = get_user_plan(username)
    recipes = get_user_recipes(username)

    # Aggregate ingredients
    shopping = {}
    for day in DAYS_OF_WEEK:
        recipe_name = plan.get(day)
        if recipe_name and recipe_name in recipes:
            for ingredient in recipes[recipe_name]["ingredients"]:
                # Normalise to lowercase for grouping
                key = ingredient.lower().strip()
                shopping[key] = shopping.get(key, 0) + 1

    if not shopping:
        print("Your meal plan is empty. Plan some meals first.")
        return

    print("\nIngredients needed for the week:")
    for item, count in sorted(shopping.items()):
        if count > 1:
            print(f"  - {item.capitalize()} (×{count})")
        else:
            print(f"  - {item.capitalize()}")

    print(f"\nTotal unique ingredients: {len(shopping)}")


# ══════════════════════════════════════════════
#  MENU SYSTEM
# ══════════════════════════════════════════════

def recipe_menu(username):
    """Sub-menu for all recipe-related operations."""
    while True:
        print("\n══ Recipe Manager ══")
        print("  [1] View all recipes")
        print("  [2] Add a recipe")
        print("  [3] Search recipes")
        print("  [4] Edit a recipe")
        print("  [5] Delete a recipe")
        print("  [0] Back to main menu")

        choice = input("Choose an option: ").strip()
        if   choice == "1": view_recipes(username)
        elif choice == "2": add_recipe(username)
        elif choice == "3": search_recipes(username)
        elif choice == "4": edit_recipe(username)
        elif choice == "5": delete_recipe(username)
        elif choice == "0": break
        else: print("Invalid option. Please try again.")


def main_menu(username):
    """Main application menu shown after a successful login."""
    while True:
        print(f"\n══ Main Menu  [{username}] ══")
        print("  [1] Recipes")
        print("  [2] Plan my week")
        print("  [3] View meal plan")
        print("  [4] Generate shopping list")
        print("  [0] Log out")

        choice = input("Choose an option: ").strip()
        if   choice == "1": recipe_menu(username)
        elif choice == "2": plan_meals(username)
        elif choice == "3": view_meal_plan(username)
        elif choice == "4": generate_shopping_list(username)
        elif choice == "0":
            print("Logged out. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


def auth_menu():
    """Entry-point menu: login or register before accessing the app."""
    print("╔══════════════════════════════════╗")
    print("║   Recipe Manager & Meal Planner  ║")
    print("╚══════════════════════════════════╝")

    while True:
        print("\n  [1] Log in")
        print("  [2] Register")
        print("  [0] Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            user = login()
            if user:
                main_menu(user)
        elif choice == "2":
            register()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════

if __name__ == "__main__":
    auth_menu()