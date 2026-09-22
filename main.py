import os
import json
import shutil
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty

APP_NAME = "Money Manager"
APP_VERSION = "1.0.0"

KV = '''
#:import dp kivy.metrics.dp

<MainScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(7)

        canvas.before:
            Color:
                rgba: .035,.045,.075,1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "💰 MONEY MANAGER"
            font_size: "25sp"
            bold: True
            size_hint_y: None
            height: dp(45)

        Label:
            text: "مدیریت هوشمند پول"
            size_hint_y: None
            height: dp(25)

        BoxLayout:
            size_hint_y: None
            height: dp(90)
            spacing: dp(5)

            BoxLayout:
                orientation: "vertical"
                canvas.before:
                    Color:
                        rgba: .04,.22,.12,1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]
                Label:
                    text: "💰 درآمد"
                Label:
                    text: root.income

            BoxLayout:
                orientation: "vertical"
                canvas.before:
                    Color:
                        rgba: .28,.06,.08,1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]
                Label:
                    text: "💸 هزینه"
                Label:
                    text: root.expense

            BoxLayout:
                orientation: "vertical"
                canvas.before:
                    Color:
                        rgba: .07,.13,.28,1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]
                Label:
                    text: "💵 موجودی"
                Label:
                    text: root.balance

        Label:
            text: root.msg
            size_hint_y: None
            height: dp(25)

        TextInput:
            id: amount
            hint_text: "💵 مبلغ"
            input_filter: "int"
            multiline: False
            size_hint_y: None
            height: dp(48)

        TextInput:
            id: title
            hint_text: "📝 عنوان"
            multiline: False
            size_hint_y: None
            height: dp(48)

        TextInput:
            id: category
            hint_text: "📂 دسته‌بندی"
            multiline: False
            size_hint_y: None
            height: dp(48)

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(7)

            Button:
                text: "➕ درآمد"
                on_release: root.add("income")

            Button:
                text: "➖ هزینه"
                on_release: root.add("expense")

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(7)

            Button:
                text: "📜 تاریخچه"
                on_release: app.root.current = "history"

            Button:
                text: "📊 گزارش"
                on_release: root.report()

            Button:
                text: "🎯 هدف"
                on_release: root.goal()

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(7)

            Button:
                text: "⚙️ تنظیمات"
                on_release: app.root.current = "settings"

            Button:
                text: "🧹 پاک کردن"
                on_release: root.clear()


<HistoryScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(7)

        canvas.before:
            Color:
                rgba: .035,.045,.075,1
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
            hint_text: "🔎 جستجو"
            multiline: False
            size_hint_y: None
            height: dp(48)
            on_text: root.refresh(self.text)

        ScrollView:
            Label:
                text: root.text
                font_size: "16sp"
                text_size: self.width,None
                halign: "right"
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
                rgba: .035,.045,.075,1
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
                text: root.text
                font_size: "18sp"
                text_size: self.width,None
                halign: "right"
                size_hint_y: None
                height: self.texture_size[1]

        Button:
            text: "⬅️ بازگشت"
            size_hint_y: None
            height: dp(50)
            on_release: app.root.current = "main"


<GoalScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(15)
        spacing: dp(10)

        canvas.before:
            Color:
                rgba: .035,.045,.075,1
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
            size_hint_y: None
            height: dp(52)

        Button:
            text: "🎯 ثبت هدف"
            size_hint_y: None
            height: dp(52)
            on_release: root.set_goal()

        Label:
            text: root.info
            font_size: "18sp"
            text_size: self.width,None

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
                rgba: .035,.045,.075,1
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
            text: "🗑 پاک کردن اطلاعات"
            size_hint_y: None
            height: dp(52)
            on_release: root.reset()

        Label:
            text: root.msg
            font_size: "17sp"

        Widget:

        Label:
            text: "Money Manager " + root.version
            size_hint_y: None
            height: dp(30)

        Button:
            text: "⬅️ بازگشت"
            size_hint_y: None
            height: dp(52)
            on_release: app.root.current = "main"
'''


class MainScreen(Screen):
    income = StringProperty("0 تومان")
    expense = StringProperty("0 تومان")
    balance = StringProperty("0 تومان")
    msg = StringProperty("آماده به کار")

    def on_enter(self):
        self.update()

    def update(self):
        data = App.get_running_app().data["transactions"]
        inc = sum(x["amount"] for x in data if x["type"] == "income")
        exp = sum(x["amount"] for x in data if x["type"] == "expense")
        self.income = f"{inc:,} تومان"
        self.expense = f"{exp:,} تومان"
        self.balance = f"{inc-exp:,} تومان"

    def add(self, kind):
        value = self.ids.amount.text.strip()

        if not value.isdigit() or int(value) <= 0:
            self.msg = "⚠️ مبلغ معتبر وارد کن"
            return

        item = {
            "type": kind,
            "amount": int(value),
            "title": self.ids.title.text.strip() or "بدون عنوان",
            "category": self.ids.category.text.strip() or "عمومی",
            "date": datetime.now().strftime("%Y/%m/%d %H:%M")
        }

        App.get_running_app().data["transactions"].append(item)
        App.get_running_app().save()

        self.clear()
        self.update()

        self.msg = "✅ تراکنش ثبت شد"

    def clear(self):
        self.ids.amount.text = ""
        self.ids.title.text = ""
        self.ids.category.text = ""

    def report(self):
        self.manager.get_screen("report").update()
        self.manager.current = "report"

    def goal(self):
        self.manager.get_screen("goal").update()
        self.manager.current = "goal"


class HistoryScreen(Screen):
    text = StringProperty("")

    def on_enter(self):
        self.refresh("")

    def refresh(self, query=""):
        data = App.get_running_app().data["transactions"]
        query = query.lower().strip()

        result = []

        for i, x in enumerate(data):
            s = (
                str(x.get("title", "")) + " " +
                str(x.get("category", "")) + " " +
                str(x.get("amount", "")) + " " +
                str(x.get("date", ""))
            ).lower()

            if not query or query in s:
                result.append((i, x))

        if not result:
            self.text = "📭 تراکنشی وجود ندارد."
            return

        lines = []

        for i, x in reversed(result):
            icon = "🟢" if x["type"] == "income" else "🔴"
            sign = "+" if x["type"] == "income" else "-"

            lines.append(
                f"{icon} {x['title']}\n"
                f"💵 {sign}{x['amount']:,} تومان\n"
                f"📂 {x['category']}\n"
                f"🕐 {x['date']}\n"
                "━━━━━━━━━━━━━━\n"
            )

        self.text = "\n".join(lines)

    def delete_last(self):
        data = App.get_running_app().data["transactions"]

        if data:
            data.pop()
            App.get_running_app().save()

        self.refresh(self.ids.search.text)

    def delete_all(self):
        App.get_running_app().data["transactions"] = []
        App.get_running_app().save()
        self.refresh("")


class ReportScreen(Screen):
    text = StringProperty("")

    def update(self):
        data = App.get_running_app().data["transactions"]

        inc = sum(x["amount"] for x in data if x["type"] == "income")
        exp = sum(x["amount"] for x in data if x["type"] == "expense")
        bal = inc - exp

        cats = {}

        for x in data:
            if x["type"] == "expense":
                c = x.get("category", "عمومی")
                cats[c] = cats.get(c, 0) + x["amount"]

        if inc:
            percent = bal / inc * 100
        else:
            percent = 0

        category_text = "\n".join(
            f"• {k}: {v:,} تومان"
            for k, v in sorted(
                cats.items(),
                key=lambda z: z[1],
                reverse=True
            )
        )

        if not category_text:
            category_text = "هنوز هزینه‌ای ثبت نشده."

        self.text = (
            "📊 گزارش مالی\n\n"
            f"💰 درآمد: {inc:,} تومان\n\n"
            f"💸 هزینه: {exp:,} تومان\n\n"
            f"💵 موجودی: {bal:,} تومان\n\n"
            f"📈 درصد باقی‌مانده: {percent:.1f}%\n\n"
            "📂 هزینه‌ها:\n\n"
            + category_text
        )


class GoalScreen(Screen):
    info = StringProperty("هنوز هدفی تعیین نشده.")
    progress = NumericProperty(0)

    def on_enter(self):
        self.update()

    def set_goal(self):
        value = self.ids.goal.text.strip()

        if not value.isdigit() or int(value) <= 0:
            self.info = "⚠️ مبلغ هدف معتبر نیست."
            return

        App.get_running_app().data["goal"] = int(value)
        App.get_running_app().save()

        self.ids.goal.text = ""
        self.update()

    def update(self):
        app = App.get_running_app()
        goal = app.data.get("goal", 0)

        data = app.data["transactions"]

        inc = sum(x["amount"] for x in data if x["type"] == "income")
        exp = sum(x["amount"] for x in data if x["type"] == "expense")

        balance = inc - exp

        if goal <= 0:
            self.info = "🎯 هنوز هدفی تعیین نشده."
            self.progress = 0
            return

        percent = max(0, min(100, balance / goal * 100))
        remain = max(0, goal - balance)

        self.progress = percent

        self.info = (
            f"🎯 هدف: {goal:,} تومان\n\n"
            f"💰 موجودی: {balance:,} تومان\n\n"
            f"📈 پیشرفت: {percent:.1f}%\n\n"
            f"💵 باقی‌مانده: {remain:,} تومان"
        )


class SettingsScreen(Screen):
    msg = StringProperty("")
    version = StringProperty(APP_VERSION)

    def backup(self):
        app = App.get_running_app()
        app.save()

        try:
            shutil.copy2(app.path_file, app.backup_file)
            self.msg = "✅ بکاپ ساخته شد"
        except Exception as e:
            self.msg = "❌ خطا در ساخت بکاپ"
            print(e)

    def restore(self):
        app = App.get_running_app()

        try:
            if not os.path.exists(app.backup_file):
                self.msg = "⚠️ بکاپ وجود ندارد"
                return

            shutil.copy2(app.backup_file, app.path_file)
            app.load()

            self.manager.get_screen("main").update()
            self.msg = "✅ بکاپ بازیابی شد"

        except Exception as e:
            self.msg = "❌ خطا در بازیابی"
            print(e)

    def reset(self):
        app = App.get_running_app()

        app.data = {
            "transactions": [],
            "goal": 0
        }

        app.save()
        self.manager.get_screen("main").update()
        self.msg = "♻️ اطلاعات پاک شد"


class MoneyManager(App):

    def build(self):
        self.title = APP_NAME

        self.data = {
            "transactions": [],
            "goal": 0
        }

        self.path_file = os.path.join(
            self.user_data_dir,
            "money_manager.json"
        )

        self.backup_file = os.path.join(
            self.user_data_dir,
            "money_manager_backup.json"
        )

        self.load()

        Builder.load_string(KV)

        sm = ScreenManager()

        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.add_widget(ReportScreen(name="report"))
        sm.add_widget(GoalScreen(name="goal"))
        sm.add_widget(SettingsScreen(name="settings"))

        return sm

    def load(self):
        try:
            if os.path.exists(self.path_file):
                with open(
                    self.path_file,
                    "r",
                    encoding="utf-8"
                ) as f:
                    self.data = json.load(f)

            if "transactions" not in self.data:
                self.data["transactions"] = []

            if "goal" not in self.data:
                self.data["goal"] = 0

        except Exception:
            self.data = {
                "transactions": [],
                "goal": 0
            }

    def save(self):
        try:
            os.makedirs(
                self.user_data_dir,
                exist_ok=True
            )

            temp = self.path_file + ".tmp"

            with open(
                temp,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    self.data,
                    f,
                    ensure_ascii=False,
                    indent=2
                )

            os.replace(temp, self.path_file)

        except Exception as e:
            print("Save error:", e)


if __name__ == "__main__":
    MoneyManager().run()
