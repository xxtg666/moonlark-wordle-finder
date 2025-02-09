import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QApplication, QLineEdit, QHBoxLayout, QWidget, QSpinBox, QLabel, QPushButton, QListWidget
)
from PySide6.QtUiTools import QUiLoader
import json


app = QApplication(sys.argv)
loader = QUiLoader()
ui_file = QFile("form.ui")
main_window = loader.load(ui_file)
ui_file.close()


spin_box = main_window.findChild(QSpinBox, "edit_length")
container = main_window.findChild(QWidget, "widget")
label_status = main_window.findChild(QLabel, "label_status")
edit_include = main_window.findChild(QLineEdit, "edit_include")
edit_exclude = main_window.findChild(QLineEdit, "edit_exclude")
button_find = main_window.findChild(QPushButton, "button_find")
word_list = main_window.findChild(QListWidget, "word_list")


layout = QHBoxLayout(container)
layout.setContentsMargins(0, 0, 0, 0)
container.setLayout(layout)


json_path = os.path.join(os.path.dirname(__file__), "EnWords.json")
with open(json_path, "r", encoding="utf-8") as f:
    en_words = json.load(f)
    

def update_ui(length: int):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
    for _ in range(length):
        le = QLineEdit()
        le.setMaxLength(1)
        le.setAlignment(Qt.AlignCenter)
        layout.addWidget(le)
    words = en_words.get(str(length), {})
    count = len(words)
    label_status.setText(f"已加载 {count} 个单词")


update_ui(spin_box.value())
spin_box.valueChanged.connect(update_ui)

def find_words():
    length = spin_box.value()
    fixed = []
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        text = widget.text().strip().lower() if widget else ""
        fixed.append(text)
    include = edit_include.text().strip().lower()
    exclude = edit_exclude.text().strip().lower()
    words_dict = en_words.get(str(length), {})
    result = []
    for word in words_dict.keys():
        word_lower = word.lower()
        valid = True
        for idx, letter in enumerate(fixed):
            if letter and word_lower[idx] != letter:
                valid = False
                break
        if not valid:
            continue
        for ch in include:
            if ch and ch not in word_lower:
                valid = False
                break
        if not valid:
            continue
        for ch in exclude:
            if ch and ch in word_lower:
                valid = False
                break
        if valid:
            result.append(word)
    word_list.clear()
    word_list.addItems(result)

button_find.clicked.connect(find_words)


main_window.show()
sys.exit(app.exec())

