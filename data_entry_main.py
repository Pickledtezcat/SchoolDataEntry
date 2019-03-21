from tkinter import *
from tkinter.ttk import *

import file_utils
from PIL import Image, ImageTk

from time import sleep


class MainWindow(object):
    def __init__(self, parent_frame):
        self.image_list = None
        self.get_picture_list()
        self.top_frame = Frame(parent_frame)
        self.top_frame.grid(row=0, column=0, sticky='news', columnspan=5, rowspan=5)
        parent_frame.grid_columnconfigure(1, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        self.parent_frame = parent_frame
        self.parent_frame.bind("<Return>", self.submit)

        self.current_save_name = "week1"
        self.current_save_data = self.get_save_data()

        self.main_controls = MainControls(self, self.top_frame)
        self.saves_list = SavesList(self, self.top_frame)
        self.words_list = WordsList(self, self.top_frame)

        self.console = Frame(self.top_frame)
        self.console.grid(row=0, column=3, columnspan=2)
        self.add_menus()

    def submit(self, event):
        self.add_collection()
        self.save_content()

    def add_menus(self):
        my_menu = Menu(self.parent_frame)
        self.parent_frame.config(menu=my_menu)

        # add file menu
        file = Menu(my_menu)
        file.add_command(label="Exit", command=self.client_exit)
        my_menu.add_cascade(label="File", menu=file)

        # add edit menu
        edit = Menu(my_menu)
        edit.add_command(label="Undo")
        my_menu.add_cascade(label="Edit", menu=edit)

        edit.add_command(label="Show Img", command=self.showing)

    def get_words(self):
        self.current_save_data = self.get_save_data()
        words = self.current_save_data["words"]
        return words

    def get_sentences(self):
        self.current_save_data = self.get_save_data()
        sentences = self.current_save_data["sentences"]
        return sentences

    def get_target(self):
        self.current_save_data = self.get_save_data()
        target_language = self.current_save_data["target_language"]
        return target_language

    def get_saves(self):
        content = file_utils.load_file("saved_data")
        saves = list(save_key for save_key in content)

        return sorted(saves)

    def get_save_data(self):
        content = file_utils.load_file("saved_data")

        save_name = self.current_save_name
        if not content.get(save_name):
            save = self.new_collection()
            content[save_name] = save
            file_utils.save_file(content, "saved_data")
        else:
            save = content[save_name]

        return save

    def add_collection(self):
        new_collection_name = self.main_controls.new_entry.get()
        if new_collection_name:
            save = self.new_collection()
            content = file_utils.load_file("saved_data")
            content[new_collection_name] = save
            file_utils.save_file(content, "saved_data")

            self.current_save_name = new_collection_name
            self.reset()

    def new_collection(self):
        return {"words": [], "sentences": [], "target_language": []}

    def spawn_controls(self):
        if self.main_controls:
            self.main_controls.frame.destroy()
        self.main_controls = MainControls(self, self.top_frame)

    def spawn_saves_lists(self):
        if self.saves_list:
            self.saves_list.frame.destroy()
        self.saves_list = SavesList(self, self.top_frame)

    def spawn_word_lists(self):
        if self.words_list:
            self.words_list.frame.destroy()
        self.words_list = WordsList(self, self.top_frame)

    def spawn_console(self):
        if self.console:
            self.console.destroy()

        self.console = Frame(self.top_frame)
        self.console.grid(row=0, column=3, columnspan=2)

    def client_exit(self):
        exit()

    def showing(self):
        image = file_utils.get_path() + "//pictures//" + "biggest.jpg"

        load = Image.open(image)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self.console, image=render)
        img.image = render
        img.pack()

    def update_pictures(self):
        save_list, processing = file_utils.get_image_list()
        self.main_controls.process_pictures(processing)

        image_dict = {"images": save_list}
        file_utils.save_file(image_dict, "image_names")

        self.get_picture_list()
        self.reset()

    def get_picture_list(self):
        pictures = file_utils.load_file("image_names")
        if pictures:
            self.image_list = pictures["images"]
        else:
            self.image_list = []

    def show_text(self, text_content):
        text = Label(self.console, text=text_content)
        text.pack()

    def reset(self):
        self.spawn_controls()
        self.spawn_saves_lists()
        self.spawn_word_lists()
        self.spawn_console()
        self.current_save_data = self.get_save_data()

    def save_content(self):
        words = [entry.get() for entry in self.words_list.words_boxes.entries if entry.get() != ""]
        self.current_save_data["words"] = words
        sentences = [entry.get() for entry in self.words_list.sentence_boxes.entries if entry.get() != ""]
        self.current_save_data["sentences"] = sentences
        targets = [entry.get() for entry in self.words_list.target_boxes.entries if entry.get() != ""]
        self.current_save_data["target_language"] = targets
        content = file_utils.load_file("saved_data")
        content[self.current_save_name] = self.current_save_data
        file_utils.save_file(content, "saved_data")

        self.reset()

    def clear_saves(self):
        file_utils.save_file({}, "saved_data")
        self.reset()


class MainControls(object):
    def __init__(self, manager, parent_frame):
        self.manager = manager
        self.parent_frame = parent_frame
        self.frame = Frame(parent_frame)
        self.frame.grid(row=0, column=0)
        self.new_entry = None
        self.picture_progress = None

        self.file_buttons()

    def file_buttons(self):
        new_label = Label(self.frame, width=25, text="Add new collection:", anchor='e')
        new_label.grid(row=1, column=0)

        self.new_entry = Entry(self.frame, width=15)
        self.new_entry.grid(row=1, column=1)

        add_button = Button(self.frame, text='ADD', width=25, command=self.manager.add_collection)
        add_button.grid(row=2, column=0)

        clear_button = Button(self.frame, text='CLEAR ALL', width=25, command=self.manager.clear_saves)
        clear_button.grid(row=3, column=0)

        pictures_button = Button(self.frame, text='UPDATE PICTURES', width=25, command=self.manager.update_pictures)
        pictures_button.grid(row=4, column=0)

    def process_pictures(self, picture_progress):
        number_of_pictures = len(picture_progress)
        value = 1.0 / number_of_pictures

        self.picture_progress = Progressbar(self.frame, mode="determinate", length=200, maximum=1.0)
        self.picture_progress.grid(row=5, column=0)
        self.picture_progress.start()

        while len(picture_progress) > 0:
            image_path, new_name = picture_progress.pop()
            file_utils.process_image(image_path, new_name)
            self.picture_progress.step(value)
            self.picture_progress.update()

        self.picture_progress.stop()

    def add_new_entry(self):
        print(self.new_entry.get())


class SavesList(object):
    def __init__(self, manager, parent_frame):
        self.manager = manager
        self.parent_frame = parent_frame
        self.frame = Frame(parent_frame)
        self.frame.grid(row=1, column=0)
        self.combo_box = None
        self.add_saves()

    def add_saves(self):
        my_label = Label(self.frame, width=25, text="Choose a collection:", anchor='w')
        my_label.grid(row=1, column=0)

        def load_save(event):
            self.manager.current_save_name = event.widget.get()
            self.manager.reset()

        saves = self.manager.get_saves()
        self.combo_box = Combobox(self.frame, width=25, values=saves)
        self.combo_box.insert(10, self.manager.current_save_name)
        self.combo_box.grid(row=2, column=0)
        self.combo_box.bind("<<ComboboxSelected>>", load_save)


class WordsList(object):
    def __init__(self, manager, parent_frame):
        self.manager = manager
        self.parent_frame = parent_frame
        self.frame = Frame(parent_frame)
        self.frame.grid(row=0, column=1, rowspan=3)

        self.words_control = WordsControls(self.manager, self.frame)
        self.words_boxes = WordsBoxes(self.manager, self.frame)
        self.sentence_boxes = SentenceBoxes(self.manager, self.frame)
        self.target_boxes = TargetBoxes(self.manager, self.frame)


class WordsControls(object):
    def __init__(self, manager, parent_frame):
        self.manager = manager
        self.parent_frame = parent_frame
        self.frame = Frame(parent_frame)
        self.frame.grid(row=0, column=0)
        self.init_window()

    def init_window(self):
        saving_button = Button(self.frame, text='SAVE', width=12, command=self.manager.save_content)
        saving_button.grid(row=0, column=0)


class WordsBoxes(object):
    def __init__(self, manager, parent_frame):
        self.manager = manager
        self.parent_frame = parent_frame
        self.frame = Frame(parent_frame)
        self.frame.grid(row=0, column=1, rowspan=3)
        self.entries = []
        self.setup()

    def setup(self):
        current_label = Label(self.frame, width=20, text="WORD LIST:", justify='center')
        current_label.grid(row=0, column=1)

        words = self.manager.get_words()
        index = 0

        for i in range(len(words)):
            self.add_entry(index, words[i])
            index += 1

        self.add_entry(index, "")
        self.entries[-1].focus_set()

    def add_entry(self, index, word):

        word_label = "word {}".format(index + 1)
        my_label = Label(self.frame, width=12, text=word_label, anchor='e')
        my_entry = Entry(self.frame, width=20)

        my_label.grid(row=index + 1, column=0)
        my_entry.grid(row=index + 1, column=1)

        if word.lower() not in self.manager.image_list and word != "":
            my_entry["style"] = "Missing.TLabel"

        my_entry.insert(10, word)
        self.entries.append(my_entry)


class SentenceBoxes(object):
    def __init__(self, manager, parent_frame):
        self.manager = manager
        self.parent_frame = parent_frame
        self.frame = Frame(parent_frame)
        self.frame.grid(row=0, column=2)
        self.entries = []
        self.setup()

    def setup(self):
        current_label = Label(self.frame, width=20, text="SENTENCE LIST:", justify='center')
        current_label.grid(row=0, column=1)

        sentences = self.manager.get_sentences()
        index = 0

        for i in range(len(sentences)):
            self.add_entry(index, sentences[i])
            index += 1

        self.add_entry(index, "")

    def add_entry(self, index, sentence):
        sentence_label = "Sentence {}".format(index + 1)
        my_label = Label(self.frame, width=15, text=sentence_label, anchor='e')
        my_entry = Entry(self.frame, width=35)

        my_label.grid(row=index + 1, column=0)
        my_entry.grid(row=index + 1, column=1)

        my_entry.insert(END, sentence)

        self.entries.append(my_entry)


class TargetBoxes(object):
    def __init__(self, manager, parent_frame):
        self.manager = manager
        self.parent_frame = parent_frame
        self.frame = Frame(parent_frame)
        self.frame.grid(row=1, column=2)
        self.entries = []
        self.setup()

    def setup(self):
        current_label = Label(self.frame, width=20, text="TARGET LANGUAGE ($):", justify='center')
        current_label.grid(row=0, column=1)

        sentences = self.manager.get_target()
        index = 0

        for i in range(len(sentences)):
            self.add_entry(index, sentences[i])
            index += 1

        self.add_entry(index, "")

    def add_entry(self, index, sentence):
        sentence_label = "Target {}".format(index + 1)
        my_label = Label(self.frame, width=15, text=sentence_label, anchor='e')
        my_entry = Entry(self.frame, width=35)

        my_label.grid(row=index + 1, column=0)
        my_entry.grid(row=index + 1, column=1)

        my_entry.insert(END, sentence)

        self.entries.append(my_entry)


root = Tk()
root.geometry("1300x600")
#style = Style()
#print(style.theme_names())
#style.theme_use("clam")

new_style = Style()

new_style.configure("TButton", padding=6, relief="flat")

new_style.configure("Missing.TLabel", background="LightGrey")

app = MainWindow(root)

root.mainloop()

