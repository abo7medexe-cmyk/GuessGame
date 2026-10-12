import random
import os
import traceback
import re

from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

# هذه النسخة تستخدم arabic_reshaper فقط، ولا تحتاج python-bidi.
# ملاحظة: المعالجة اليدوية مناسبة للنصوص العربية البسيطة، لكنها ليست
# بديلًا كاملًا لخوارزمية Unicode ثنائية الاتجاه، خصوصًا مع النص المختلط.

try:
    import arabic_reshaper
except ImportError:
    arabic_reshaper = None

Window.clearcolor = (0.035, 0.05, 0.10, 1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(
    BASE_DIR, "NotoNaskhArabic-VariableFont_wght.ttf"
)
FONT = "Roboto"

try:
    if os.path.isfile(FONT_FILE):
        LabelBase.register(name="GameArabicFont", fn_regular=FONT_FILE)
        FONT = "GameArabicFont"
except Exception:
    FONT = "Roboto"


def ar(text):
    """تشكيل وعرض مبدئي للنص العربي في Kivy من دون python-bidi."""
    text = str(text)
    if arabic_reshaper is None:
        return text

    shaped = arabic_reshaper.reshape(text)

    # نُبقي مجموعات الأرقام واللاتينية بترتيبها، ونعكس مقاطع العربية.
    parts = re.findall(r"[0-9A-Za-z]+|[^0-9A-Za-z]+", shaped)
    parts.reverse()
    result = []
    for part in parts:
        if re.fullmatch(r"[0-9A-Za-z]+", part):
            result.append(part)
        else:
            result.append(part[::-1])
    return "".join(result)


def make_label(text, size=18, color=(1, 1, 1, 1), **kwargs):
    return Label(
        text=ar(text),
        font_name=FONT,
        font_size=dp(size),
        color=color,
        halign="center",
        valign="middle",
        **kwargs
    )


def make_button(text, color, height=54):
    return Button(
        text=ar(text),
        font_name=FONT,
        font_size=dp(19),
        size_hint_y=None,
        height=dp(height),
        background_normal="",
        background_down="",
        background_color=color,
        color=(1, 1, 1, 1)
    )


class GuessNumberGame(App):
    def build(self):
        self.start_new_round()

        root = BoxLayout(
            orientation="vertical",
            padding=[dp(22), dp(22), dp(22), dp(18)],
            spacing=dp(12)
        )

        root.add_widget(make_label(
            "لعبة تخمين الرقم", size=29,
            color=(0.20, 0.80, 1, 1),
            size_hint_y=None, height=dp(66)
        ))
        root.add_widget(make_label(
            "اختر رقمًا من 1 إلى 100", size=20,
            size_hint_y=None, height=dp(44)
        ))

        self.number_input = TextInput(
            hint_text=ar("اكتب رقمك هنا"),
            font_name=FONT,
            font_size=dp(23),
            input_filter="int",
            multiline=False,
            halign="center",
            size_hint_y=None,
            height=dp(58),
            background_normal="",
            background_active="",
            background_color=(0.12, 0.15, 0.24, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.65, 0.68, 0.76, 1),
            cursor_color=(0.20, 0.80, 1, 1)
        )
        self.number_input.bind(on_text_validate=self.check_guess)
        root.add_widget(self.number_input)

        guess_button = make_button(
            "تحقق من الرقم", (0.08, 0.40, 0.82, 1)
        )
        guess_button.bind(on_release=self.check_guess)
        root.add_widget(guess_button)

        self.feedback = make_label(
            "حظًا موفقًا! ابدأ التخمين", size=19
        )
        self.feedback.bind(size=self.fit_feedback)
        root.add_widget(self.feedback)

        self.attempt_label = make_label(
            "عدد المحاولات: 0", size=18,
            color=(0.70, 0.82, 0.96, 1),
            size_hint_y=None, height=dp(42)
        )
        root.add_widget(self.attempt_label)

        reset_button = make_button(
            "لعبة جديدة", (0.10, 0.52, 0.32, 1)
        )
        reset_button.bind(on_release=self.new_game)
        root.add_widget(reset_button)

        root.add_widget(make_label(
            "خمّن الرقم السري وحاول الوصول إليه!", size=16,
            color=(0.72, 0.76, 0.86, 1)
        ))
        return root

    def fit_feedback(self, instance, size):
        instance.text_size = size

    def start_new_round(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.finished = False

    def check_guess(self, instance):
        if self.finished:
            self.feedback.text = ar("انتهت الجولة! اضغط لعبة جديدة")
            self.feedback.color = (1, 0.78, 0.25, 1)
            return

        value = self.number_input.text.strip()
        if not value:
            self.feedback.text = ar("اكتب رقمًا أولًا")
            self.feedback.color = (1, 0.35, 0.35, 1)
            return

        try:
            guess = int(value)
        except ValueError:
            self.feedback.text = ar("أدخل رقمًا صحيحًا")
            self.feedback.color = (1, 0.35, 0.35, 1)
            return

        if not 1 <= guess <= 100:
            self.feedback.text = ar("الرقم يجب أن يكون بين 1 و100")
            self.feedback.color = (1, 0.35, 0.35, 1)
            return

        self.attempts += 1
        difference = abs(guess - self.secret_number)

        if guess == self.secret_number:
            message = "أحسنت! الرقم الصحيح هو " + str(self.secret_number)
            self.feedback.color = (0.25, 1, 0.5, 1)
            self.finished = True
        elif difference <= 3:
            message = "قريب جدًا! الفرق 3 أو أقل"
            self.feedback.color = (1, 0.76, 0.20, 1)
        elif guess < self.secret_number:
            message = "الرقم السري أكبر من تخمينك"
            self.feedback.color = (0.25, 0.80, 1, 1)
        else:
            message = "الرقم السري أصغر من تخمينك"
            self.feedback.color = (1, 0.48, 0.48, 1)

        self.feedback.text = ar(message)
        self.attempt_label.text = ar("عدد المحاولات: " + str(self.attempts))
        self.number_input.text = ""

    def new_game(self, instance):
        self.start_new_round()
        self.number_input.text = ""
        self.feedback.text = ar("بدأت لعبة جديدة! خمّن الرقم")
        self.feedback.color = (1, 1, 1, 1)
        self.attempt_label.text = ar("عدد المحاولات: 0")


if __name__ == "__main__":
    try:
        GuessNumberGame().run()
    except Exception:
        traceback.print_exc()
        raise
