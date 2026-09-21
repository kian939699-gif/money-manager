__version__ = "1.0.0"

import json
import os
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window


DATA_FILE = "money_data.json"


class MoneyManager(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(12),
            **kwargs
        )

        self.transactions = []
        self.savings_goal = 0

        self.load_data()
        self.build_ui()
        self.update_screen()

    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)

                self.transactions = data.get("transactions", [])
                self.savings_goal = data.get("savings_goal", 0)

        except Exception:
            self.transactions = []
            self.savings_goal = 0

    def save_data(self):
        data = {
            "transactions": self.transactions,
            "savings_goal": self.savings_goal
        }

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def add_transaction(self, transaction_type):
        amount_text = self.amount_input.text.strip()

        if not amount_text:
            self.show_message("Error", "Please enter an amount.")
            return

        try:
            amount = float(amount_text.replace(",", ""))
        except ValueError:
            self.show_message("Error", "Please enter a valid number.")
            return

        if amount <= 0:
            self.show_message("Error", "Amount must be greater than zero.")
            return

        category = self.category_input.text.strip()

        if not category:
            category = "General"

        transaction = {
            "type": transaction_type,
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.transactions.append(transaction)

        self.amount_input.text = ""
        self.category_input.text = ""

        self.save_data()
        self.update_screen()

    def set_goal(self):
        text = self.goal_input.text.strip()

        if not text:
            self.show_message("Error", "Please enter a savings goal.")
            return

        try:
            goal = float(text.replace(",", ""))
        except ValueError:
            self.show_message("Error", "Please enter a valid number.")
            return

        if goal <= 0:
            self.show_message("Error", "Goal must be greater than zero.")
            return

        self.savings_goal = goal
        self.goal_input.text = ""

        self.save_data()
        self.update_screen()

    def calculate_income(self):
        return sum(
            t["amount"]
            for t in self.transactions
            if t["type"] == "income"
        )

    def calculate_expense(self):
        return sum(
            t["amount"]
            for t in self.transactions
            if t["type"] == "expense"
        )

    def calculate_balance(self):
        return self.calculate_income() - self.calculate_expense()

    def build_ui(self):

        title = Label(
            text="MONEY MANAGER",
            font_size=dp(26),
            bold=True,
            size_hint_y=None,
            height=dp(55)
        )
        self.add_widget(title)

        # Balance section
        balance_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(100),
            padding=dp(8)
        )

        balance_title = Label(
            text="CURRENT BALANCE",
            font_size=dp(16)
        )

        self.balance_label = Label(
            text="0",
            font_size=dp(30),
            bold=True
        )

        balance_box.add_widget(balance_title)
        balance_box.add_widget(self.balance_label)

        self.add_widget(balance_box)

        # Statistics
        stats = GridLayout(
            cols=2,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(90)
        )

        self.income_label = Label(text="Income: 0")
        self.expense_label = Label(text="Expense: 0")

        stats.add_widget(self.income_label)
        stats.add_widget(self.expense_label)

        self.add_widget(stats)

        # Amount
        self.amount_input = TextInput(
            hint_text="Enter amount",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(48)
        )

        self.add_widget(self.amount_input)

        # Category
        self.category_input = TextInput(
            hint_text="Category (Food, Transport, etc.)",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )

        self.add_widget(self.category_input)

        # Buttons
        buttons = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(52)
        )

        income_button = Button(text="ADD INCOME")
        income_button.bind(
            on_press=lambda x: self.add_transaction("income")
        )

        expense_button = Button(text="ADD EXPENSE")
        expense_button.bind(
            on_press=lambda x: self.add_transaction("expense")
        )

        buttons.add_widget(income_button)
        buttons.add_widget(expense_button)

        self.add_widget(buttons)

        # Savings goal
        goal_title = Label(
            text="SAVINGS GOAL",
            font_size=dp(17),
            bold=True,
            size_hint_y=None,
            height=dp(35)
        )

        self.add_widget(goal_title)

        goal_box = BoxLayout(
            spacing=dp(6),
            size_hint_y=None,
            height=dp(48)
        )

        self.goal_input = TextInput(
            hint_text="Goal amount",
            multiline=False,
            input_filter="float"
        )

        goal_button = Button(
            text="SET GOAL",
            size_hint_x=None,
            width=dp(110)
        )

        goal_button.bind(on_press=lambda x: self.set_goal())

        goal_box.add_widget(self.goal_input)
        goal_box.add_widget(goal_button)

        self.add_widget(goal_box)

        self.goal_label = Label(
            text="No savings goal set.",
            size_hint_y=None,
            height=dp(40)
        )

        self.add_widget(self.goal_label)

        # History title
        history_title = Label(
            text="TRANSACTION HISTORY",
            font_size=dp(17),
            bold=True,
            size_hint_y=None,
            height=dp(35)
        )

        self.add_widget(history_title)

        # History
        self.history_label = Label(
            text="No transactions yet.",
            halign="left",
            valign="top"
        )

        self.history_label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", (value[0], None))
        )

        self.add_widget(self.history_label)

        # Bottom buttons
        bottom = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(50)
        )

        clear_button = Button(text="CLEAR HISTORY")
        clear_button.bind(
            on_press=lambda x: self.confirm_clear()
        )

        reset_button = Button(text="RESET ALL")
        reset_button.bind(
            on_press=lambda x: self.confirm_reset()
        )

        bottom.add_widget(clear_button)
        bottom.add_widget(reset_button)

        self.add_widget(bottom)

    def update_screen(self):

        income = self.calculate_income()
        expense = self.calculate_expense()
        balance = self.calculate_balance()

        self.balance_label.text = f"{balance:,.2f}"
        self.income_label.text = f"Income: {income:,.2f}"
        self.expense_label.text = f"Expense: {expense:,.2f}"

        # Savings goal
        if self.savings_goal > 0:
            percentage = (balance / self.savings_goal) * 100

            if percentage < 0:
                percentage = 0

            if percentage > 100:
                percentage = 100

            self.goal_label.text = (
                f"Goal: {self.savings_goal:,.2f}   "
                f"Progress: {percentage:.1f}%"
            )
        else:
            self.goal_label.text = "No savings goal set."

        # History
        if not self.transactions:
            self.history_label.text = "No transactions yet."
            return

        lines = []

        for t in reversed(self.transactions[-15:]):

            if t["type"] == "income":
                symbol = "+"
                kind = "Income"
            else:
                symbol = "-"
                kind = "Expense"

            line = (
                f"{symbol}{t['amount']:,.2f} | "
                f"{kind} | "
                f"{t['category']} | "
                f"{t['date']}"
            )

            lines.append(line)

        self.history_label.text = "\n".join(lines)

    def confirm_clear(self):

        box = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )

        label = Label(
            text="Delete all transaction history?"
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(50)
        )

        yes = Button(text="YES")
        no = Button(text="NO")

        buttons.add_widget(yes)
        buttons.add_widget(no)

        box.add_widget(label)
        box.add_widget(buttons)

        popup = Popup(
            title="Confirm",
            content=box,
            size_hint=(0.85, 0.3)
        )

        yes.bind(
            on_press=lambda x: (
                self.clear_history(),
                popup.dismiss()
            )
        )

        no.bind(on_press=popup.dismiss)

        popup.open()

    def clear_history(self):
        self.transactions = []
        self.save_data()
        self.update_screen()

    def confirm_reset(self):

        box = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )

        label = Label(
            text="Reset ALL data?"
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(50)
        )

        yes = Button(text="YES")
        no = Button(text="NO")

        buttons.add_widget(yes)
        buttons.add_widget(no)

        box.add_widget(label)
        box.add_widget(buttons)

        popup = Popup(
            title="Reset",
            content=box,
            size_hint=(0.85, 0.3)
        )

        yes.bind(
            on_press=lambda x: (
                self.reset_all(),
                popup.dismiss()
            )
        )

        no.bind(on_press=popup.dismiss)

        popup.open()

    def reset_all(self):
        self.transactions = []
        self.savings_goal = 0

        self.amount_input.text = ""
        self.category_input.text = ""
        self.goal_input.text = ""

        self.save_data()
        self.update_screen()

    def show_message(self, title, message):

        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )

        popup.open()


class MoneyManagerApp(App):

    def build(self):
        Window.softinput_mode = "below_target"
        return MoneyManager()


if __name__ == "__main__":
    MoneyManagerApp().run()
