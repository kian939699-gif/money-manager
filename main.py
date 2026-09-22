__version__ = "2.0.0"

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
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex


DATA_FILE = "money_data.json"


# ---------------- COLORS ----------------

BG = "#0B0F14"
CARD = "#151B23"
CARD2 = "#1D2530"
WHITE = "#F4F7FA"
MUTED = "#9AA7B5"
GREEN = "#35D07F"
RED = "#FF5C67"
BLUE = "#4C9AFF"
YELLOW = "#FFC857"
PURPLE = "#9B7BFF"
BORDER = "#293442"


# ---------------- HELPERS ----------------

def money(value):
    return f"{value:,.2f}"


class RoundedBox(BoxLayout):

    def __init__(self, bg_color=CARD, radius=18, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*get_color_from_hex(bg_color))
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(radius)]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class AppButton(Button):

    def __init__(self, color=BLUE, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = get_color_from_hex(color)
        self.color = get_color_from_hex(WHITE)
        self.font_size = sp(15)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(52)


class SmallButton(Button):

    def __init__(self, color=CARD2, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = get_color_from_hex(color)
        self.color = get_color_from_hex(WHITE)
        self.font_size = sp(13)
        self.size_hint_y = None
        self.height = dp(42)


# ---------------- MAIN APP ----------------

class MoneyManager(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(12),
            padding=[dp(14), dp(12), dp(14), dp(12)],
            **kwargs
        )

        self.data = {
            "balance": 0.0,
            "income": 0.0,
            "expense": 0.0,
            "goal": 0.0,
            "transactions": []
        }

        self.load_data()
        self.build_ui()
        self.refresh()

    # ---------------- DATA ----------------

    def load_data(self):

        try:
            if os.path.exists(DATA_FILE):

                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)

                self.data.update(saved)

        except Exception:
            pass

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

    # ---------------- UI ----------------

    def build_ui(self):

        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=dp(58),
            spacing=dp(8)
        )

        title = Label(
            text="MONEY MANAGER",
            color=get_color_from_hex(WHITE),
            font_size=sp(22),
            bold=True,
            halign="left",
            valign="middle"
        )

        title.bind(size=lambda x, y: setattr(title, "text_size", title.size))

        version = Label(
            text="v2.0",
            color=get_color_from_hex(MUTED),
            font_size=sp(12),
            size_hint_x=None,
            width=dp(45)
        )

        header.add_widget(title)
        header.add_widget(version)

        self.add_widget(header)

        # Main scroll
        scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(4)
        )

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        # Balance card
        balance_card = RoundedBox(
            bg_color=CARD,
            orientation="vertical",
            padding=[dp(18), dp(16)],
            spacing=dp(4),
            size_hint_y=None,
            height=dp(150)
        )

        self.balance_title = Label(
            text="CURRENT BALANCE",
            color=get_color_from_hex(MUTED),
            font_size=sp(13),
            size_hint_y=None,
            height=dp(25)
        )

        self.balance_label = Label(
            text="0.00",
            color=get_color_from_hex(WHITE),
            font_size=sp(34),
            bold=True,
            size_hint_y=None,
            height=dp(58)
        )

        balance_card.add_widget(self.balance_title)
        balance_card.add_widget(self.balance_label)

        stats = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(42)
        )

        self.income_label = Label(
            text="Income: 0.00",
            color=get_color_from_hex(GREEN),
            font_size=sp(13)
        )

        self.expense_label = Label(
            text="Expense: 0.00",
            color=get_color_from_hex(RED),
            font_size=sp(13)
        )

        stats.add_widget(self.income_label)
        stats.add_widget(self.expense_label)

        balance_card.add_widget(stats)
        content.add_widget(balance_card)

        # Transaction card
        transaction_card = RoundedBox(
            bg_color=CARD,
            orientation="vertical",
            padding=[dp(14), dp(14)],
            spacing=dp(10),
            size_hint_y=None,
            height=dp(330)
        )

        transaction_title = Label(
            text="ADD TRANSACTION",
            color=get_color_from_hex(WHITE),
            font_size=sp(18),
            bold=True,
            size_hint_y=None,
            height=dp(35)
        )

        transaction_card.add_widget(transaction_title)

        self.amount_input = TextInput(
            hint_text="Amount",
            multiline=False,
            input_filter="float",
            font_size=sp(17),
            padding=[dp(14), dp(12)],
            size_hint_y=None,
            height=dp(52),
            background_color=get_color_from_hex(CARD2),
            foreground_color=get_color_from_hex(WHITE),
            hint_text_color=get_color_from_hex(MUTED)
        )

        self.category_input = TextInput(
            hint_text="Category  (Food, Transport, Game...)",
            multiline=False,
            font_size=sp(15),
            padding=[dp(14), dp(12)],
            size_hint_y=None,
            height=dp(52),
            background_color=get_color_from_hex(CARD2),
            foreground_color=get_color_from_hex(WHITE),
            hint_text_color=get_color_from_hex(MUTED)
        )

        transaction_card.add_widget(self.amount_input)
        transaction_card.add_widget(self.category_input)

        buttons = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(52)
        )

        income_btn = AppButton(
            text="+  ADD INCOME",
            color=GREEN
        )

        expense_btn = AppButton(
            text="-  ADD EXPENSE",
            color=RED
        )

        income_btn.bind(
            on_release=lambda x: self.add_transaction("income")
        )

        expense_btn.bind(
            on_release=lambda x: self.add_transaction("expense")
        )

        buttons.add_widget(income_btn)
        buttons.add_widget(expense_btn)

        transaction_card.add_widget(buttons)

        content.add_widget(transaction_card)

        # Goal card
        goal_card = RoundedBox(
            bg_color=CARD,
            orientation="vertical",
            padding=[dp(14), dp(14)],
            spacing=dp(8),
            size_hint_y=None,
            height=dp(220)
        )

        goal_title = Label(
            text="SAVINGS GOAL",
            color=get_color_from_hex(WHITE),
            font_size=sp(18),
            bold=True,
            size_hint_y=None,
            height=dp(35)
        )

        goal_row = BoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(52)
        )

        self.goal_input = TextInput(
            hint_text="Goal amount",
            multiline=False,
            input_filter="float",
            font_size=sp(16),
            padding=[dp(12), dp(12)],
            background_color=get_color_from_hex(CARD2),
            foreground_color=get_color_from_hex(WHITE),
            hint_text_color=get_color_from_hex(MUTED)
        )

        goal_btn = AppButton(
            text="SET GOAL",
            color=PURPLE
        )

        goal_btn.bind(
            on_release=self.set_goal
        )

        goal_row.add_widget(self.goal_input)
        goal_row.add_widget(goal_btn)

        self.goal_label = Label(
            text="No savings goal set.",
            color=get_color_from_hex(MUTED),
            font_size=sp(14),
            size_hint_y=None,
            height=dp(30)
        )

        self.goal_progress = Label(
            text="",
            color=get_color_from_hex(YELLOW),
            font_size=sp(15),
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )

        goal_card.add_widget(goal_title)
        goal_card.add_widget(goal_row)
        goal_card.add_widget(self.goal_label)
        goal_card.add_widget(self.goal_progress)

        content.add_widget(goal_card)

        # History
        history_card = RoundedBox(
            bg_color=CARD,
            orientation="vertical",
            padding=[dp(14), dp(14)],
            spacing=dp(8),
            size_hint_y=None,
            height=dp(390)
        )

        history_title = Label(
            text="TRANSACTION HISTORY",
            color=get_color_from_hex(WHITE),
            font_size=sp(18),
            bold=True,
            size_hint_y=None,
            height=dp(35)
        )

        history_card.add_widget(history_title)

        history_scroll = ScrollView(
            do_scroll_x=False,
            size_hint_y=1
        )

        self.history_box = BoxLayout(
            orientation="vertical",
            spacing=dp(7),
            size_hint_y=None
        )

        self.history_box.bind(
            minimum_height=self.history_box.setter("height")
        )

        history_scroll.add_widget(self.history_box)
        history_card.add_widget(history_scroll)

        content.add_widget(history_card)

        # Bottom buttons
        bottom = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )

        clear_btn = SmallButton(
            text="CLEAR HISTORY",
            color=CARD2
        )

        reset_btn = SmallButton(
            text="RESET ALL",
            color="#7D3038"
        )

        clear_btn.bind(
            on_release=self.confirm_clear
        )

        reset_btn.bind(
            on_release=self.confirm_reset
        )

        bottom.add_widget(clear_btn)
        bottom.add_widget(reset_btn)

        content.add_widget(bottom)

        scroll.add_widget(content)
        self.add_widget(scroll)

    # ---------------- TRANSACTIONS ----------------

    def add_transaction(self, kind):

        amount_text = self.amount_input.text.strip()
        category = self.category_input.text.strip()

        if not amount_text:

            self.show_message(
                "Please enter an amount."
            )
            return

        try:
            amount = float(amount_text)

        except ValueError:

            self.show_message(
                "Amount is not valid."
            )
            return

        if amount <= 0:

            self.show_message(
                "Amount must be greater than zero."
            )
            return

        if not category:
            category = "General"

        now = datetime.now()

        transaction = {
            "type": kind,
            "amount": amount,
            "category": category,
            "date": now.strftime("%Y/%m/%d"),
            "time": now.strftime("%H:%M")
        }

        if kind == "income":

            self.data["income"] += amount
            self.data["balance"] += amount

        else:

            self.data["expense"] += amount
            self.data["balance"] -= amount

        self.data["transactions"].insert(
            0,
            transaction
        )

        self.save_data()

        self.amount_input.text = ""
        self.category_input.text = ""

        self.refresh()

    # ---------------- GOAL ----------------

    def set_goal(self, *args):

        text = self.goal_input.text.strip()

        if not text:

            self.show_message(
                "Enter a goal amount."
            )
            return

        try:
            goal = float(text)

        except ValueError:

            self.show_message(
                "Goal amount is not valid."
            )
            return

        if goal <= 0:

            self.show_message(
                "Goal must be greater than zero."
            )
            return

        self.data["goal"] = goal

        self.save_data()
        self.goal_input.text = ""

        self.refresh()

    # ---------------- REFRESH ----------------

    def refresh(self):

        balance = self.data["balance"]
        income = self.data["income"]
        expense = self.data["expense"]
        goal = self.data["goal"]

        self.balance_label.text = money(balance)
        self.income_label.text = f"Income: {money(income)}"
        self.expense_label.text = f"Expense: {money(expense)}"

        if balance >= 0:
            self.balance_label.color = get_color_from_hex(WHITE)
        else:
            self.balance_label.color = get_color_from_hex(RED)

        # Goal
        if goal > 0:

            percent = (balance / goal) * 100

            if percent < 0:
                percent = 0

            if percent > 100:
                percent = 100

            self.goal_label.text = (
                f"Goal: {money(goal)}"
            )

            self.goal_progress.text = (
                f"Progress: {percent:.1f}%"
            )

        else:

            self.goal_label.text = "No savings goal set."
            self.goal_progress.text = ""

        self.refresh_history()

    # ---------------- HISTORY ----------------

    def refresh_history(self):

        self.history_box.clear_widgets()

        transactions = self.data["transactions"]

        if not transactions:

            empty = Label(
                text="No transactions yet.",
                color=get_color_from_hex(MUTED),
                font_size=sp(14),
                size_hint_y=None,
                height=dp(45)
            )

            self.history_box.add_widget(empty)
            return

        for index, item in enumerate(transactions):

            row = RoundedBox(
                bg_color=CARD2,
                orientation="horizontal",
                padding=[dp(10), dp(7)],
                spacing=dp(8),
                size_hint_y=None,
                height=dp(62)
            )

            info = BoxLayout(
                orientation="vertical",
                spacing=dp(2)
            )

            category = Label(
                text=item.get("category", "General"),
                color=get_color_from_hex(WHITE),
                font_size=sp(14),
                bold=True,
                halign="left",
                valign="middle"
            )

            category.bind(
                size=lambda x, y: setattr(
                    category,
                    "text_size",
                    category.size
                )
            )

            date = Label(
                text=f"{item.get('date', '')}  {item.get('time', '')}",
                color=get_color_from_hex(MUTED),
                font_size=sp(11),
                halign="left",
                valign="middle"
            )

            date.bind(
                size=lambda x, y: setattr(
                    date,
                    "text_size",
                    date.size
                )
            )

            info.add_widget(category)
            info.add_widget(date)

            sign = "+" if item["type"] == "income" else "-"
            color = GREEN if item["type"] == "income" else RED

            amount = Label(
                text=f"{sign}{money(item['amount'])}",
                color=get_color_from_hex(color),
                font_size=sp(14),
                bold=True,
                size_hint_x=None,
                width=dp(105),
                halign="right",
                valign="middle"
            )

            amount.bind(
                size=lambda x, y: setattr(
                    amount,
                    "text_size",
                    amount.size
                )
            )

            row.add_widget(info)
            row.add_widget(amount)

            self.history_box.add_widget(row)

    # ---------------- POPUPS ----------------

    def show_message(self, message):

        box = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(12)
        )

        label = Label(
            text=message,
            color=get_color_from_hex(WHITE),
            font_size=sp(15)
        )

        button = AppButton(
            text="OK",
            color=BLUE
        )

        box.add_widget(label)
        box.add_widget(button)

        popup = Popup(
            title="Money Manager",
            content=box,
            size_hint=(0.85, None),
            height=dp(210),
            separator_color=get_color_from_hex(BLUE),
            background_color=get_color_from_hex(CARD)
        )

        button.bind(
            on_release=popup.dismiss
        )

        popup.open()

    def confirm_clear(self, *args):

        self.confirm_popup(
            "Clear all transaction history?",
            self.clear_history
        )

    def confirm_reset(self, *args):

        self.confirm_popup(
            "Reset everything including balance and goal?",
            self.reset_all
        )

    def confirm_popup(self, message, action):

        box = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(12)
        )

        label = Label(
            text=message,
            color=get_color_from_hex(WHITE),
            font_size=sp(14)
        )

        buttons = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )

        cancel = SmallButton(
            text="CANCEL",
            color=CARD2
        )

        yes = SmallButton(
            text="YES",
            color=RED
        )

        buttons.add_widget(cancel)
        buttons.add_widget(yes)

        box.add_widget(label)
        box.add_widget(buttons)

        popup = Popup(
            title="Confirmation",
            content=box,
            size_hint=(0.88, None),
            height=dp(220),
            separator_color=get_color_from_hex(RED),
            background_color=get_color_from_hex(CARD)
        )

        cancel.bind(
            on_release=popup.dismiss
        )

        def do_action(instance):

            popup.dismiss()
            action()

        yes.bind(
            on_release=do_action
        )

        popup.open()

    # ---------------- CLEAR / RESET ----------------

    def clear_history(self):

        self.data["transactions"] = []

        self.save_data()
        self.refresh()

    def reset_all(self):

        self.data = {
            "balance": 0.0,
            "income": 0.0,
            "expense": 0.0,
            "goal": 0.0,
            "transactions": []
        }

        self.save_data()
        self.refresh()


# ---------------- APP ----------------

class MoneyManagerApp(App):

    def build(self):

        self.title = "Money Manager"

        Window.clearcolor = get_color_from_hex(BG)

        try:
            Window.softinput_mode = "below_target"
        except Exception:
            pass

        return MoneyManager()


if __name__ == "__main__":
    MoneyManagerApp().run()
