__version__ = "2.1.0"

import json
import os
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle


DATA_FILE = "money_data.json"


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def money(value):
    try:
        value = float(value)
    except:
        value = 0

    if value == int(value):
        return f"{int(value):,}"

    return f"{value:,.2f}"


def today():
    return datetime.now().strftime("%Y-%m-%d")


def make_id():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


# ---------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------

class MoneyManagerApp(App):

    def build(self):

        Window.clearcolor = (0.035, 0.035, 0.045, 1)

        self.data = self.load_data()

        self.root_box = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        self.build_header()
        self.build_dashboard()

        return self.root_box

    # -----------------------------------------------------
    # DATA
    # -----------------------------------------------------

    def default_data(self):
        return {
            "transactions": [],
            "goal": 0,
            "goal_name": "Savings Goal"
        }

    def load_data(self):

        if not os.path.exists(DATA_FILE):
            return self.default_data()

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                old = json.load(f)

            data = self.default_data()

            # New format
            if isinstance(old, dict):

                if isinstance(old.get("transactions"), list):
                    data["transactions"] = old["transactions"]

                data["goal"] = old.get(
                    "goal",
                    old.get("goal_amount", 0)
                )

                data["goal_name"] = old.get(
                    "goal_name",
                    "Savings Goal"
                )

            self.normalize_transactions(data)

            return data

        except Exception:
            return self.default_data()

    def normalize_transactions(self, data):

        clean = []

        for item in data.get("transactions", []):

            if not isinstance(item, dict):
                continue

            amount = item.get(
                "amount",
                item.get("value", 0)
            )

            try:
                amount = float(amount)
            except:
                continue

            typ = str(
                item.get(
                    "type",
                    item.get("kind", "expense")
                )
            ).lower()

            if typ in ("income", "in", "درآمد"):
                typ = "income"
            else:
                typ = "expense"

            clean.append({
                "id": item.get("id", make_id()),
                "type": typ,
                "amount": amount,
                "category": str(
                    item.get(
                        "category",
                        item.get("name", "Other")
                    )
                ),
                "date": str(
                    item.get(
                        "date",
                        today()
                    )
                ),
                "note": str(
                    item.get(
                        "note",
                        item.get("description", "")
                    )
                )
            })

        data["transactions"] = clean

    def save_data(self):

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    self.data,
                    f,
                    ensure_ascii=False,
                    indent=2
                )
        except Exception:
            pass

    # -----------------------------------------------------
    # UI HELPERS
    # -----------------------------------------------------

    def label(self, text, size=16, bold=False):
        return Label(
            text=text,
            font_size=sp(size),
            bold=bold,
            color=(0.95, 0.95, 0.98, 1),
            halign="center",
            valign="middle"
        )

    def button(self, text, callback, height=48):
        btn = Button(
            text=text,
            font_size=sp(15),
            size_hint_y=None,
            height=dp(height),
            background_normal="",
            background_color=(0.16, 0.17, 0.21, 1),
            color=(1, 1, 1, 1)
        )
        btn.bind(on_release=callback)
        return btn

    def input_box(self, hint="", text=""):
        return TextInput(
            hint_text=hint,
            text=text,
            multiline=False,
            font_size=sp(16),
            size_hint_y=None,
            height=dp(50),
            padding=[dp(12), dp(12)]
        )

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    def build_header(self):

        header = BoxLayout(
            size_hint_y=None,
            height=dp(65),
            spacing=dp(8)
        )

        title = self.label(
            "💰 MONEY MANAGER",
            23,
            True
        )

        version = self.label(
            "v2.1",
            13,
            False
        )

        header.add_widget(title)
        header.add_widget(version)

        self.root_box.add_widget(header)

    # -----------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------

    def build_dashboard(self):

        self.dashboard = BoxLayout(
            orientation="vertical",
            spacing=dp(8)
        )

        self.root_box.add_widget(self.dashboard)

        self.refresh_dashboard()

    def refresh_dashboard(self):

        self.dashboard.clear_widgets()

        income = sum(
            x["amount"]
            for x in self.data["transactions"]
            if x["type"] == "income"
        )

        expense = sum(
            x["amount"]
            for x in self.data["transactions"]
            if x["type"] == "expense"
        )

        balance = income - expense

        # Balance
        balance_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(125),
            padding=dp(12)
        )

        balance_box.add_widget(
            self.label("CURRENT BALANCE", 15, True)
        )

        self.balance_label = self.label(
            money(balance),
            32,
            True
        )

        balance_box.add_widget(self.balance_label)

        self.dashboard.add_widget(balance_box)

        # Summary
        summary = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(85),
            spacing=dp(8)
        )

        summary.add_widget(
            self.label(
                f"INCOME\n{money(income)}",
                15,
                True
            )
        )

        summary.add_widget(
            self.label(
                f"EXPENSE\n{money(expense)}",
                15,
                True
            )
        )

        self.dashboard.add_widget(summary)

        # Buttons
        actions = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(105),
            spacing=dp(8)
        )

        actions.add_widget(
            self.button(
                "➕ ADD INCOME",
                self.add_income
            )
        )

        actions.add_widget(
            self.button(
                "➖ ADD EXPENSE",
                self.add_expense
            )
        )

        actions.add_widget(
            self.button(
                "🎯 SAVINGS GOAL",
                self.goal_popup
            )
        )

        actions.add_widget(
            self.button(
                "📊 REPORT",
                self.report_popup
            )
        )

        self.dashboard.add_widget(actions)

        # More
        more = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(105),
            spacing=dp(8)
        )

        more.add_widget(
            self.button(
                "🔎 SEARCH",
                self.search_popup
            )
        )

        more.add_widget(
            self.button(
                "📜 HISTORY",
                self.history_popup
            )
        )

        more.add_widget(
            self.button(
                "🔄 REFRESH",
                lambda x: self.refresh_dashboard()
            )
        )

        more.add_widget(
            self.button(
                "⚙ RESET DATA",
                self.reset_popup
            )
        )

        self.dashboard.add_widget(more)

        # Goal
        self.dashboard.add_widget(
            self.goal_summary()
        )

        self.dashboard.add_widget(
            self.label(
                "Money Manager • Your money, your control.",
                12
            )
        )

    # -----------------------------------------------------
    # GOAL
    # -----------------------------------------------------

    def goal_summary(self):

        box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(105),
            spacing=dp(5)
        )

        goal = float(self.data.get("goal", 0) or 0)

        income = sum(
            x["amount"]
            for x in self.data["transactions"]
            if x["type"] == "income"
        )

        expense = sum(
            x["amount"]
            for x in self.data["transactions"]
            if x["type"] == "expense"
        )

        balance = max(0, income - expense)

        if goal > 0:

            percent = min(
                100,
                (balance / goal) * 100
            )

            box.add_widget(
                self.label(
                    f"🎯 {self.data.get('goal_name','Savings Goal')}   "
                    f"{money(balance)} / {money(goal)}",
                    14,
                    True
                )
            )

            progress = ProgressBar(
                max=100,
                value=percent,
                size_hint_y=None,
                height=dp(18)
            )

            box.add_widget(progress)

            box.add_widget(
                self.label(
                    f"{percent:.1f}% completed",
                    13
                )
            )

        else:

            box.add_widget(
                self.label(
                    "🎯 No savings goal set.",
                    14,
                    True
                )
            )

        return box

    def goal_popup(self, *args):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        name = self.input_box(
            "Goal name",
            self.data.get("goal_name", "Savings Goal")
        )

        amount = self.input_box(
            "Goal amount",
            str(self.data.get("goal", ""))
        )

        save = self.button(
            "SAVE GOAL",
            lambda x: self.save_goal(
                name,
                amount,
                popup
            )
        )

        layout.add_widget(name)
        layout.add_widget(amount)
        layout.add_widget(save)

        popup = Popup(
            title="🎯 Savings Goal",
            content=layout,
            size_hint=(0.9, None),
            height=dp(280)
        )

        popup.open()

    def save_goal(self, name, amount, popup):

        try:
            value = float(amount.text)
            if value < 0:
                raise ValueError
        except:
            return

        self.data["goal"] = value
        self.data["goal_name"] = (
            name.text.strip()
            or "Savings Goal"
        )

        self.save_data()
        popup.dismiss()
        self.refresh_dashboard()

    # -----------------------------------------------------
    # ADD TRANSACTION
    # -----------------------------------------------------

    def add_income(self, *args):
        self.transaction_popup("income")

    def add_expense(self, *args):
        self.transaction_popup("expense")

    def transaction_popup(self, typ):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        amount = self.input_box(
            "Amount"
        )

        category = self.input_box(
            "Category (Food, Transport, etc.)"
        )

        note = self.input_box(
            "Note (optional)"
        )

        date = self.input_box(
            "Date YYYY-MM-DD",
            today()
        )

        title = (
            "➕ Add Income"
            if typ == "income"
            else
            "➖ Add Expense"
        )

        save = self.button(
            "SAVE",
            lambda x: self.save_transaction(
                typ,
                amount,
                category,
                note,
                date,
                popup
            )
        )

        layout.add_widget(amount)
        layout.add_widget(category)
        layout.add_widget(note)
        layout.add_widget(date)
        layout.add_widget(save)

        popup = Popup(
            title=title,
            content=layout,
            size_hint=(0.92, None),
            height=dp(390)
        )

        popup.open()

    def save_transaction(
        self,
        typ,
        amount,
        category,
        note,
        date,
        popup
    ):

        try:
            value = float(
                amount.text.replace(",", "")
            )

            if value <= 0:
                raise ValueError

        except:
            return

        item = {
            "id": make_id(),
            "type": typ,
            "amount": value,
            "category": category.text.strip() or "Other",
            "date": date.text.strip() or today(),
            "note": note.text.strip()
        }

        self.data["transactions"].append(item)

        self.save_data()

        popup.dismiss()

        self.refresh_dashboard()

    # -----------------------------------------------------
    # HISTORY
    # -----------------------------------------------------

    def history_popup(self, *args):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(5)
        )

        scroll = ScrollView()

        items = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            size_hint_y=None
        )

        items.bind(
            minimum_height=items.setter(
                "height"
            )
        )

        transactions = list(
            reversed(
                self.data["transactions"]
            )
        )

        if not transactions:

            items.add_widget(
                self.label(
                    "No transactions yet.",
                    16
                )
            )

        for item in transactions:

            row = self.transaction_row(
                item
            )

            items.add_widget(row)

        scroll.add_widget(items)

        layout.add_widget(scroll)

        close = self.button(
            "CLOSE",
            lambda x: popup.dismiss()
        )

        layout.add_widget(close)

        popup = Popup(
            title="📜 Transaction History",
            content=layout,
            size_hint=(0.96, 0.9)
        )

        popup.open()

    def transaction_row(self, item):

        row = BoxLayout(
            size_hint_y=None,
            height=dp(85),
            spacing=dp(5)
        )

        typ = item["type"]

        sign = "+" if typ == "income" else "-"

        text = (
            f"{sign}{money(item['amount'])}\n"
            f"{item['category']} • {item['date']}\n"
            f"{item.get('note','')}"
        )

        info = self.label(
            text,
            13,
            False
        )

        edit = self.button(
            "✏️",
            lambda x, i=item:
            self.edit_transaction(i),
            55
        )

        delete = self.button(
            "🗑️",
            lambda x, i=item:
            self.delete_transaction(i),
            55
        )

        row.add_widget(info)
        row.add_widget(edit)
        row.add_widget(delete)

        return row

    # -----------------------------------------------------
    # EDIT
    # -----------------------------------------------------

    def edit_transaction(self, item):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        amount = self.input_box(
            "Amount",
            str(item["amount"])
        )

        category = self.input_box(
            "Category",
            item["category"]
        )

        note = self.input_box(
            "Note",
            item.get("note", "")
        )

        date = self.input_box(
            "Date",
            item.get("date", today())
        )

        save = self.button(
            "SAVE CHANGES",
            lambda x: self.update_transaction(
                item,
                amount,
                category,
                note,
                date,
                popup
            )
        )

        layout.add_widget(amount)
        layout.add_widget(category)
        layout.add_widget(note)
        layout.add_widget(date)
        layout.add_widget(save)

        popup = Popup(
            title="✏️ Edit Transaction",
            content=layout,
            size_hint=(0.92, None),
            height=dp(390)
        )

        popup.open()

    def update_transaction(
        self,
        item,
        amount,
        category,
        note,
        date,
        popup
    ):

        try:
            value = float(
                amount.text.replace(",", "")
            )

            if value <= 0:
                raise ValueError

        except:
            return

        item["amount"] = value
        item["category"] = (
            category.text.strip()
            or "Other"
        )
        item["note"] = note.text.strip()
        item["date"] = (
            date.text.strip()
            or today()
        )

        self.save_data()

        popup.dismiss()

        self.refresh_dashboard()

    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------

    def delete_transaction(self, item):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        layout.add_widget(
            self.label(
                "Delete this transaction?",
                17,
                True
            )
        )

        buttons = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(55),
            spacing=dp(8)
        )

        buttons.add_widget(
            self.button(
                "CANCEL",
                lambda x: popup.dismiss()
            )
        )

        buttons.add_widget(
            self.button(
                "DELETE",
                lambda x:
                self.confirm_delete(
                    item,
                    popup
                )
            )
        )

        layout.add_widget(buttons)

        popup = Popup(
            title="⚠️ Confirm",
            content=layout,
            size_hint=(0.85, None),
            height=dp(210)
        )

        popup.open()

    def confirm_delete(self, item, popup):

        try:
            self.data["transactions"].remove(
                item
            )
        except:
            pass

        self.save_data()

        popup.dismiss()

        self.refresh_dashboard()

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    def search_popup(self, *args):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        search = self.input_box(
            "Search category, note, date..."
        )

        results = ScrollView()

        result_box = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_y=None
        )

        result_box.bind(
            minimum_height=result_box.setter(
                "height"
            )
        )

        def do_search(instance):

            result_box.clear_widgets()

            q = search.text.lower().strip()

            found = []

            for item in self.data["transactions"]:

                text = (
                    str(item.get("category", "")) +
                    " " +
                    str(item.get("note", "")) +
                    " " +
                    str(item.get("date", ""))
                ).lower()

                if q in text:
                    found.append(item)

            if not found:

                result_box.add_widget(
                    self.label(
                        "No results.",
                        16
                    )
                )

            else:

                for item in reversed(found):
                    result_box.add_widget(
                        self.transaction_row(item)
                    )

        search.bind(
            text=do_search
        )

        results.add_widget(result_box)

        layout.add_widget(search)
        layout.add_widget(results)

        close = self.button(
            "CLOSE",
            lambda x: popup.dismiss()
        )

        layout.add_widget(close)

        popup = Popup(
            title="🔎 Search",
            content=layout,
            size_hint=(0.96, 0.9)
        )

        popup.open()

    # -----------------------------------------------------
    # REPORT
    # -----------------------------------------------------

    def report_popup(self, *args):

        income = sum(
            x["amount"]
            for x in self.data["transactions"]
            if x["type"] == "income"
        )

        expense = sum(
            x["amount"]
            for x in self.data["transactions"]
            if x["type"] == "expense"
        )

        balance = income - expense

        categories = {}

        for item in self.data["transactions"]:

            if item["type"] != "expense":
                continue

            cat = item["category"]

            categories[cat] = (
                categories.get(cat, 0)
                + item["amount"]
            )

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        layout.add_widget(
            self.label(
                "📊 FINANCIAL REPORT",
                21,
                True
            )
        )

        layout.add_widget(
            self.label(
                f"Total Income: {money(income)}",
                16,
                True
            )
        )

        layout.add_widget(
            self.label(
                f"Total Expense: {money(expense)}",
                16,
                True
            )
        )

        layout.add_widget(
            self.label(
                f"Balance: {money(balance)}",
                18,
                True
            )
        )

        layout.add_widget(
            self.label(
                "EXPENSE BY CATEGORY",
                15,
                True
            )
        )

        scroll = ScrollView()

        cats = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(5)
        )

        cats.bind(
            minimum_height=cats.setter(
                "height"
            )
        )

        if categories:

            for name, value in sorted(
                categories.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                cats.add_widget(
                    self.label(
                        f"{name}: {money(value)}",
                        14
                    )
                )

        else:

            cats.add_widget(
                self.label(
                    "No expenses yet.",
                    14
                )
            )

        scroll.add_widget(cats)

        layout.add_widget(scroll)

        layout.add_widget(
            self.button(
                "CLOSE",
                lambda x: popup.dismiss()
            )
        )

        popup = Popup(
            title="📊 Report",
            content=layout,
            size_hint=(0.92, 0.9)
        )

        popup.open()

    # -----------------------------------------------------
    # RESET
    # -----------------------------------------------------

    def reset_popup(self, *args):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        layout.add_widget(
            self.label(
                "⚠️ This will delete all transactions\n"
                "and the savings goal.",
                16,
                True
            )
        )

        buttons = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(55),
            spacing=dp(8)
        )

        buttons.add_widget(
            self.button(
                "CANCEL",
                lambda x: popup.dismiss()
            )
        )

        buttons.add_widget(
            self.button(
                "RESET",
                lambda x:
                self.do_reset(popup)
            )
        )

        layout.add_widget(buttons)

        popup = Popup(
            title="⚠️ RESET ALL",
            content=layout,
            size_hint=(0.88, None),
            height=dp(230)
        )

        popup.open()

    def do_reset(self, popup):

        self.data = self.default_data()

        self.save_data()

        popup.dismiss()

        self.refresh_dashboard()


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

if __name__ == "__main__":
    MoneyManagerApp().run()
