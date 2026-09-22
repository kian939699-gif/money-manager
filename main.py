import os
import json
import shutil
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty


KV = r'''
#:import dp kivy.metrics.dp


<MainScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(7)

        canvas.before:
            Color:
                rgba: 0.035, 0.045, 0.075, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "💰 MONEY MANAGER 3"
            font_size: "25sp"
            bold: True
            size_hint_y: None
            height: dp(45)

        Label:
            text: "مدیریت هوشمند پول"
            font_size: "13sp"
            size_hint_y: None
            height: dp(22)

        BoxLayout:
            size_hint_y: None
            height: dp(100)
            spacing: dp(6)

            BoxLayout:
                orientation: "vertical"

                canvas.before:
                    Color:
                        rgba: 0.04, 0.22, 0.12, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]

                Label:
                    text: "💰 درآمد"
                    font_size: "14sp"

                Label:
                    text: root.income_text
                    font_size: "16sp"
                    bold: True

            BoxLayout:
                orientation: "vertical"

                canvas.before:
                    Color:
                        rgba: 0.28, 0.06, 0.08, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]

                Label:
                    text: "💸 هزینه"
                    font_size: "14sp"

                Label:
                    text: root.expense_text
                    font_size: "16sp"
                    bold: True

            BoxLayout:
                orientation: "vertical"

                canvas.before:
                    Color:
                        rgba: 0.07, 0.13, 0.28, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]

                Label:
                    text: "💵 موجودی"
                    font_size: "14sp"

                Label:
                    text: root.balance_text
                    font_size: "16sp"
                    bold: True

        Label:
            text: root.message
            size_hint_y: None
            height: dp(28)

        TextInput:
            id: amount
            hint_text: "💵 مبلغ"
            input_filter: "int"
            multiline: False
            font_size: "18sp"
            size_hint_y: None
            height: dp(48)

        TextInput:
            id: title
            hint_text: "📝 عنوان"
            multiline: False
            font_size: "16sp"
            size_hint_y: None
            height: dp(48)

        TextInput:
            id: category
            hint_text: "📂 دسته‌بندی"
            multiline: False
            font_size: "16sp"
            size_hint_y: None
            height: dp(48)

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(7)

            Button:
                text: "➕ درآمد"
                font_size: "17sp"
                on_release: root.add_transaction("income")

            Button:
                text: "➖ هزینه"
                font_size: "17sp"
                on_release: root.add_transaction("expense")

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(6)

            Button:
                text: "📜 تاریخچه"
                on_release: root.open_history()

            Button:
                text: "📊 گزارش"
                on_release: root.open_report()

            Button:
                text: "🎯 هدف"
                on_release: root.open_goal()

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(6)

            Button:
                text: "⚙️ تنظیمات"
                on_release: root.open_settings()

            Button:
                text: "🧹 پاک کردن فرم"
                on_release: root.clear_form()


<HistoryScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(7)

        canvas.before:
            Color:
                rgba: 0.035, 0.045, 0.075, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "📜 تاریخچه"
            font_size: "24sp"
            bold: True
            size_hint_y: None
            height: dp(45)

        TextInput:
            id: search
            hint_text: "🔎 جستجو..."
            multiline: False
            size_hint_y: None
            height: dp(48)
            on_text: root.refresh(self.text)

        ScrollView:

            Label:
                text: root.history_text
                font_size: "16sp"
                text_size: self.width, None
                halign: "right"
                valign: "top"
                size_hint_y: None
                height: self.texture_size[1]

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(7)

            Button:
                text: "🗑 حذف آخرین"
                on_release: root.delete_last()

            Button:
                text: "🗑 حذف همه"
                on_release: root.delete_all()

        Button:
            text: "⬅️ بازگشت"
            size_hint_y: None
            height: dp(50)
            on_release: app.root.current = "main"


<ReportScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(8)

        canvas.before:
            Color:
                rgba: 0.035, 0.045, 0.075, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "📊 گزارش مالی"
            font_size: "25sp"
            bold: True
            size_hint_y: None
            height: dp(50)

        ScrollView:

            Label:
                text: root.report_text
                font_size: "18sp"
                text_size: self.width, None
                halign: "right"
                valign: "top"
                size_hint_y: None
                height: self.texture_size[1]

        Button:
            text: "⬅️ بازگشت"
            size_hint_y: None
            height: dp(52)
            on_release: app.root.current = "main"


<GoalScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(15)
        spacing: dp(10)

        canvas.before:
            Color:
                rgba: 0.035, 0.045, 0.075, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "🎯 هدف پس‌انداز"
            font_size: "25sp"
            bold: True
            size_hint_y: None
            height: dp(50)

        TextInput:
            id: goal
            hint_text: "مبلغ هدف"
            input_filter: "int"
            multiline: False
            font_size: "18sp"
            size_hint_y: None
            height: dp(52)

        Button:
            text: "🎯 ثبت هدف"
            size_hint_y: None
            height: dp(52)
            on_release: root.set_goal()

        Label:
            text: root.goal_text
            font_size: "18sp"
            text_size: self.width, None

        ProgressBar:
            max: 100
            value: root.progress
            size_hint_y: None
            height: dp(30)

        Button:
            text: "⬅️ بازگشت"
            size_hint_y: None
            height: dp(52)
            on_release: app.root.current = "main"


<SettingsScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(15)
        spacing: dp(10)

        canvas.before:
            Color:
                rgba: 0.035, 0.045, 0.075, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "⚙️ تنظیمات"
            font_size: "25sp"
            bold: True
            size_hint_y: None
            height: dp(50)

        Button:
            text: "💾 ساخت بکاپ"
            size_hint_y: None
            height: dp(52)
            on_release: root.backup()

        Button:
            text: "♻️ بازیابی بکاپ"
            size_hint_y: None
            height: dp(52)
            on_release: root.restore()

        Button:
            text: "🗑 پاک کردن تمام اطلاعات"
            size_hint_y: None
            height: dp(52)
            on_release: root.reset_all()

        Label:
            text: root.status
            font_size: "17sp"
            text_size: self.width, None

        Widget:

        Button:
            text: "⬅️ بازگشت"
            size_hint_y: None
            height: dp(52)
            on_release: app.root.current = "main"
'''


class MainScreen(Screen):

    income_text = StringProperty("0 تومان")
    expense_text = StringProperty("0 تومان")
    balance_text = StringProperty("0 تومان")
    message = StringProperty("آماده به کار")

    def on_enter(self):
        self.update_dashboard()

    def update_dashboard(self):

        app = App.get_running_app()

        income = sum(
            x["amount"]
            for x in app.data["transactions"]
            if x["type"] == "income"
        )

        expense = sum(
            x["amount"]
            for x in app.data["transactions"]
            if x["type"] == "expense"
        )

        balance = income - expense

        self.income_text = f"{income:,} تومان"
        self.expense_text = f"{expense:,} تومان"
        self.balance_text = f"{balance:,} تومان"

    def add_transaction(self, kind):

        amount_text = self.ids.amount.text.strip()

        if not amount_text.isdigit() or int(amount_text) <= 0:
            self.message = "⚠️ مبلغ معتبر وارد کن"
            return

        amount = int(amount_text)

        title = self.ids.title.text.strip()

        if not title:
            title = "بدون عنوان"

        category = self.ids.category.text.strip()

        if not category:
            category = "عمومی"

        transaction = {
            "type": kind,
            "amount": amount,
            "title": title,
            "category": category,
            "date": datetime.now().strftime("%Y/%m/%d %H:%M")
        }

        App.get_running_app().data["transactions"].append(
            transaction
        )

        App.get_running_app().save_file()

        self.clear_form()
        self.update_dashboard()

        if kind == "income":
            self.message = "✅ درآمد ثبت شد"
        else:
            self.message = "✅ هزینه ثبت شد"

    def clear_form(self):

        self.ids.amount.text = ""
        self.ids.title.text = ""
        self.ids.category.text = ""

    def open_history(self):

        screen = self.manager.get_screen("history")

        screen.refresh("")

        self.manager.current = "history"

    def open_report(self):

        screen = self.manager.get_screen("report")

        screen.update()

        self.manager.current = "report"

    def open_goal(self):

        screen = self.manager.get_screen("goal")

        screen.update()

        self.manager.current = "goal"

    def open_settings(self):

        self.manager.current = "settings"


class HistoryScreen(Screen):

    history_text = StringProperty("")

    def refresh(self, search=""):

        transactions = App.get_running_app().data["transactions"]

        search = search.lower().strip()

        results = []

        for index, item in enumerate(transactions):

            searchable = (
                item["title"]
                + " "
                + item["category"]
                + " "
                + str(item["amount"])
                + " "
                + item["date"]
            ).lower()

            if not search or search in searchable:

                results.append(
                    (index, item)
                )

        if not results:

            self.history_text = "📭 تراکنشی پیدا نشد."

            return

        lines = []

        for index, item in reversed(results):

            if item["type"] == "income":

                icon = "🟢"
                sign = "+"

            else:

                icon = "🔴"
                sign = "-"

            lines.append(
                f"{icon} {item['title']}\n"
                f"💵 {sign}{item['amount']:,} تومان\n"
                f"📂 {item['category']}\n"
                f"🕐 {item['date']}\n"
                f"شماره تراکنش: {index + 1}\n"
                "━━━━━━━━━━━━━━━━\n"
            )

        self.history_text = "\n".join(lines)

    def delete_last(self):

        data = App.get_running_app().data["transactions"]

        if not data:

            self.history_text = "📭 تراکنشی وجود ندارد."

            return

        data.pop()

        App.get_running_app().save_file()

        self.refresh(
            self.ids.search.text
        )

    def delete_all(self):

        App.get_running_app().data["transactions"] = []

        App.get_running_app().save_file()

        self.refresh("")


class ReportScreen(Screen):

    report_text = StringProperty("")

    def update(self):

        transactions = (
            App.get_running_app()
            .data["transactions"]
        )

        income = 0
        expense = 0

        categories = {}

        for item in transactions:

            if item["type"] == "income":

                income += item["amount"]

            else:

                expense += item["amount"]

                category = item["category"]

                categories[category] = (
                    categories.get(category, 0)
                    + item["amount"]
                )

        balance = income - expense

        if income > 0:

            saving_percent = (
                balance / income
            ) * 100

        else:

            saving_percent = 0

        if categories:

            category_lines = []

            for category, amount in sorted(
                categories.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                category_lines.append(
                    f"• {category}: "
                    f"{amount:,} تومان"
                )

            category_text = "\n".join(
                category_lines
            )

        else:

            category_text = (
                "هنوز هزینه‌ای ثبت نشده."
            )

        self.report_text = (
            "📊 گزارش کامل\n\n"
            f"💰 کل درآمد:\n"
            f"{income:,} تومان\n\n"
            f"💸 کل هزینه:\n"
            f"{expense:,} تومان\n\n"
            f"💵 موجودی:\n"
            f"{balance:,} تومان\n\n"
            f"📈 درصد باقی‌مانده:\n"
            f"{saving_percent:.1f}%\n\n"
            "📂 هزینه بر اساس دسته‌بندی:\n\n"
            f"{category_text}"
        )


class GoalScreen(Screen):

    goal_text = StringProperty(
        "هنوز هدفی تعیین نشده."
    )

    progress = NumericProperty(0)

    def on_enter(self):

        self.update()

    def set_goal(self):

        value = self.ids.goal.text.strip()

        if not value.isdigit() or int(value) <= 0:

            self.goal_text = (
                "⚠️ مبلغ هدف معتبر نیست."
            )

            return

        App.get_running_app().data["goal"] = (
            int(value)
        )

        App.get_running_app().save_file()

        self.ids.goal.text = ""

        self.update()

    def update(self):

        app = App.get_running_app()

        goal = app.data.get("goal", 0)

        income = sum(
            x["amount"]
            for x in app.data["transactions"]
            if x["type"] == "income"
        )

        expense = sum(
            x["amount"]
            for x in app.data["transactions"]
            if x["type"] == "expense"
        )

        balance = income - expense

        if goal <= 0:

            self.goal_text = (
                "🎯 هنوز هدفی تعیین نشده."
            )

            self.progress = 0

            return

        percent = (
            balance / goal
        ) * 100

        if percent < 0:
            percent = 0

        if percent > 100:
            percent = 100

        self.progress = percent

        self.goal_text = (
            f"🎯 هدف: {goal:,} تومان\n\n"
            f"💰 موجودی فعلی: "
            f"{balance:,} تومان\n\n"
            f"📈 پیشرفت: "
            f"{percent:.1f}%"
        )


class SettingsScreen(Screen):

    status = StringProperty("")

    def backup(self):

        app = App.get_running_app()

        try:

            if os.path.exists(
                app.file_path
            ):

                shutil.copy2(
                    app.file_path,
                    app.backup_path
                )

                self.status = (
                    "✅ بکاپ ساخته شد"
                )

            else:

                self.status = (
                    "⚠️ اطلاعاتی برای بکاپ نیست"
                )

        except Exception as e:

            self.status = (
                f"❌ خطا: {e}"
            )

    def restore(self):

        app = App.get_running_app()

        try:

            if not os.path.exists(
                app.backup_path
            ):

                self.status = (
                    "⚠️ بکاپ پیدا نشد"
                )

                return

            shutil.copy2(
                app.backup_path,
                app.file_path
            )

            app.load_file()

            main = self.manager.get_screen(
                "main"
            )

            main.update_dashboard()

            self.status = (
                "✅ بکاپ بازیابی شد"
            )

        except Exception as e:

            self.status = (
                f"❌ خطا: {e}"
            )

    def reset_all(self):

        app = App.get_running_app()

        app.data = {
            "transactions": [],
            "goal": 0
        }

        app.save_file()

        main = self.manager.get_screen(
            "main"
        )

        main.update_dashboard()

        self.status = (
            "♻️ اطلاعات پاک شد"
        )


class MoneyManagerApp(App):

    def build(self):

        self.title = "Money Manager 3"

        self.data = {
            "transactions": [],
            "goal": 0
        }

        self.file_path = os.path.join(
            self.user_data_dir,
            "money_manager.json"
        )

        self.backup_path = os.path.join(
            self.user_data_dir,
            "money_manager_backup.json"
        )

        self.load_file()

        Builder.load_string(KV)

        manager = ScreenManager()

        manager.add_widget(
            MainScreen(
                name="main"
            )
        )

        manager.add_widget(
            HistoryScreen(
                name="history"
            )
        )

        manager.add_widget(
            ReportScreen(
                name="report"
            )
        )

        manager.add_widget(
            GoalScreen(
                name="goal"
            )
        )

        manager.add_widget(
            SettingsScreen(
                name="settings"
            )
        )

        return manager

    def load_file(self):

        try:

            if os.path.exists(
                self.file_path
            ):

                with open(
                    self.file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.data = json.load(file)

            if "transactions" not in self.data:

                self.data["transactions"] = []

            if "goal" not in self.data:

                self.data["goal"] = 0

        except Exception:

            self.data = {
                "transactions": [],
                "goal": 0
            }

    def save_file(self):

        try:

            os.makedirs(
                self.user_data_dir,
                exist_ok=True
            )

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.data,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception as e:

            print(
                "Save error:",
                e
            )


if __name__ == "__main__":

    MoneyManagerApp().run()
