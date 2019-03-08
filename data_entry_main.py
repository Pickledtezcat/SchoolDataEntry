from tkinter import *
import file_utils

from PIL import Image, ImageTk


class Words(object):
    def __init__(self, master, control):
        self.control = control
        self.frame = Frame(master)
        self.frame.pack()
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
            label = "word {}".format(i)
            word = self.word_list[i]

            my_label = Label(self.frame, width=15, text=label, anchor='w')
            my_entry = Entry(self.frame)
            my_entry.insert(10, word)

            my_label.grid(row=self.row_number, column=0)
            my_entry.grid(row=self.row_number, column=1)

            self.entries.append((label, my_entry))
            self.row_number += 1
            self.word_number += 1


class MainWindow(object):
    def __init__(self, master=None):
        self.frame = Frame(master)
        self.frame.pack()
        self.master = master

        self.master.title("Data Entry")
        self.word_lists = None
        self.init_window()

    def get_path(self):
        path = "D:/projects//gitpages//numlocked//Pickledtezcat.github.io/"
        return path

    def reload_word_lists(self):
        if self.word_lists:
            self.word_lists.frame.destroy()
        self.word_lists = Words(self.master, self)

    def clear_button(self):
        loading_button = Button(self.frame, text='CLEAR', width=25, command=self.reload_word_lists)
        loading_button.grid(row=0, column=0)

    def init_window(self):
        self.word_lists = Words(self.master, self)
        self.clear_button()

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
root.geometry("600x400")

app = MainWindow(root)
root.mainloop()
