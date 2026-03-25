"""
============================================================
  Recipe Manager & Meal Planner  –  GUI Version
  FC308 - Programming Assignment Part 2
  Built with Python tkinter (standard library)
  Author: 
============================================================
"""

import json
import os
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# ─────────────────────────────────────────────
#  FILE PATHS
# ─────────────────────────────────────────────
USERS_FILE   = "users.json"
RECIPES_FILE = "recipes.json"
PLAN_FILE    = "meal_plan.json"

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]

# ─────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────
BG          = "#F7F9FC"
SIDEBAR_BG  = "#1E2D40"
CARD_BG     = "#FFFFFF"
ACCENT      = "#3A86FF"
ACCENT_DARK = "#2667CC"
SUCCESS     = "#06D6A0"
DANGER      = "#EF476F"
TEXT_DARK   = "#1A1A2E"
TEXT_LIGHT  = "#FFFFFF"
TEXT_MUTED  = "#8A9BB0"
BORDER      = "#DEE6F0"
HEADER_BG   = "#253547"

FONT_BODY   = ("Segoe UI", 11)
FONT_BOLD   = ("Segoe UI", 11, "bold")
FONT_TITLE  = ("Segoe UI", 16, "bold")
FONT_SMALL  = ("Segoe UI", 9)
FONT_H2     = ("Segoe UI", 13, "bold")


# ══════════════════════════════════════════════
#  FILE I/O
# ══════════════════════════════════════════════

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_recipes(username):
    return load_json(RECIPES_FILE).get(username, {})

def save_user_recipes(username, recipes):
    all_r = load_json(RECIPES_FILE)
    all_r[username] = recipes
    save_json(RECIPES_FILE, all_r)

def get_user_plan(username):
    all_p = load_json(PLAN_FILE)
    return all_p.get(username, {day: None for day in DAYS_OF_WEEK})

def save_user_plan(username, plan):
    all_p = load_json(PLAN_FILE)
    all_p[username] = plan
    save_json(PLAN_FILE, all_p)


# ══════════════════════════════════════════════
#  REUSABLE UI HELPERS
# ══════════════════════════════════════════════

def styled_button(parent, text, command, color=ACCENT, fg=TEXT_LIGHT,
                  width=14, font=FONT_BOLD, pady=6):
    """Flat coloured button with hover effect."""
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg=fg, activebackground=color,
        activeforeground=fg, relief="flat", cursor="hand2",
        font=font, width=width, pady=pady, bd=0
    )
    def on_enter(e): btn.config(bg=_darken(color))
    def on_leave(e): btn.config(bg=color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def _darken(hex_color):
    """Return a slightly darker version of a hex colour."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = max(0, r-25), max(0, g-25), max(0, b-25)
    return f"#{r:02x}{g:02x}{b:02x}"

def card_frame(parent, **kwargs):
    """White rounded-looking card frame."""
    f = tk.Frame(parent, bg=CARD_BG, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1,
                 **kwargs)
    return f

def section_label(parent, text):
    return tk.Label(parent, text=text, font=FONT_H2,
                    bg=CARD_BG, fg=TEXT_DARK)

def muted_label(parent, text):
    return tk.Label(parent, text=text, font=FONT_SMALL,
                    bg=CARD_BG, fg=TEXT_MUTED)

def form_row(parent, label_text, bg=CARD_BG, show=None):
    """Label + Entry pair. Returns the Entry widget."""
    tk.Label(parent, text=label_text, font=FONT_BOLD,
             bg=bg, fg=TEXT_DARK, anchor="w").pack(fill="x", padx=24, pady=(10, 2))
    entry = tk.Entry(parent, font=FONT_BODY, bg=BG,
                     relief="flat", bd=0,
                     highlightbackground=BORDER, highlightthickness=1,
                     show=show or "")
    entry.pack(fill="x", padx=24, ipady=6)
    return entry

def divider(parent, bg=CARD_BG):
    tk.Frame(parent, height=1, bg=BORDER).pack(fill="x", padx=24, pady=8)


# ══════════════════════════════════════════════
#  AUTH WINDOW  (Login / Register)
# ══════════════════════════════════════════════

class AuthWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Recipe Manager – Login")
        self.root.geometry("420x560")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._center_window(420, 560)
        self._build_ui()

    def _center_window(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # Header banner
        header = tk.Frame(self.root, bg=SIDEBAR_BG, height=130)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🍽️", font=("Segoe UI Emoji", 32),
                 bg=SIDEBAR_BG, fg=TEXT_LIGHT).pack(pady=(20, 4))
        tk.Label(header, text="Recipe Manager", font=FONT_TITLE,
                 bg=SIDEBAR_BG, fg=TEXT_LIGHT).pack()

        # Card
        card = card_frame(self.root, padx=0, pady=0)
        card.pack(fill="both", expand=True, padx=32, pady=24)

        # Tab row
        tab_bar = tk.Frame(card, bg=CARD_BG)
        tab_bar.pack(fill="x", padx=24, pady=(16, 0))

        self.mode = tk.StringVar(value="login")
        self.login_btn  = tk.Button(tab_bar, text="Log In",  font=FONT_BOLD,
                                    bg=ACCENT, fg=TEXT_LIGHT, relief="flat",
                                    cursor="hand2", command=self._show_login, width=10, pady=5)
        self.reg_btn    = tk.Button(tab_bar, text="Register", font=FONT_BOLD,
                                    bg=CARD_BG, fg=TEXT_MUTED, relief="flat",
                                    cursor="hand2", command=self._show_register, width=10, pady=5)
        self.login_btn.pack(side="left", padx=(0, 6))
        self.reg_btn.pack(side="left")

        divider(card)
        self.form_container = tk.Frame(card, bg=CARD_BG)
        self.form_container.pack(fill="both", expand=True)
        self._show_login()

    def _clear_form(self):
        for w in self.form_container.winfo_children():
            w.destroy()

    def _show_login(self):
        self._clear_form()
        self.login_btn.config(bg=ACCENT, fg=TEXT_LIGHT)
        self.reg_btn.config(bg=CARD_BG, fg=TEXT_MUTED)

        self.lu = form_row(self.form_container, "Username")
        self.lp = form_row(self.form_container, "Password", show="•")

        self.msg_var = tk.StringVar()
        tk.Label(self.form_container, textvariable=self.msg_var,
                 font=FONT_SMALL, bg=CARD_BG, fg=DANGER).pack(pady=4)

        styled_button(self.form_container, "Log In",
                      self._do_login, width=18).pack(pady=8)
        self.lu.bind("<Return>", lambda e: self._do_login())
        self.lp.bind("<Return>", lambda e: self._do_login())

    def _show_register(self):
        self._clear_form()
        self.login_btn.config(bg=CARD_BG, fg=TEXT_MUTED)
        self.reg_btn.config(bg=ACCENT, fg=TEXT_LIGHT)

        self.ru = form_row(self.form_container, "Choose a username")
        self.rp = form_row(self.form_container, "Choose a password", show="•")
        self.rp2 = form_row(self.form_container, "Confirm password", show="•")

        self.msg_var = tk.StringVar()
        tk.Label(self.form_container, textvariable=self.msg_var,
                 font=FONT_SMALL, bg=CARD_BG, fg=DANGER).pack(pady=4)

        styled_button(self.form_container, "Create Account",
                      self._do_register, width=18).pack(pady=8)

    def _do_login(self):
        users = load_json(USERS_FILE)
        u = self.lu.get().strip()
        p = self.lp.get().strip()
        if u in users and users[u] == hash_password(p):
            self.root.destroy()
            self.on_success(u)
        else:
            self.msg_var.set("Incorrect username or password.")

    def _do_register(self):
        users = load_json(USERS_FILE)
        u  = self.ru.get().strip()
        p  = self.rp.get().strip()
        p2 = self.rp2.get().strip()
        if not u:
            self.msg_var.set("Username cannot be empty.")
        elif u in users:
            self.msg_var.set("Username already taken.")
        elif len(p) < 4:
            self.msg_var.set("Password must be at least 4 characters.")
        elif p != p2:
            self.msg_var.set("Passwords do not match.")
        else:
            users[u] = hash_password(p)
            save_json(USERS_FILE, users)
            messagebox.showinfo("Success", f"Account created! You can now log in.")
            self._show_login()


# ══════════════════════════════════════════════
#  MAIN APP WINDOW
# ══════════════════════════════════════════════

class AppWindow:
    def __init__(self, root, username):
        self.root     = root
        self.username = username
        self.root.title("Recipe Manager & Meal Planner")
        self.root.geometry("1050x680")
        self.root.configure(bg=BG)
        self.root.minsize(900, 600)
        self._center_window(1050, 680)
        self._build_layout()
        self._show_recipes()

    def _center_window(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ── LAYOUT ──────────────────────────────────────────────────────
    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # App logo area
        logo = tk.Frame(self.sidebar, bg=HEADER_BG, height=70)
        logo.pack(fill="x")
        logo.pack_propagate(False)
        tk.Label(logo, text="🍽️  Recipe Manager", font=("Segoe UI", 12, "bold"),
                 bg=HEADER_BG, fg=TEXT_LIGHT).pack(expand=True)

        # User badge
        tk.Label(self.sidebar, text=f"👤  {self.username}",
                 font=FONT_SMALL, bg=SIDEBAR_BG, fg=TEXT_MUTED).pack(pady=(12, 4))

        tk.Frame(self.sidebar, height=1, bg="#2E3F52").pack(fill="x", padx=16, pady=6)

        # Nav buttons
        self.nav_btns = {}
        nav_items = [
            ("📋  Recipes",       self._show_recipes),
            ("🗓️  Meal Planner",  self._show_planner),
            ("🛒  Shopping List", self._show_shopping),
        ]
        for label, cmd in nav_items:
            b = tk.Button(self.sidebar, text=label, font=FONT_BODY,
                          bg=SIDEBAR_BG, fg=TEXT_LIGHT, activebackground=ACCENT,
                          activeforeground=TEXT_LIGHT, relief="flat",
                          anchor="w", padx=20, pady=10, cursor="hand2",
                          command=lambda c=cmd, l=label: self._nav(c, l))
            b.pack(fill="x", pady=1)
            self.nav_btns[label] = b

        # Logout at bottom
        tk.Frame(self.sidebar, bg=SIDEBAR_BG).pack(expand=True)
        styled_button(self.sidebar, "⏻  Log Out", self._logout,
                      color=DANGER, width=16, pady=8).pack(pady=16)

        # Main content area
        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

    def _nav(self, cmd, label):
        for lbl, btn in self.nav_btns.items():
            btn.config(bg=ACCENT if lbl == label else SIDEBAR_BG)
        cmd()

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _logout(self):
        self.root.destroy()
        _launch_auth()

    # ── PAGE HEADER ─────────────────────────────────────────────────
    def _page_header(self, title, subtitle=""):
        bar = tk.Frame(self.content, bg=CARD_BG,
                       highlightbackground=BORDER, highlightthickness=1)
        bar.pack(fill="x")
        tk.Label(bar, text=title, font=FONT_TITLE,
                 bg=CARD_BG, fg=TEXT_DARK).pack(side="left", padx=24, pady=14)
        if subtitle:
            tk.Label(bar, text=subtitle, font=FONT_SMALL,
                     bg=CARD_BG, fg=TEXT_MUTED).pack(side="left", pady=14)

    # ══════════════════════════════════════════
    #  RECIPES PAGE
    # ══════════════════════════════════════════

    def _show_recipes(self):
        self._clear_content()
        self._page_header("📋  Recipes", "  Manage your recipe collection")
        self._nav_highlight("📋  Recipes")

        # Toolbar
        toolbar = tk.Frame(self.content, bg=BG)
        toolbar.pack(fill="x", padx=20, pady=(12, 6))

        styled_button(toolbar, "+ Add Recipe", self._open_add_recipe,
                      color=SUCCESS, width=14).pack(side="left")

        # Search box
        tk.Label(toolbar, text="🔍", font=FONT_BODY,
                 bg=BG, fg=TEXT_MUTED).pack(side="right")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._refresh_recipe_list())
        search_entry = tk.Entry(toolbar, textvariable=self.search_var,
                                font=FONT_BODY, bg=CARD_BG, relief="flat",
                                highlightbackground=BORDER, highlightthickness=1,
                                width=20)
        search_entry.pack(side="right", ipady=5, padx=(0, 6))
        tk.Label(toolbar, text="Search:", font=FONT_BODY,
                 bg=BG, fg=TEXT_DARK).pack(side="right", padx=(0, 4))

        # Split pane
        pane = tk.Frame(self.content, bg=BG)
        pane.pack(fill="both", expand=True, padx=20, pady=8)

        # Left: recipe list
        list_card = card_frame(pane)
        list_card.pack(side="left", fill="both", expand=False,
                       ipadx=4, ipady=4)
        list_card.config(width=280)

        tk.Label(list_card, text="Your Recipes", font=FONT_BOLD,
                 bg=CARD_BG, fg=TEXT_DARK).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Frame(list_card, height=1, bg=BORDER).pack(fill="x", padx=16)

        self.recipe_listbox = tk.Listbox(list_card, font=FONT_BODY,
                                          bg=CARD_BG, fg=TEXT_DARK,
                                          selectbackground=ACCENT,
                                          selectforeground=TEXT_LIGHT,
                                          activestyle="none",
                                          relief="flat", bd=0,
                                          highlightthickness=0,
                                          width=30)
        self.recipe_listbox.pack(fill="both", expand=True, padx=8, pady=8)
        self.recipe_listbox.bind("<<ListboxSelect>>", self._on_recipe_select)

        # Right: detail panel
        self.detail_card = card_frame(pane)
        self.detail_card.pack(side="left", fill="both", expand=True,
                              padx=(12, 0), ipadx=8, ipady=8)

        self._refresh_recipe_list()
        self._show_recipe_placeholder()

    def _nav_highlight(self, label):
        for lbl, btn in self.nav_btns.items():
            btn.config(bg=ACCENT if lbl == label else SIDEBAR_BG)

    def _refresh_recipe_list(self):
        keyword = self.search_var.get().lower() if hasattr(self, "search_var") else ""
        self.recipe_listbox.delete(0, "end")
        recipes = get_user_recipes(self.username)
        self._recipe_names = []
        for name, data in recipes.items():
            match = (keyword in name.lower() or
                     any(keyword in ing.lower() for ing in data["ingredients"]))
            if not keyword or match:
                self.recipe_listbox.insert("end", f"  {name}")
                self._recipe_names.append(name)

    def _show_recipe_placeholder(self):
        for w in self.detail_card.winfo_children():
            w.destroy()
        tk.Label(self.detail_card,
                 text="Select a recipe to view details",
                 font=FONT_BODY, bg=CARD_BG, fg=TEXT_MUTED).pack(expand=True)

    def _on_recipe_select(self, event):
        sel = self.recipe_listbox.curselection()
        if not sel:
            return
        name = self._recipe_names[sel[0]]
        recipes = get_user_recipes(self.username)
        data = recipes.get(name, {})
        self._show_recipe_detail(name, data)

    def _show_recipe_detail(self, name, data):
        for w in self.detail_card.winfo_children():
            w.destroy()

        # Title + action buttons
        top = tk.Frame(self.detail_card, bg=CARD_BG)
        top.pack(fill="x", padx=16, pady=(14, 0))
        tk.Label(top, text=name, font=FONT_TITLE,
                 bg=CARD_BG, fg=TEXT_DARK).pack(side="left")
        styled_button(top, "✏️ Edit", lambda: self._open_edit_recipe(name),
                      color=ACCENT, width=9, pady=4).pack(side="right", padx=(6, 0))
        styled_button(top, "🗑 Delete", lambda: self._delete_recipe(name),
                      color=DANGER, width=9, pady=4).pack(side="right")

        divider(self.detail_card)

        # Ingredients
        tk.Label(self.detail_card, text="Ingredients",
                 font=FONT_H2, bg=CARD_BG, fg=TEXT_DARK).pack(anchor="w", padx=16)
        for ing in data.get("ingredients", []):
            tk.Label(self.detail_card, text=f"  •  {ing}",
                     font=FONT_BODY, bg=CARD_BG, fg=TEXT_DARK,
                     anchor="w").pack(fill="x", padx=24)

        tk.Label(self.detail_card, text="",
                 bg=CARD_BG).pack()

        # Steps
        tk.Label(self.detail_card, text="Preparation Steps",
                 font=FONT_H2, bg=CARD_BG, fg=TEXT_DARK).pack(anchor="w", padx=16)
        for i, step in enumerate(data.get("steps", []), 1):
            frame = tk.Frame(self.detail_card, bg=CARD_BG)
            frame.pack(fill="x", padx=16, pady=2)
            tk.Label(frame, text=str(i), font=FONT_BOLD, width=3,
                     bg=ACCENT, fg=TEXT_LIGHT).pack(side="left")
            tk.Label(frame, text=f"  {step}", font=FONT_BODY,
                     bg=CARD_BG, fg=TEXT_DARK, anchor="w",
                     wraplength=480).pack(side="left", fill="x")

    def _delete_recipe(self, name):
        if not messagebox.askyesno("Confirm Delete",
                                   f"Delete '{name}'? This cannot be undone."):
            return
        recipes = get_user_recipes(self.username)
        del recipes[name]
        save_user_recipes(self.username, recipes)
        # Remove from meal plan
        plan = get_user_plan(self.username)
        for day in plan:
            if plan[day] == name:
                plan[day] = None
        save_user_plan(self.username, plan)
        self._refresh_recipe_list()
        self._show_recipe_placeholder()

    # ── ADD RECIPE DIALOG ──────────────────────────────────────────
    def _open_add_recipe(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Recipe")
        dlg.geometry("520x580")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.grab_set()

        tk.Label(dlg, text="Add New Recipe", font=FONT_TITLE,
                 bg=BG, fg=TEXT_DARK).pack(pady=(20, 4))
        tk.Frame(dlg, height=1, bg=BORDER).pack(fill="x", padx=24)

        # Name
        tk.Label(dlg, text="Recipe Name", font=FONT_BOLD,
                 bg=BG, fg=TEXT_DARK, anchor="w").pack(fill="x", padx=24, pady=(12, 2))
        name_entry = tk.Entry(dlg, font=FONT_BODY, bg=CARD_BG, relief="flat",
                              highlightbackground=BORDER, highlightthickness=1)
        name_entry.pack(fill="x", padx=24, ipady=6)

        # Ingredients
        tk.Label(dlg, text="Ingredients (one per line)", font=FONT_BOLD,
                 bg=BG, fg=TEXT_DARK, anchor="w").pack(fill="x", padx=24, pady=(12, 2))
        ing_text = scrolledtext.ScrolledText(dlg, font=FONT_BODY, height=5,
                                             bg=CARD_BG, relief="flat",
                                             highlightbackground=BORDER,
                                             highlightthickness=1, wrap="word")
        ing_text.pack(fill="x", padx=24)

        # Steps
        tk.Label(dlg, text="Preparation Steps (one per line)", font=FONT_BOLD,
                 bg=BG, fg=TEXT_DARK, anchor="w").pack(fill="x", padx=24, pady=(12, 2))
        steps_text = scrolledtext.ScrolledText(dlg, font=FONT_BODY, height=6,
                                               bg=CARD_BG, relief="flat",
                                               highlightbackground=BORDER,
                                               highlightthickness=1, wrap="word")
        steps_text.pack(fill="x", padx=24)

        def save():
            name = name_entry.get().strip().title()
            ingredients = [l.strip() for l in ing_text.get("1.0", "end").splitlines() if l.strip()]
            steps = [l.strip() for l in steps_text.get("1.0", "end").splitlines() if l.strip()]

            if not name:
                messagebox.showerror("Error", "Recipe name cannot be empty.", parent=dlg)
                return
            recipes = get_user_recipes(self.username)
            if name in recipes:
                messagebox.showerror("Error", f"'{name}' already exists.", parent=dlg)
                return
            if not ingredients:
                messagebox.showerror("Error", "Add at least one ingredient.", parent=dlg)
                return
            if not steps:
                messagebox.showerror("Error", "Add at least one step.", parent=dlg)
                return

            recipes[name] = {"ingredients": ingredients, "steps": steps}
            save_user_recipes(self.username, recipes)
            dlg.destroy()
            self._refresh_recipe_list()
            messagebox.showinfo("Saved", f"Recipe '{name}' added!")

        btn_row = tk.Frame(dlg, bg=BG)
        btn_row.pack(pady=16)
        styled_button(btn_row, "Save Recipe", save, color=SUCCESS, width=14).pack(side="left", padx=6)
        styled_button(btn_row, "Cancel", dlg.destroy, color="#8A9BB0", width=10).pack(side="left")

    # ── EDIT RECIPE DIALOG ─────────────────────────────────────────
    def _open_edit_recipe(self, name):
        recipes = get_user_recipes(self.username)
        data = recipes.get(name, {})

        dlg = tk.Toplevel(self.root)
        dlg.title(f"Edit – {name}")
        dlg.geometry("520x580")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.grab_set()

        tk.Label(dlg, text=f"Edit: {name}", font=FONT_TITLE,
                 bg=BG, fg=TEXT_DARK).pack(pady=(20, 4))
        tk.Frame(dlg, height=1, bg=BORDER).pack(fill="x", padx=24)

        tk.Label(dlg, text="Ingredients (one per line)", font=FONT_BOLD,
                 bg=BG, fg=TEXT_DARK, anchor="w").pack(fill="x", padx=24, pady=(12, 2))
        ing_text = scrolledtext.ScrolledText(dlg, font=FONT_BODY, height=6,
                                             bg=CARD_BG, relief="flat",
                                             highlightbackground=BORDER,
                                             highlightthickness=1, wrap="word")
        ing_text.pack(fill="x", padx=24)
        ing_text.insert("1.0", "\n".join(data.get("ingredients", [])))

        tk.Label(dlg, text="Preparation Steps (one per line)", font=FONT_BOLD,
                 bg=BG, fg=TEXT_DARK, anchor="w").pack(fill="x", padx=24, pady=(12, 2))
        steps_text = scrolledtext.ScrolledText(dlg, font=FONT_BODY, height=7,
                                               bg=CARD_BG, relief="flat",
                                               highlightbackground=BORDER,
                                               highlightthickness=1, wrap="word")
        steps_text.pack(fill="x", padx=24)
        steps_text.insert("1.0", "\n".join(data.get("steps", [])))

        def save():
            ingredients = [l.strip() for l in ing_text.get("1.0", "end").splitlines() if l.strip()]
            steps = [l.strip() for l in steps_text.get("1.0", "end").splitlines() if l.strip()]
            if not ingredients or not steps:
                messagebox.showerror("Error", "Ingredients and steps cannot be empty.", parent=dlg)
                return
            recipes[name] = {"ingredients": ingredients, "steps": steps}
            save_user_recipes(self.username, recipes)
            dlg.destroy()
            self._refresh_recipe_list()
            self._show_recipe_detail(name, recipes[name])

        btn_row = tk.Frame(dlg, bg=BG)
        btn_row.pack(pady=16)
        styled_button(btn_row, "Save Changes", save, color=SUCCESS, width=14).pack(side="left", padx=6)
        styled_button(btn_row, "Cancel", dlg.destroy, color="#8A9BB0", width=10).pack(side="left")

    # ══════════════════════════════════════════
    #  MEAL PLANNER PAGE
    # ══════════════════════════════════════════

    def _show_planner(self):
        self._clear_content()
        self._page_header("🗓️  Meal Planner", "  Plan your week")
        self._nav_highlight("🗓️  Meal Planner")

        recipes = get_user_recipes(self.username)
        plan    = get_user_plan(self.username)
        recipe_names = ["-- None --"] + list(recipes.keys())

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=24, pady=16)

        self.plan_vars = {}

        # Two columns of day cards
        for i, day in enumerate(DAYS_OF_WEEK):
            col = i % 2
            row = i // 2

            card = card_frame(outer)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            outer.columnconfigure(col, weight=1)

            tk.Label(card, text=day, font=FONT_BOLD,
                     bg=CARD_BG, fg=ACCENT).pack(anchor="w", padx=16, pady=(12, 4))

            var = tk.StringVar(value=plan.get(day) or "-- None --")
            self.plan_vars[day] = var

            cb = ttk.Combobox(card, textvariable=var,
                              values=recipe_names, state="readonly",
                              font=FONT_BODY, width=28)
            cb.pack(padx=16, pady=(0, 12))

        # Save button spanning both columns
        styled_button(outer, "💾  Save Plan", self._save_plan,
                      color=SUCCESS, width=18, pady=8).grid(
                          row=4, column=0, columnspan=2, pady=(12, 0))

    def _save_plan(self):
        plan = {}
        for day, var in self.plan_vars.items():
            v = var.get()
            plan[day] = None if v == "-- None --" else v
        save_user_plan(self.username, plan)
        messagebox.showinfo("Saved", "Your meal plan has been saved!")

    # ══════════════════════════════════════════
    #  SHOPPING LIST PAGE
    # ══════════════════════════════════════════

    def _show_shopping(self):
        self._clear_content()
        self._page_header("🛒  Shopping List", "  Auto-generated from your meal plan")
        self._nav_highlight("🛒  Shopping List")

        plan    = get_user_plan(self.username)
        recipes = get_user_recipes(self.username)

        # Build shopping dict
        shopping = {}
        days_used = []
        for day in DAYS_OF_WEEK:
            rname = plan.get(day)
            if rname and rname in recipes:
                days_used.append((day, rname))
                for ing in recipes[rname]["ingredients"]:
                    key = ing.lower().strip()
                    shopping[key] = shopping.get(key, 0) + 1

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=24, pady=16)

        # Left: meal plan summary
        left = card_frame(outer)
        left.pack(side="left", fill="y", ipadx=8, ipady=8, padx=(0, 12))
        left.config(width=260)

        tk.Label(left, text="This Week's Meals", font=FONT_H2,
                 bg=CARD_BG, fg=TEXT_DARK).pack(anchor="w", padx=16, pady=(12, 6))
        tk.Frame(left, height=1, bg=BORDER).pack(fill="x", padx=16, pady=4)

        if not days_used:
            tk.Label(left, text="No meals planned yet.\nGo to Meal Planner first.",
                     font=FONT_BODY, bg=CARD_BG, fg=TEXT_MUTED,
                     justify="center").pack(expand=True)
        else:
            for day, rname in days_used:
                row = tk.Frame(left, bg=CARD_BG)
                row.pack(fill="x", padx=16, pady=3)
                tk.Label(row, text=day, font=FONT_BOLD, width=10,
                         bg=CARD_BG, fg=TEXT_DARK, anchor="w").pack(side="left")
                tk.Label(row, text=rname, font=FONT_BODY,
                         bg=CARD_BG, fg=ACCENT, anchor="w").pack(side="left")

        # Right: shopping list
        right = card_frame(outer)
        right.pack(side="left", fill="both", expand=True, ipadx=8, ipady=8)

        top_row = tk.Frame(right, bg=CARD_BG)
        top_row.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(top_row, text="Shopping List", font=FONT_H2,
                 bg=CARD_BG, fg=TEXT_DARK).pack(side="left")
        if shopping:
            tk.Label(top_row, text=f"{len(shopping)} items",
                     font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MUTED).pack(side="left", padx=8)

        tk.Frame(right, height=1, bg=BORDER).pack(fill="x", padx=16, pady=6)

        if not shopping:
            tk.Label(right, text="Your shopping list is empty.\nPlan some meals first!",
                     font=FONT_BODY, bg=CARD_BG, fg=TEXT_MUTED,
                     justify="center").pack(expand=True)
            return

        # Scrollable list
        canvas = tk.Canvas(right, bg=CARD_BG, highlightthickness=0)
        scroll = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
        items_frame = tk.Frame(canvas, bg=CARD_BG)
        items_frame.bind("<Configure>",
                         lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=items_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(8, 0))
        scroll.pack(side="right", fill="y")

        for item, count in sorted(shopping.items()):
            row = tk.Frame(items_frame, bg=CARD_BG)
            row.pack(fill="x", padx=8, pady=2)
            # Tick circle
            tk.Label(row, text="○", font=FONT_BODY,
                     bg=CARD_BG, fg=SUCCESS).pack(side="left", padx=(0, 8))
            tk.Label(row, text=item.capitalize(), font=FONT_BODY,
                     bg=CARD_BG, fg=TEXT_DARK).pack(side="left")
            if count > 1:
                tk.Label(row, text=f"  ×{count}", font=FONT_SMALL,
                         bg=CARD_BG, fg=ACCENT).pack(side="left")


# ══════════════════════════════════════════════
#  APP LAUNCHER
# ══════════════════════════════════════════════

def _launch_auth():
    root = tk.Tk()
    def on_login(username):
        app_root = tk.Tk()
        AppWindow(app_root, username)
        app_root.mainloop()
    AuthWindow(root, on_login)
    root.mainloop()


if __name__ == "__main__":
    _launch_auth()