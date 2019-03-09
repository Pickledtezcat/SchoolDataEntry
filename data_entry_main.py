from tkinter import *
from tkinter.ttk import *

import file_utils

from PIL import Image, ImageTk


class Words(object):
    def __init__(self, master, control):
        self.control = control
        self.frame = Frame(master)
        self.frame.grid(row=0, column=2)
        self.master = master
        self.title = "Word List"
        self.word_number = 1
        self.word_list = []
        self.entries = []
        self.row_number = 2

        self.init_window()

    def init_window(self):

        saving_button = Button(self.frame, text='SAVE', width=25, command=self.save_content)
        saving_button.grid(row=self.row_number, column=1)
        self.row_number += 1

        loading_button = Button(self.frame, text='LOAD', width=25, command=self.reset)
        loading_button.grid(row=self.row_number, column=1)
        self.row_number += 1

        adding_button = Button(self.frame, text='more...', width=25, command=self.add_entry_field)
        adding_button.grid(row=self.row_number, column=1)
        self.row_number += 1

        self.load_entries()

    def reset(self):
        self.control.reload_word_lists()

    def save_content(self):
        content = {}
        for entry in self.entries:
            label = entry[0]
            word = entry[1].get()

            if word != "":
                content[label] = word

        file_utils.save_file(content)

    def load_entries(self):
        data = file_utils.load_file()
        if data:
            key_list = [entry_key for entry_key in data]
            key_list = sorted(key_list)

            for entry_key in key_list:
                word = data[entry_key]
                if word != "":
                    self.word_list.append(word)

            self.add_entry_fields()

        else:
            self.add_entry_field()

    def add_entry_field(self):
        label = "word {}".format(self.word_number)

        my_label = Label(self.frame, width=15, text=label, anchor='w')
        my_entry = Entry(self.frame)

        my_label.grid(row=self.row_number, column=0)
        my_entry.grid(row=self.row_number, column=1)

        self.entries.append((label, my_entry))
        self.row_number += 1
        self.word_number += 1

    def add_entry_fields(self):
        for i in range(len(self.word_list)):
            label = "word {}".format(i + 1)
            word = self.word_list[i]

            my_label = Label(self.frame, width=15, text=label, anchor='w')
            my_entry = Entry(self.frame)
            my_entry.insert(10, word)

            my_label.grid(row=self.row_number, column=0)
            my_entry.grid(row=self.row_number, column=1)

            self.entries.append((label, my_entry))
            self.row_number += 1
            self.word_number += 1


class SavesList(object):
    def __init__(self, master, control):
        self.control = control
        self.frame = Frame(master)
        self.frame.grid(row=2, column=0)
        self.master = master
        self.combo_box = None
        self.add_saves()

    def add_saves(self):
        def load_save(event):
            print(event.widget.current())

        saves = self.control.saves
        self.combo_box = Combobox(self.frame, width=25, values=saves)
        self.combo_box.grid(row=2, column=0)
        self.combo_box.bind("<<ComboboxSelected>>", load_save)


class MainWindow(object):
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.frame.grid(row=0, column=0)
        self.master = master
        self.rows = 0
        self.combo_box = None
        self.saves = self.get_saves()

        self.master.title("Data Entry")
        self.new_entry = None
        self.word_lists = None
        self.saves_list = None
        self.init_window()

    def get_saves(self):
        saves = ["week{}".format(n) for n in range(50)]
        return saves

    def get_path(self):
        path = "D:/projects//gitpages//numlocked//Pickledtezcat.github.io/"
        return path

    def reload_word_lists(self):
        if self.word_lists:
            self.word_lists.frame.destroy()
        self.word_lists = Words(self.master, self)

    def file_buttons(self):
        clear_button = Button(self.frame, text='CLEAR', width=15, command=self.reload_word_lists)
        clear_button.grid(row=0, column=0)

        new_label = Label(self.frame, width=15, text="Add new entry:")
        new_label.grid(row=1, column=0)

        self.new_entry = Entry(self.frame, width=15)
        self.new_entry.grid(row=1, column=1)

        add_button = Button(self.frame, text='ADD', width=15, command=self.add_new_entry)
        add_button.grid(row=2, column=0)

    def add_new_entry(self):
        print(self.new_entry.get())

    def init_window(self):
        self.file_buttons()
        self.saves_list = SavesList(self.master, self)
        self.word_lists = Words(self.master, self)

        my_menu = Menu(self.master)
        self.master.config(menu=my_menu)

        # add file menu
        file = Menu(my_menu)
        file.add_command(label="Exit", command=self.client_exit)
        my_menu.add_cascade(label="File", menu=file)

        # add edit menu
        edit = Menu(my_menu)
        edit.add_command(label="Undo")
        my_menu.add_cascade(label="Edit", menu=edit)

        edit.add_command(label="Show Img", command=self.showImg)
        edit.add_command(label="Show Contents", command=self.show_contents)

    def x(self, my_menu):

        # example of dynamic menu
        save_menu = Menu(my_menu)
        my_menu.add_cascade(label="Saves", menu=save_menu)

        def button_press(my_label):
            print(my_label)

        saves = ["week1", "week2", "week3", "week4", "week5", "week6", "week7"]

        for save_name in saves:
            save_menu.add_command(label=save_name, command=lambda in_label=save_name: button_press(in_label))

    def show_contents(self):
        contents = list(entry[1].get() for entry in self.word_lists.entries)
        text = Label(self.frame, text="contents:{}".format(contents))
        text.grid(row=2, column=1)

    def client_exit(self):
        exit()

    def showImg(self):
        image = self.get_path() + "//pictures//" + "biggest.jpg"

        load = Image.open(image)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self.frame, image=render)
        img.image = render
        img.grid(row=3, column=0)

    def showText(self):
        text = Label(self.frame, text="Hey there good lookin!")
        text.pack()


root = Tk()
root.geometry("800x400")

s = Style()
s.theme_use("alt")

print(s.theme_names())

app = MainWindow(root)

root.mainloop()
