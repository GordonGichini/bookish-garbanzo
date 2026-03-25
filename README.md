# bookish-garbanzo
# Recipe Manager & Meal Planner

A Python desktop application that helps users store recipes, plan weekly meals, and automatically generate shopping lists — built with a clean graphical interface using **tkinter**.

> **FC308 – Programming Assignment Part 2**  
> Module: Information Technology | Submission: 7th April 2026

---

## Features

- **Secure login & registration** — passwords stored as SHA-256 hashes
- **Recipe management** — add, view, edit, and delete recipes with ingredients and preparation steps
- **Live search** — filter recipes by name or ingredient as you type
- **Weekly meal planner** — assign saved recipes to each day of the week via dropdown menus
- **Auto shopping list** — ingredients from your meal plan combined automatically, with ×2, ×3 multipliers for repeated items
- **Persistent storage** — all data saved locally in JSON files, available every time you open the app
- **Multi-user support** — each user has their own private recipe collection and meal plan

---

## Requirements

| Requirement | Detail |
|-------------|--------|
| Python | Version 3.6 or higher |
| tkinter | Included with Python (no extra install needed) |
| Operating System | Windows, macOS, or Linux |

> **tkinter is bundled with Python on Windows and macOS.**  
> On Linux it may need a separate install — see [Troubleshooting](#troubleshooting) below.

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Run the program

```bash
python ui.py
```

On some systems use `python3`:

```bash
python3 ui.py
```

No pip installs, no virtual environments, no dependencies beyond the Python standard library.

---

## File Structure

```
├── recipe_manager_gui.py   ← Main application — run this file
├── users.json              ← Created automatically on first registration
├── recipes.json            ← Created automatically when you add a recipe
├── meal_plan.json          ← Created automatically when you save a plan
└── README.md
```

> The three `.json` files are created automatically the first time you use each feature. You do not need to create them manually.

---

## How to Use

### Registering and Logging In
1. Launch the app — the login screen appears
2. Click **Register** to create a new account
3. Enter a username and a password (minimum 4 characters)
4. Switch back to **Log In** and enter your credentials

### Managing Recipes
1. Navigate to **Recipes** in the sidebar
2. Click **+ Add Recipe** to open the add dialog
3. Enter the recipe name, ingredients (one per line), and preparation steps (one per line)
4. Click **Save Recipe**
5. Select any recipe in the list to view its full details
6. Use the **Edit** or **Delete** buttons in the detail panel to update or remove it

### Searching Recipes
- Type any keyword or ingredient name into the search box — the list filters instantly as you type

### Planning Your Week
1. Navigate to **Meal Planner**
2. Use the dropdown on each day to select a saved recipe (or `-- None --` to leave a day empty)
3. Click **Save Plan** when done

### Generating a Shopping List
1. Navigate to **Shopping List**
2. Your list is generated automatically from the saved meal plan
3. Ingredients used more than once show a multiplier (e.g. ×2)

---

## Troubleshooting

### tkinter not found (Linux)

If you see `ModuleNotFoundError: No module named 'tkinter'`, install it with:

```bash
# Ubuntu / Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

### `python` not recognised (Windows)

Try using `py` instead:

```bash
py recipe_manager_gui.py
```

Or ensure Python is added to your system PATH when installing.

---

## Data & Privacy

- All data is stored **locally** on your machine in JSON files
- Passwords are **never stored in plain text** — hashed with SHA-256 before saving
- No data is sent over the internet

---

## Built With

| Technology | Purpose |
|------------|---------|
| Python 3 | Core programming language |
| tkinter | GUI framework (Python standard library) |
| json | Data storage and retrieval |
| hashlib | SHA-256 password hashing |
| os | File path checks |

---

## Author

** **  
FC308 – Information Technology  
