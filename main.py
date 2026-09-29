# -*- coding: utf-8 -*-

__version__ = "1.0.0"

import json
import os
import random

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


# =========================================================
# تنظیمات
# =========================================================

Window.clearcolor = (0.04, 0.055, 0.08, 1)

DATA_FILE = "english7_progress.json"

BG = (0.04, 0.055, 0.08, 1)
CARD = (0.075, 0.095, 0.13, 1)
CARD2 = (0.10, 0.125, 0.17, 1)

TEXT = (0.95, 0.97, 1, 1)
MUTED = (0.65, 0.70, 0.78, 1)

GREEN = (0.20, 0.82, 0.50, 1)
BLUE = (0.25, 0.58, 1, 1)
PURPLE = (0.60, 0.40, 1, 1)
ORANGE = (1, 0.60, 0.20, 1)
RED = (1, 0.30, 0.35, 1)


# =========================================================
# داده‌های آموزشی
# =========================================================

LESSONS = [
    {
        "title": "الفبای انگلیسی",
        "icon": "🔤",
        "description": "یادگیری A تا Z",
        "words": [
            ("A", "اِی", "Apple", "سیب"),
            ("B", "بی", "Book", "کتاب"),
            ("C", "سی", "Cat", "گربه"),
            ("D", "دی", "Dog", "سگ"),
            ("E", "ای", "Egg", "تخم‌مرغ"),
            ("F", "اِف", "Fish", "ماهی"),
            ("G", "جی", "Game", "بازی"),
            ("H", "اِیچ", "House", "خانه"),
            ("I", "آی", "Ice", "یخ"),
            ("J", "جِی", "Juice", "آبمیوه"),
            ("K", "کِی", "King", "پادشاه"),
            ("L", "اِل", "Lion", "شیر"),
            ("M", "اِم", "Moon", "ماه"),
            ("N", "اِن", "Name", "نام"),
            ("O", "او", "Orange", "پرتقال"),
            ("P", "پی", "Pen", "خودکار"),
            ("Q", "کیو", "Queen", "ملکه"),
            ("R", "آر", "Red", "قرمز"),
            ("S", "اِس", "Sun", "خورشید"),
            ("T", "تی", "Tree", "درخت"),
            ("U", "یو", "Umbrella", "چتر"),
            ("V", "وی", "Van", "ون"),
            ("W", "دابلیو", "Water", "آب"),
            ("X", "اِکس", "Box", "جعبه"),
            ("Y", "وای", "Yellow", "زرد"),
            ("Z", "زِد", "Zoo", "باغ‌وحش"),
        ]
    },

    {
        "title": "کلمات روزمره",
        "icon": "📚",
        "description": "کلمات پرکاربرد",
        "words": [
            ("Hello", "هلو", "سلام", "سلام"),
            ("Goodbye", "گودبای", "خداحافظ", "خداحافظ"),
            ("Yes", "یِس", "بله", "بله"),
            ("No", "نو", "نه", "نه"),
            ("Please", "پلیز", "لطفاً", "لطفاً"),
            ("Thanks", "ثَنکس", "متشکرم", "متشکرم"),
            ("Friend", "فِرِند", "دوست", "دوست"),
            ("School", "اِسکول", "مدرسه", "مدرسه"),
            ("Teacher", "تیچِر", "معلم", "معلم"),
            ("Student", "اِستودِنت", "دانش‌آموز", "دانش‌آموز"),
            ("Book", "بوک", "کتاب", "کتاب"),
            ("Pen", "پِن", "خودکار", "خودکار"),
            ("Football", "فوتبال", "فوتبال", "فوتبال"),
            ("Water", "واتِر", "آب", "آب"),
            ("Food", "فود", "غذا", "غذا"),
        ]
    },

    {
        "title": "معرفی خودت",
        "icon": "🙋",
        "description": "جمله‌های مهم برای معرفی",
        "words": [
            (
                "My name is Kian.",
                "مای نیم ایز کیان.",
                "اسم من کیان است.",
                ""
            ),
            (
                "I am a student.",
                "آی اَم اِ اِستودِنت.",
                "من دانش‌آموز هستم.",
                ""
            ),
            (
                "I am fourteen years old.",
                "آی اَم فورتین ییرز اُلد.",
                "من چهارده ساله هستم.",
                ""
            ),
            (
                "I like football.",
                "آی لایک فوتبال.",
                "من فوتبال دوست دارم.",
                ""
            ),
            (
                "I like English.",
                "آی لایک انگلیش.",
                "من انگلیسی دوست دارم.",
                ""
            ),
            (
                "My favorite team is Real Madrid.",
                "مای فِیوِریت تیم ایز رئال مادرید.",
                "تیم مورد علاقه من رئال مادرید است.",
                ""
            ),
            (
                "I live in Iran.",
                "آی لیو اِن ایران.",
                "من در ایران زندگی می‌کنم.",
                ""
            ),
            (
                "I am from Iran.",
                "آی اَم فرام ایران.",
                "من اهل ایران هستم.",
                ""
            ),
        ]
    },

    {
        "title": "افعال مهم",
        "icon": "⚡",
        "description": "فعل‌های پایه",
        "words": [
            ("Be", "بی", "بودن", ""),
            ("Have", "هَو", "داشتن", ""),
            ("Go", "گو", "رفتن", ""),
            ("Come", "کام", "آمدن", ""),
            ("Like", "لایک", "دوست داشتن", ""),
            ("Play", "پلی", "بازی کردن", ""),
            ("Eat", "ایت", "خوردن", ""),
            ("Drink", "درینک", "نوشیدن", ""),
            ("See", "سی", "دیدن", ""),
            ("Read", "رید", "خواندن", ""),
            ("Write", "رایت", "نوشتن", ""),
            ("Speak", "اِسپیک", "صحبت کردن", ""),
        ]
    },

    {
        "title": "گرامر پایه",
        "icon": "🧠",
        "description": "جمله‌سازی ساده",
        "words": [
            ("I am", "آی اَم", "من هستم", ""),
            ("You are", "یو آر", "تو هستی", ""),
            ("He is", "هی ایز", "او مذکر است", ""),
            ("She is", "شی ایز", "او مؤنث است", ""),
            ("It is", "ایت ایز", "آن است", ""),
            ("We are", "وی آر", "ما هستیم", ""),
            ("They are", "ذِی آر", "آن‌ها هستند", ""),
        ]
    },

    {
        "title": "مکالمه روزمره",
        "icon": "🗣️",
        "description": "صحبت کردن در موقعیت‌های ساده",
        "words": [
            (
                "How are you?",
                "هاو آر یو؟",
                "حالت چطوره؟",
                ""
            ),
            (
                "I am fine.",
                "آی اَم فاین.",
                "من خوبم.",
                ""
            ),
            (
                "What is your name?",
                "وات ایز یور نیم؟",
                "اسمت چیست؟",
                ""
            ),
            (
                "My name is Kian.",
                "مای نیم ایز کیان.",
                "اسم من کیان است.",
                ""
            ),
            (
                "How old are you?",
                "هاو اُلد آر یو؟",
                "چند سالت است؟",
                ""
            ),
            (
                "I am fourteen.",
                "آی اَم فورتین.",
                "من چهارده ساله هستم.",
                ""
            ),
            (
                "What do you like?",
                "وات دو یو لایک؟",
                "چه چیزی دوست داری؟",
                ""
            ),
            (
                "I like football.",
                "آی لایک فوتبال.",
                "من فوتبال دوست دارم.",
                ""
            ),
            (
                "Nice to meet you.",
                "نایس تو میت یو.",
                "از آشنایی با تو خوشحالم.",
                ""
            ),
            (
                "See you later.",
                "سی یو لِیتِر.",
                "بعداً می‌بینمت.",
                ""
            ),
        ]
    },
]


# =========================================================
# سوال‌های آزمون
# =========================================================

QUIZ = [
    {
        "q": "Apple یعنی چه؟",
        "options": ["سیب", "کتاب", "خانه", "آب"],
        "answer": 0
    },
    {
        "q": "Book یعنی چه؟",
        "options": ["گربه", "کتاب", "سگ", "مدرسه"],
        "answer": 1
    },
    {
        "q": "Hello یعنی چه؟",
        "options": ["خداحافظ", "لطفاً", "سلام", "متشکرم"],
        "answer": 2
    },
    {
        "q": "Teacher یعنی چه؟",
        "options": ["دانش‌آموز", "معلم", "دوست", "بازیکن"],
        "answer": 1
    },
    {
        "q": "I like football یعنی چه؟",
        "options": [
            "من فوتبال دوست دارم.",
            "من فوتبال بازی می‌کنم.",
            "من فوتبال ندارم.",
            "من فوتبال می‌بینم."
        ],
        "answer": 0
    },
    {
        "q": "My name is Kian یعنی چه؟",
        "options": [
            "من کیان را دوست دارم.",
            "اسم من کیان است.",
            "کیان دوست من است.",
            "من دانش‌آموزم."
        ],
        "answer": 1
    },
    {
        "q": "Goodbye یعنی چه؟",
        "options": [
            "سلام",
            "صبح بخیر",
            "خداحافظ",
            "شب بخیر"
        ],
        "answer": 2
    },
    {
        "q": "Water یعنی چه؟",
        "options": [
            "آب",
            "غذا",
            "شیر",
            "آبمیوه"
        ],
        "answer": 0
    },
    {
        "q": "Student یعنی چه؟",
        "options": [
            "معلم",
            "دانش‌آموز",
            "پزشک",
            "دوست"
        ],
        "answer": 1
    },
    {
        "q": "How are you? یعنی چه؟",
        "options": [
            "اسمت چیست؟",
            "کجا زندگی می‌کنی؟",
            "حالت چطوره؟",
            "چند سالت است؟"
        ],
        "answer": 2
    },
]


# =========================================================
# ابزارهای ظاهری
# =========================================================

class RoundedBox(BoxLayout):

    def __init__(self, bg=CARD, radius=18, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*bg)

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(radius)]
            )

        self.bind(
            pos=self._update_rect,
            size=self._update_rect
        )

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MainButton(Button):

    def __init__(
        self,
        text="",
        bg=BLUE,
        font_size=17,
        **kwargs
    ):
        super().__init__(
            text=text,
            font_size=sp(font_size),
            color=TEXT,
            background_normal="",
            background_down="",
            **kwargs
        )

        self.bg_color = bg

        with self.canvas.before:
            Color(*bg)

            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

        self.bind(
            pos=self._update,
            size=self._update
        )

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


def make_label(
    text,
    size=18,
    color=TEXT,
    bold=False,
    halign="center"
):
    label = Label(
        text=text,
        font_size=sp(size),
        color=color,
        bold=bold,
        halign=halign,
        valign="middle"
    )

    label.bind(
        size=lambda instance, value:
        setattr(instance, "text_size", value)
    )

    return label


# =========================================================
# صفحه اصلی
# =========================================================

class HomeScreen(Screen):

    def on_pre_enter(self):
        self.build()

    def build(self):

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(14)
        )

        # هدر
        header = BoxLayout(
            size_hint_y=None,
            height=dp(75)
        )

        title_box = BoxLayout(
            orientation="vertical"
        )

        title_box.add_widget(
            make_label(
                "English 7",
                27,
                TEXT,
                True
            )
        )

        title_box.add_widget(
            make_label(
                "یادگیری انگلیسی از صفر تا مکالمه",
                13,
                MUTED
            )
        )

        header.add_widget(title_box)

        profile = MainButton(
            text="👤",
            bg=PURPLE,
            font_size=24,
            size_hint_x=None,
            width=dp(58)
        )

        profile.bind(
            on_release=lambda x:
            setattr(self.manager, "current", "profile")
        )

        header.add_widget(profile)

        root.add_widget(header)

        # کارت پیشرفت
        progress_card = RoundedBox(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(155)
        )

        app = App.get_running_app()

        level = app.get_level()
        xp = app.data.get("xp", 0)

        progress_card.add_widget(
            make_label(
                f"سطح {level}  ⭐",
                23,
                TEXT,
                True
            )
        )

        progress_card.add_widget(
            make_label(
                f"{xp} امتیاز تجربه",
                14,
                MUTED
            )
        )

        bar = ProgressBar(
            max=100,
            value=app.get_progress(),
            size_hint_y=None,
            height=dp(14)
        )

        progress_card.add_widget(bar)

        progress_card.add_widget(
            make_label(
                f"پیشرفت کلی: {app.get_progress()}٪",
                13,
                GREEN
            )
        )

        root.add_widget(progress_card)

        # لیست درس‌ها
        scroll = ScrollView()

        lessons_box = GridLayout(
            cols=1,
            spacing=dp(12),
            size_hint_y=None
        )

        lessons_box.bind(
            minimum_height=lessons_box.setter("height")
        )

        for i, lesson in enumerate(LESSONS):

            unlocked = i <= app.data.get(
                "unlocked",
                0
            )

            button_text = (
                f"{lesson['icon']}   "
                f"{lesson['title']}\n"
                f"{lesson['description']}"
            )

            if not unlocked:
                button_text = (
                    "🔒   "
                    + lesson["title"]
                    + "\n"
                    + "این مرحله هنوز قفل است"
                )

            btn = MainButton(
                text=button_text,
                bg=(
                    CARD2
                    if unlocked
                    else (0.11, 0.12, 0.15, 1)
                ),
                font_size=16,
                size_hint_y=None,
                height=dp(82)
            )

            if unlocked:
                btn.bind(
                    on_release=lambda x, index=i:
                    self.open_lesson(index)
                )

            lessons_box.add_widget(btn)

        scroll.add_widget(lessons_box)

        root.add_widget(scroll)

        # پایین
        bottom = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )

        quiz_btn = MainButton(
            text="🎯 آزمون",
            bg=ORANGE
        )

        quiz_btn.bind(
            on_release=lambda x:
            setattr(self.manager, "current", "quiz")
        )

        bottom.add_widget(quiz_btn)

        stats_btn = MainButton(
            text="📊 پیشرفت",
            bg=GREEN
        )

        stats_btn.bind(
            on_release=lambda x:
            setattr(self.manager, "current", "profile")
        )

        bottom.add_widget(stats_btn)

        root.add_widget(bottom)

        self.add_widget(root)

    def open_lesson(self, index):

        lesson_screen = self.manager.get_screen(
            "lesson"
        )

        lesson_screen.load_lesson(index)

        self.manager.current = "lesson"


# =========================================================
# صفحه درس
# =========================================================

class LessonScreen(Screen):

    def load_lesson(self, index):

        self.lesson_index = index
        self.word_index = 0

        self.clear_widgets()

        lesson = LESSONS[index]

        root = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(15)
        )

        top = BoxLayout(
            size_hint_y=None,
            height=dp(60)
        )

        back = MainButton(
            text="←",
            bg=CARD2,
            font_size=25,
            size_hint_x=None,
            width=dp(60)
        )

        back.bind(
            on_release=lambda x:
            self.back_home()
        )

        top.add_widget(back)

        top.add_widget(
            make_label(
                lesson["icon"] + " " + lesson["title"],
                21,
                TEXT,
                True
            )
        )

        root.add_widget(top)

        self.counter = make_label(
            "",
            14,
            MUTED
        )

        root.add_widget(self.counter)

        # کارت کلمه
        self.card = RoundedBox(
            orientation="vertical",
            padding=dp(22),
            spacing=dp(14)
        )

        self.english = make_label(
            "",
            34,
            TEXT,
            True
        )

        self.pronunciation = make_label(
            "",
            19,
            BLUE
        )

        self.meaning = make_label(
            "",
            23,
            GREEN,
            True
        )

        self.card.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(10)
            )
        )

        self.card.add_widget(self.english)
        self.card.add_widget(self.pronunciation)
        self.card.add_widget(self.meaning)

        self.card.add_widget(Widget())

        root.add_widget(self.card)

        # اطلاعات
        self.extra = make_label(
            "",
            15,
            MUTED
        )

        root.add_widget(self.extra)

        # دکمه‌ها
        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(65),
            spacing=dp(12)
        )

        prev = MainButton(
            text="◀ قبلی",
            bg=CARD2
        )

        prev.bind(
            on_release=lambda x:
            self.previous_word()
        )

        buttons.add_widget(prev)

        next_btn = MainButton(
            text="بعدی ▶",
            bg=BLUE
        )

        next_btn.bind(
            on_release=lambda x:
            self.next_word()
        )

        buttons.add_widget(next_btn)

        root.add_widget(buttons)

        self.add_widget(root)

        self.update_word()

    def update_word(self):

        lesson = LESSONS[self.lesson_index]

        word = lesson["words"][self.word_index]

        self.english.text = word[0]
        self.pronunciation.text = "🔊 " + word[1]
        self.meaning.text = word[2]

        if word[3]:
            self.extra.text = word[3]
        else:
            self.extra.text = (
                "کلمه را چند بار با صدای بلند تکرار کن."
            )

        self.counter.text = (
            f"{self.word_index + 1} / "
            f"{len(lesson['words'])}"
        )

    def previous_word(self):

        if self.word_index > 0:
            self.word_index -= 1
            self.update_word()

    def next_word(self):

        lesson = LESSONS[self.lesson_index]

        if self.word_index < len(lesson["words"]) - 1:

            self.word_index += 1
            self.update_word()

        else:

            app = App.get_running_app()

            app.complete_lesson(
                self.lesson_index
            )

            Popup(
                title="🎉 مرحله کامل شد!",
                content=make_label(
                    "آفرین!\n"
                    "این درس را تمام کردی.\n\n"
                    "+100 XP ⭐",
                    19,
                    TEXT,
                    True
                ),
                size_hint=(0.85, 0.35)
            ).open()

            self.manager.current = "home"

    def back_home(self):

        self.manager.current = "home"


# =========================================================
# صفحه آزمون
# =========================================================

class QuizScreen(Screen):

    def on_pre_enter(self):

        self.question_index = 0
        self.score = 0

        self.questions = random.sample(
            QUIZ,
            len(QUIZ)
        )

        self.build_question()

    def build_question(self):

        self.clear_widgets()

        q = self.questions[
            self.question_index
        ]

        root = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(18)
        )

        header = BoxLayout(
            size_hint_y=None,
            height=dp(60)
        )

        back = MainButton(
            text="←",
            bg=CARD2,
            font_size=25,
            size_hint_x=None,
            width=dp(60)
        )

        back.bind(
            on_release=lambda x:
            setattr(self.manager, "current", "home")
        )

        header.add_widget(back)

        header.add_widget(
            make_label(
                "🎯 آزمون انگلیسی",
                23,
                TEXT,
                True
            )
        )

        root.add_widget(header)

        root.add_widget(
            make_label(
                f"سؤال {self.question_index + 1} "
                f"از {len(self.questions)}",
                14,
                MUTED
            )
        )

        card = RoundedBox(
            orientation="vertical",
            padding=dp(22),
            spacing=dp(20)
        )

        card.add_widget(
            make_label(
                q["q"],
                25,
                TEXT,
                True
            )
        )

        root.add_widget(card)

        options = GridLayout(
            cols=1,
            spacing=dp(12),
            size_hint_y=None
        )

        options.bind(
            minimum_height=options.setter("height")
        )

        for i, option in enumerate(
            q["options"]
        ):

            btn = MainButton(
                text=option,
                bg=CARD2,
                font_size=17,
                size_hint_y=None,
                height=dp(60)
            )

            btn.bind(
                on_release=lambda x, n=i:
                self.answer(n)
            )

            options.add_widget(btn)

        root.add_widget(options)

        root.add_widget(Widget())

        self.add_widget(root)

    def answer(self, selected):

        q = self.questions[
            self.question_index
        ]

        if selected == q["answer"]:

            self.score += 1

            Popup(
                title="✅ درست!",
                content=make_label(
                    "آفرین! پاسخ درست بود.",
                    19,
                    GREEN,
                    True
                ),
                size_hint=(0.8, 0.3)
            ).open()

        else:

            Popup(
                title="❌ اشتباه",
                content=make_label(
                    "اشکالی ندارد؛ جواب درست را یاد بگیر.",
                    17,
                    RED,
                    True
                ),
                size_hint=(0.85, 0.3)
            ).open()

        if self.question_index < len(
            self.questions
        ) - 1:

            self.question_index += 1
            self.build_question()

        else:

            self.finish_quiz()

    def finish_quiz(self):

        app = App.get_running_app()

        xp = self.score * 20

        app.data["xp"] += xp
        app.data["quiz_score"] = self.score

        app.save_data()

        percentage = int(
            self.score /
            len(self.questions) *
            100
        )

        Popup(
            title="🏆 آزمون تمام شد!",
            content=make_label(
                f"امتیاز: "
                f"{self.score}/"
                f"{len(self.questions)}\n\n"
                f"درصد: {percentage}%\n\n"
                f"+{xp} XP ⭐",
                20,
                TEXT,
                True
            ),
            size_hint=(0.85, 0.45)
        ).open()

        self.manager.current = "home"


# =========================================================
# صفحه پروفایل
# =========================================================

class ProfileScreen(Screen):

    def on_pre_enter(self):

        self.clear_widgets()

        app = App.get_running_app()

        root = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(15)
        )

        header = BoxLayout(
            size_hint_y=None,
            height=dp(60)
        )

        back = MainButton(
            text="←",
            bg=CARD2,
            font_size=25,
            size_hint_x=None,
            width=dp(60)
        )

        back.bind(
            on_release=lambda x:
            setattr(self.manager, "current", "home")
        )

        header.add_widget(back)

        header.add_widget(
            make_label(
                "📊 پیشرفت من",
                23,
                TEXT,
                True
            )
        )

        root.add_widget(header)

        stats = RoundedBox(
            orientation="vertical",
            padding=dp(22),
            spacing=dp(15)
        )

        stats.add_widget(
            make_label(
                f"⭐ سطح {app.get_level()}",
                28,
                TEXT,
                True
            )
        )

        stats.add_widget(
            make_label(
                f"امتیاز تجربه: "
                f"{app.data.get('xp', 0)} XP",
                18,
                GREEN
            )
        )

        stats.add_widget(
            make_label(
                f"🔥 روزهای متوالی: "
                f"{app.data.get('streak', 0)}",
                18,
                ORANGE
            )
        )

        stats.add_widget(
            make_label(
                f"🎯 بهترین آزمون: "
                f"{app.data.get('quiz_score', 0)}/10",
                18,
                BLUE
            )
        )

        stats.add_widget(
            make_label(
                f"📚 درس‌های کامل‌شده: "
                f"{app.data.get('completed', 0)}",
                18,
                PURPLE
            )
        )

        root.add_widget(stats)

        root.add_widget(
            make_label(
                "💡 برای پیشرفت سریع، هر روز "
                "حداقل ۱۵ دقیقه تمرین کن.",
                16,
                MUTED
            )
        )

        reset = MainButton(
            text="♻️ شروع دوباره",
            bg=RED,
            size_hint_y=None,
            height=dp(58)
        )

        reset.bind(
            on_release=lambda x:
            self.reset_progress()
        )

        root.add_widget(reset)

        root.add_widget(Widget())

        self.add_widget(root)

    def reset_progress(self):

        app = App.get_running_app()

        app.data = {
            "xp": 0,
            "completed": 0,
            "unlocked": 0,
            "quiz_score": 0,
            "streak": 0
        }

        app.save_data()

        self.manager.current = "home"


# =========================================================
# برنامه اصلی
# =========================================================

class English7App(App):

    def build(self):

        self.title = "English 7"

        self.load_data()

        sm = ScreenManager(
            transition=FadeTransition(
                duration=0.15
            )
        )

        sm.add_widget(
            HomeScreen(name="home")
        )

        sm.add_widget(
            LessonScreen(name="lesson")
        )

        sm.add_widget(
            QuizScreen(name="quiz")
        )

        sm.add_widget(
            ProfileScreen(name="profile")
        )

        return sm

    # -----------------------------------------------------

    def load_data(self):

        default = {
            "xp": 0,
            "completed": 0,
            "unlocked": 0,
            "quiz_score": 0,
            "streak": 0
        }

        try:

            if os.path.exists(DATA_FILE):

                with open(
                    DATA_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:

                    self.data = json.load(f)

                for key, value in default.items():

                    if key not in self.data:
                        self.data[key] = value

            else:

                self.data = default.copy()

        except Exception:

            self.data = default.copy()

    # -----------------------------------------------------

    def save_data(self):

        try:

            with open(
                DATA_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.data,
                    f,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception:
            pass

    # -----------------------------------------------------

    def complete_lesson(self, index):

        if index > self.data.get(
            "unlocked",
            0
        ):
            return

        self.data["completed"] = max(
            self.data.get("completed", 0),
            index + 1
        )

        self.data["unlocked"] = min(
            len(LESSONS) - 1,
            max(
                self.data.get("unlocked", 0),
                index + 1
            )
        )

        self.data["xp"] += 100

        self.save_data()

    # -----------------------------------------------------

    def get_level(self):

        xp = self.data.get("xp", 0)

        return min(
            20,
            (xp // 200) + 1
        )

    # -----------------------------------------------------

    def get_progress(self):

        completed = self.data.get(
            "completed",
            0
        )

        total = len(LESSONS)

        return min(
            100,
            int(
                completed /
                total *
                100
            )
        )


# =========================================================
# اجرای برنامه
# =========================================================

if __name__ == "__main__":
    English7App().run()
