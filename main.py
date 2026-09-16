import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import MyMemoryTranslator
import threading
import queue


# =========================================================
# THEME
# =========================================================

BG = "#0b1120"
CARD = "#111827"
CARD_2 = "#172033"
BORDER = "#263247"
TEXT = "#f8fafc"
MUTED = "#94a3b8"
ACCENT = "#6366f1"
ACCENT_HOVER = "#4f46e5"
SUCCESS = "#22c55e"
DANGER = "#f87171"
INPUT_BG = "#0f172a"


# =========================================================
# LANGUAGES
# =========================================================

LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en-GB",
    "Telugu": "te-IN",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Bengali": "bn-IN",
    "Gujarati": "gu-IN",
    "Marathi": "mr-IN",
    "Punjabi": "pa-IN",
    "Urdu": "ur-PK",
    "French": "fr-FR",
    "German": "de-DE",
    "Spanish": "es-ES",
    "Italian": "it-IT",
    "Portuguese": "pt-PT",
    "Russian": "ru-RU",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Chinese": "zh-CN",
    "Arabic": "ar-SA",
    "Turkish": "tr-TR",
}


# =========================================================
# TRANSLATION FUNCTION
# =========================================================

def translate_text(text, source, target):

    if source == target:
        return text

    translator = MyMemoryTranslator(
        source=source,
        target=target
    )

    result = translator.translate(text)

    if not result:
        raise Exception("No translation result received.")

    return result


# =========================================================
# APPLICATION
# =========================================================

class TranslatorApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Language Translation Tool")
        self.root.geometry("1000x760")
        self.root.minsize(850, 700)
        self.root.configure(bg=BG)

        self.result_queue = queue.Queue()
        self.loading = False
        self.loading_dots = 0

        self.setup_style()
        self.build_ui()

        self.root.after(100, self.check_queue)
        self.root.after(350, self.loading_animation)

        self.root.bind("<Control-Return>", self.translate)


    # =====================================================
    # STYLE
    # =====================================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Dark.TCombobox",
            fieldbackground=INPUT_BG,
            background=CARD_2,
            foreground=TEXT,
            arrowcolor=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=8,
            font=("Segoe UI", 11)
        )

        style.map(
            "Dark.TCombobox",
            fieldbackground=[
                ("readonly", INPUT_BG)
            ],
            foreground=[
                ("readonly", TEXT)
            ]
        )


    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        main = tk.Frame(
            self.root,
            bg=BG
        )

        main.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=24
        )


        # =================================================
        # HEADER
        # =================================================

        header = tk.Frame(
            main,
            bg=BG
        )

        header.pack(
            fill="x",
            pady=(0, 18)
        )


        logo = tk.Label(
            header,
            text="✦",
            font=("Segoe UI", 30, "bold"),
            fg=ACCENT,
            bg=BG
        )

        logo.pack(
            side="left",
            padx=(0, 12)
        )


        title_box = tk.Frame(
            header,
            bg=BG
        )

        title_box.pack(
            side="left"
        )


        tk.Label(
            title_box,
            text="Language Translation Tool",
            font=("Segoe UI", 25, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            anchor="w"
        )


        tk.Label(
            title_box,
            text="Fast • Simple • Intelligent multilingual translation",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=BG
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


        # STATUS

        status_box = tk.Frame(
            header,
            bg=CARD_2,
            padx=12,
            pady=7
        )

        status_box.pack(
            side="right",
            pady=5
        )


        self.status_dot = tk.Label(
            status_box,
            text="●",
            font=("Segoe UI", 9),
            fg=SUCCESS,
            bg=CARD_2
        )

        self.status_dot.pack(
            side="left"
        )


        self.status_label = tk.Label(
            status_box,
            text=" Ready",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT,
            bg=CARD_2
        )

        self.status_label.pack(
            side="left"
        )


        # =================================================
        # LANGUAGE CARD
        # =================================================

        language_card = tk.Frame(
            main,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        language_card.pack(
            fill="x",
            pady=(0, 16)
        )


        language_content = tk.Frame(
            language_card,
            bg=CARD
        )

        language_content.pack(
            fill="x",
            padx=18,
            pady=15
        )


        # FROM

        from_frame = tk.Frame(
            language_content,
            bg=CARD
        )

        from_frame.pack(
            side="left",
            fill="x",
            expand=True
        )


        tk.Label(
            from_frame,
            text="FROM",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(
            anchor="w",
            pady=(0, 5)
        )


        self.from_var = tk.StringVar(
            value="English"
        )


        self.from_combo = ttk.Combobox(
            from_frame,
            textvariable=self.from_var,
            values=list(LANGUAGES.keys()),
            state="readonly",
            style="Dark.TCombobox"
        )

        self.from_combo.pack(
            fill="x"
        )


        # SWAP BUTTON

        self.swap_button = tk.Button(
            language_content,
            text="⇄",
            font=("Segoe UI Symbol", 18, "bold"),
            fg=TEXT,
            bg=ACCENT,
            activeforeground=TEXT,
            activebackground=ACCENT_HOVER,
            relief="flat",
            bd=0,
            width=4,
            cursor="hand2",
            command=self.swap_languages
        )

        self.swap_button.pack(
            side="left",
            padx=18,
            pady=17
        )


        self.swap_button.bind(
            "<Enter>",
            lambda event: self.swap_button.config(
                bg=ACCENT_HOVER
            )
        )

        self.swap_button.bind(
            "<Leave>",
            lambda event: self.swap_button.config(
                bg=ACCENT
            )
        )


        # TO

        to_frame = tk.Frame(
            language_content,
            bg=CARD
        )

        to_frame.pack(
            side="left",
            fill="x",
            expand=True
        )


        tk.Label(
            to_frame,
            text="TO",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(
            anchor="w",
            pady=(0, 5)
        )


        self.to_var = tk.StringVar(
            value="Telugu"
        )


        self.to_combo = ttk.Combobox(
            to_frame,
            textvariable=self.to_var,
            values=[
                language
                for language in LANGUAGES
                if language != "Auto Detect"
            ],
            state="readonly",
            style="Dark.TCombobox"
        )

        self.to_combo.pack(
            fill="x"
        )


        # =================================================
        # TEXT AREA
        # IMPORTANT: FIXED HEIGHT
        # =================================================

        text_area = tk.Frame(
            main,
            bg=BG,
            height=360
        )

        text_area.pack(
            fill="x",
            expand=False
        )

        text_area.pack_propagate(False)


        # =================================================
        # INPUT CARD
        # =================================================

        input_card = tk.Frame(
            text_area,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        input_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )


        tk.Label(
            input_card,
            text="YOUR TEXT",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 7)
        )


        input_box = tk.Frame(
            input_card,
            bg=INPUT_BG
        )

        input_box.pack(
            fill="both",
            expand=True,
            padx=11,
            pady=(0, 7)
        )


        self.input_text = tk.Text(
            input_box,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            selectbackground=ACCENT,
            selectforeground=TEXT,
            relief="flat",
            bd=0,
            wrap="word",
            font=("Segoe UI", 12),
            padx=11,
            pady=11
        )

        self.input_text.pack(
            fill="both",
            expand=True
        )


        self.input_text.insert(
            "1.0",
            "Type or paste your text here..."
        )

        self.input_text.config(
            fg=MUTED
        )


        self.input_text.bind(
            "<FocusIn>",
            self.remove_placeholder
        )

        self.input_text.bind(
            "<FocusOut>",
            self.restore_placeholder
        )

        self.input_text.bind(
            "<KeyRelease>",
            self.update_count
        )


        self.count_label = tk.Label(
            input_card,
            text="0 characters",
            font=("Segoe UI", 8),
            fg=MUTED,
            bg=CARD
        )

        self.count_label.pack(
            anchor="e",
            padx=15,
            pady=(0, 8)
        )


        # =================================================
        # OUTPUT CARD
        # =================================================

        output_card = tk.Frame(
            text_area,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        output_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )


        tk.Label(
            output_card,
            text="TRANSLATED RESULT",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 7)
        )


        output_box = tk.Frame(
            output_card,
            bg=INPUT_BG
        )

        output_box.pack(
            fill="both",
            expand=True,
            padx=11,
            pady=(0, 7)
        )


        self.output_text = tk.Text(
            output_box,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            selectbackground=ACCENT,
            selectforeground=TEXT,
            relief="flat",
            bd=0,
            wrap="word",
            font=("Segoe UI", 12),
            padx=11,
            pady=11,
            state="disabled"
        )

        self.output_text.pack(
            fill="both",
            expand=True
        )


        # COPY BUTTON

        self.copy_button = tk.Button(
            output_card,
            text="Copy Result",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT,
            bg=CARD_2,
            activeforeground=TEXT,
            activebackground=ACCENT,
            relief="flat",
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.copy_result
        )

        self.copy_button.pack(
            anchor="e",
            padx=15,
            pady=(0, 8)
        )


        # =================================================
        # ACTION BAR
        # THIS WILL ALWAYS BE VISIBLE
        # =================================================

        action_bar = tk.Frame(
            main,
            bg=BG,
            height=55
        )

        action_bar.pack(
            fill="x",
            expand=False,
            pady=(15, 8)
        )

        action_bar.pack_propagate(False)


        # CLEAR BUTTON

        clear_button = tk.Button(
            action_bar,
            text="Clear",
            font=("Segoe UI", 10, "bold"),
            fg=MUTED,
            bg=CARD_2,
            activeforeground=TEXT,
            activebackground=BORDER,
            relief="flat",
            bd=0,
            padx=24,
            pady=9,
            cursor="hand2",
            command=self.clear_all
        )

        clear_button.pack(
            side="left"
        )


        # TRANSLATE BUTTON

        self.translate_button = tk.Button(
            action_bar,
            text="Translate  →",
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg=ACCENT,
            activeforeground="white",
            activebackground=ACCENT_HOVER,
            relief="flat",
            bd=0,
            padx=30,
            pady=9,
            cursor="hand2",
            command=self.translate
        )

        self.translate_button.pack(
            side="right"
        )


        self.translate_button.bind(
            "<Enter>",
            lambda event: self.translate_button.config(
                bg=ACCENT_HOVER
            )
        )

        self.translate_button.bind(
            "<Leave>",
            lambda event: self.translate_button.config(
                bg=ACCENT
            )
        )


        # =================================================
        # FOOTER
        # =================================================

        footer = tk.Frame(
            main,
            bg=BG
        )

        footer.pack(
            fill="x"
        )


        tk.Label(
            footer,
            text="Powered by MyMemory",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg=BG
        ).pack(
            side="left"
        )


        tk.Label(
            footer,
            text="Ctrl + Enter to translate",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg=BG
        ).pack(
            side="right"
        )


    # =====================================================
    # PLACEHOLDER
    # =====================================================

    def remove_placeholder(self, event=None):

        current = self.input_text.get(
            "1.0",
            "end-1c"
        )

        if current == "Type or paste your text here...":

            self.input_text.delete(
                "1.0",
                "end"
            )

            self.input_text.config(
                fg=TEXT
            )


    def restore_placeholder(self, event=None):

        current = self.input_text.get(
            "1.0",
            "end-1c"
        ).strip()

        if not current:

            self.input_text.delete(
                "1.0",
                "end"
            )

            self.input_text.insert(
                "1.0",
                "Type or paste your text here..."
            )

            self.input_text.config(
                fg=MUTED
            )


    # =====================================================
    # CHARACTER COUNT
    # =====================================================

    def update_count(self, event=None):

        current = self.input_text.get(
            "1.0",
            "end-1c"
        )

        if current == "Type or paste your text here...":
            count = 0
        else:
            count = len(current)

        self.count_label.config(
            text=f"{count} characters"
        )


    # =====================================================
    # TRANSLATE
    # =====================================================

    def translate(self, event=None):

        if self.loading:
            return


        text = self.input_text.get(
            "1.0",
            "end-1c"
        ).strip()


        if not text or text == "Type or paste your text here...":

            messagebox.showwarning(
                "Empty Text",
                "Please enter some text to translate."
            )

            return


        source_name = self.from_var.get()
        target_name = self.to_var.get()


        if source_name == "Auto Detect":

            messagebox.showinfo(
                "Source Language",
                "Please select the source language manually."
            )

            return


        source_code = LANGUAGES[source_name]
        target_code = LANGUAGES[target_name]


        self.loading = True
        self.loading_dots = 0


        self.status_label.config(
            text=" Translating"
        )


        self.copy_button.config(
            state="disabled"
        )


        self.translate_button.config(
            state="disabled"
        )


        thread = threading.Thread(
            target=self.translation_worker,
            args=(
                text,
                source_code,
                target_code
            ),
            daemon=True
        )

        thread.start()


    # =====================================================
    # TRANSLATION WORKER
    # =====================================================

    def translation_worker(
        self,
        text,
        source,
        target
    ):

        try:

            result = translate_text(
                text,
                source,
                target
            )

            self.result_queue.put(
                ("success", result)
            )

        except Exception as error:

            self.result_queue.put(
                ("error", str(error))
            )


    # =====================================================
    # CHECK QUEUE
    # =====================================================

    def check_queue(self):

        try:

            status, data = self.result_queue.get_nowait()

            self.loading = False


            self.translate_button.config(
                state="normal",
                text="Translate  →"
            )


            if status == "success":

                self.show_result(data)

            else:

                self.show_error(data)

        except queue.Empty:

            pass


        self.root.after(
            100,
            self.check_queue
        )


    # =====================================================
    # LOADING ANIMATION
    # =====================================================

    def loading_animation(self):

        if self.loading:

            dots = "." * (
                (self.loading_dots % 3) + 1
            )

            self.translate_button.config(
                text=f"Translating{dots}"
            )

            self.loading_dots += 1


        self.root.after(
            350,
            self.loading_animation
        )


    # =====================================================
    # SHOW RESULT
    # =====================================================

    def show_result(self, result):

        self.output_text.config(
            state="normal"
        )


        self.output_text.delete(
            "1.0",
            "end"
        )


        self.output_text.insert(
            "1.0",
            result
        )


        self.output_text.config(
            state="disabled"
        )


        self.copy_button.config(
            state="normal"
        )


        self.status_label.config(
            text=" Translation Complete"
        )


    # =====================================================
    # SWAP LANGUAGES
    # =====================================================

    def swap_languages(self):

        source = self.from_var.get()
        target = self.to_var.get()


        if source == "Auto Detect":

            messagebox.showinfo(
                "Swap Languages",
                "Please select a source language first."
            )

            return


        self.from_var.set(target)
        self.to_var.set(source)


    # =====================================================
    # COPY RESULT
    # =====================================================

    def copy_result(self):

        result = self.output_text.get(
            "1.0",
            "end-1c"
        ).strip()


        if not result:
            return


        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.root.update()


        self.copy_button.config(
            text="Copied ✓",
            bg=SUCCESS
        )


        self.root.after(
            1500,
            self.reset_copy_button
        )


    def reset_copy_button(self):

        self.copy_button.config(
            text="Copy Result",
            bg=CARD_2
        )


    # =====================================================
    # CLEAR
    # =====================================================

    def clear_all(self):

        self.input_text.delete(
            "1.0",
            "end"
        )


        self.input_text.insert(
            "1.0",
            "Type or paste your text here..."
        )


        self.input_text.config(
            fg=MUTED
        )


        self.output_text.config(
            state="normal"
        )


        self.output_text.delete(
            "1.0",
            "end"
        )


        self.output_text.config(
            state="disabled"
        )


        self.count_label.config(
            text="0 characters"
        )


        self.status_label.config(
            text=" Ready"
        )


        self.copy_button.config(
            state="disabled"
        )


    # =====================================================
    # ERROR
    # =====================================================

    def show_error(self, error):

        self.copy_button.config(
            state="disabled"
        )


        self.status_label.config(
            text=" Translation Failed"
        )


        messagebox.showerror(
            "Translation Error",
            "Unable to translate the text.\n\n"
            + str(error)
        )


# =========================================================
# START APPLICATION
# =========================================================

def main():

    root = tk.Tk()

    TranslatorApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()