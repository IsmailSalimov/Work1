import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QListWidget, QApplication, QWidget, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

app = QApplication([])
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')

field_text = QTextEdit()
list_notes = QListWidget()
list_tags = QListWidget()

field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...')

button_add_note = QPushButton('Создать заметку')
button_del_note = QPushButton('Удалить заметку')
button_save_note = QPushButton('Сохранить заметку')
button_add_tag = QPushButton('Добавить к заметке')
button_del_tag = QPushButton('Открепить от заметки')
button_search_tag = QPushButton('Искать заметки по тегу')

t1 = QLabel('Список заметок')
t2 = QLabel('Список тегов')

lineG2 = QHBoxLayout()
lineG1 = QHBoxLayout()
lineG3 = QHBoxLayout()

lineV1 = QVBoxLayout()
lineV2 = QVBoxLayout()

lineV1.addWidget(field_text)

lineV2.addWidget(t1)

lineV2.addWidget(list_notes)

lineV2.addLayout(lineG2)
lineG2.addWidget(button_add_note)
lineG2.addWidget(button_del_note)
lineV2.addWidget(button_save_note)

lineV2.addWidget(t2)

lineV2.addWidget(list_tags)

lineV2.addWidget(field_tag)

lineV2.addLayout(lineG3)
lineG3.addWidget(button_add_tag)
lineG3.addWidget(button_del_tag)
lineV2.addWidget(button_search_tag)

lineG1.addLayout(lineV1)
lineG1.addLayout(lineV2)

notes_win.setLayout(lineG1)

notes = {
    "": 
    {
        "текст" : "",
        "теги" : ["", ""]
    }
        }

with open("notes_data.json", "r", encoding="utf-8") as file:
    notes = json.load(file)

list_notes.addItems(notes)

def show_notes():
    name1 = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name1]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[name1]["теги"])

def add_note():
    note_name, result = QInputDialog.getText(notes_win, "Добавить заметку", "Название заметки:")
    if result and note_name != "":
        notes[note_name] = {"текст" : "", "теги" : []}
        list_notes.addItem(note_name)

button_add_note.clicked.connect(add_note)

def save_note():
    if list_notes.selectedItems():
        note_name = list_notes.selectedItems()[0].text() 
        text = field_text.toPlainText()
        notes[note_name] = {'текст' : text, "теги" : []}
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print("Заметка для сохранения не выбрана!")

button_save_note.clicked.connect(save_note)

def del_note():
    if list_notes.selectedItems():
        note_name = list_notes.selectedItems()[0].text()
        del notes[note_name]
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True)
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
    else:
        print("Заметка для удаления не выбрана!")

button_del_note.clicked.connect(del_note)

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open("notes_data.json", "w") as file:
                json.dump(notes, file, sort_keys=True)
        else:
            print("Такой тег у заметки есть!")
    else:
        print("Заметка для добавления тега не выбрана!")

button_add_tag.clicked.connect(add_tag)

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        if list_tags.selectedItems():
            tag = list_tags.selectedItems()[0].text()
            notes[key]["теги"].remove(tag)
            list_tags.clear()
            list_tags.addItems(notes[key]["теги"])
            with open("notes_data.json", "w") as file:
                json.dump(notes, file, sort_keys=True)
        else:
            print("Тег для удаления не выбран!")
    else:
        print("Заметка для удаления тега не выбрана!")

button_del_tag.clicked.connect(del_tag)

def search_tag():
    tag = field_tag.text()
    if button_search_tag.text() == "Искать заметки по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note]=notes[note]
        button_search_tag.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_search_tag.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_search_tag.setText("Искать заметки по тегу")
    else:
        pass

button_search_tag.clicked.connect(search_tag)

list_notes.itemClicked.connect(show_notes)

notes_win.show()
app.exec_()