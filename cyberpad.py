from tkinter import *
import base64
from tkinter import filedialog, font
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import ttk
import os

def change_color():
    color = colorchooser.askcolor(title="Pick a font color")
    text_area.config(fg=color[1])
def change_font(*args):
    text_area.config(font=(font_name.get(),size_box.get()))

def new_file():
    text_widget = get_currentText()
    window.title("Untitled")
    text_widget.delete(1.0,END)
def open_file(*args):
    file = askopenfilename(defaultextension=".txt",
                           file=[("All Files", "*.*"),
                                 ("Text Documents", "*.txt")])
    if file is None:
        return
    else:
        try:
            text_widget = get_currentText()
            window.title(os.path.basename(file))
            text_widget.delete(1.0, END)
            file = open(file, "r")
            text_widget.insert(1.0, file.read())
        except Exception:
            print("couldn't read file")

        finally:
            file.close()
         
def save_file(*args):   
    file = filedialog.asksaveasfilename(initialfile="untitled.txt",defaultextension=".txt",
                                    filetypes=[
                                        ("Text File",".txt"),
                                        ("All Files", ".*")])
    if file is None:
        return
    else:
        try:
            text_widget = get_currentText()
            window.title(os.path.basename(file))
            file = open(file, "w")
            file.write(text_widget.get(1.0,END))
        except Exception:
            print("Unable to save file")
        finally:
            file.close()
        
    
def cut():
    text_widget = get_currentText()
    text_widget.event_generate("<<Cut>>")
def copy():
    text_widget = get_currentText()
    text_widget.event_generate("<<Copy>>")
def paste():
    text_widget = get_currentText()
    text_widget.event_generate("<<Paste>>")

def base64_decode():
    text_widget = get_currentText()
    try:
        convertsample = str(text_widget.get(1.0,END))
        # converting the base64 code into ascii characters
        convertbytes = convertsample.encode("ascii")
        # converting into bytes from base64 system
        convertedbytes = base64.b64decode(convertbytes)
        # decoding the ASCII characters into alphabets
        decodedsample = convertedbytes.decode("ascii") 
        text_widget.delete(1.0, END)
        text_widget.insert(1.0, decodedsample)
    except:
        print("idk add message box here etc.")
def defang(*args):
    text_widget = get_currentText()
    domain = str(text_widget.get(1.0,END)) # need to work on this
    text_widget.delete(1.0,END)
    text_widget.insert(1.0,domain.replace(".","[.]"))

def add_tab():
    global new_tab_button_x, counter
    new_tab = ttk.Frame(notebook)
    notebook.add(new_tab, text="Tab " + str(notebook.index("end") +1))
    # Create text area for new tab and store it inside the text_areas dict
    new_text_area = Text(new_tab)
    new_text_area.pack(fill="both",expand=True)
    text_widgets.append(new_text_area)
    # Scroll bar addition
    scroll_bar = Scrollbar(new_text_area)
    scroll_bar.pack(side=RIGHT, fill=Y)
    # Text Area color
    new_text_area.config(yscrollcommand=scroll_bar.set,bg=giga_color,fg="#f8f8f2")
    new_text_area.tag_configure("sel",foreground="#282a36", background="#6272a4")
    counter += 1
    print(counter)
    if counter >= 9:
        update_tab_button(56)
    else:    
        update_tab_button(50)

    
def get_currentText():
    tab_index = notebook.index(notebook.select())  # Get the index of the currently selected tab
    return text_widgets[tab_index]  # Get the Text widget associated with the selected tab
   
window = Tk()

# Keybinds

window.bind("<Control-s>",save_file)
window.bind("<Control-o>",open_file)
window.bind("<Control-d>",defang)
# Window Config

window.title("Notebook Example")
window_width = 750
window_height = 750
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry("{}x{}+{}+{}".format(window_width,window_height,x,y))
window.grid_rowconfigure(0, weight=1) # weight set to 1 so it doesn't back expand
window.grid_columnconfigure(0, weight=1) # weight set to 1 so it doesn't back expand

# Notebook and Tab Config
style = ttk.Style()
style.theme_create( "style_obj", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [10, 5],"borderWidth": 0, "focuscolor": "none","background": "#6272a4" },
                          "map": {
                              "background": [("selected", "#282a36")],
                              "foreground": [("selected", "white")],
                          }}})

style.theme_use("style_obj")

# Images
openImage = PhotoImage(file="openfile.png")
saveImage = PhotoImage(file="save_file.png")
notebook = ttk.Notebook(window,width=600,height=600)
new_tab_button_x = 0
counter = 0
# General Setup
window.title("Cyberpad")
file = None
text_widgets = []
# Set dimensions and positions
giga_color = "#44475a"
# Font settings
font_name = StringVar(window)
font_size = StringVar(window)
font_name.set("Code New Roman")
font_size.set(12)

# Icon and window bg color
icon = PhotoImage(file='icon.png') 
window.iconphoto(True,icon) 
window.config(background="#44475a") 

# Init tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")
# Text Area in Tab 1
text_area1 = Text(tab1)
text_area1.pack(fill="both", expand=True)
text_widgets.append(text_area1)
# Label in Tab 1
label1 = Label(tab1)
label1.pack()

notebook.pack(expand=True, fill="both")

# Scroll bar addition
scroll_bar = Scrollbar(text_area1)
scroll_bar.pack(side=RIGHT, fill=Y)
# Text Area color
text_area1.config(yscrollcommand=scroll_bar.set,bg=giga_color,fg="#f8f8f2")
# Highlight color
text_area1.tag_configure("sel",foreground="#282a36", background="#6272a4")


# Top menus (Frames atm, change to menu)
frame = Frame(notebook)
frame.grid()



# Button Styles
custom_button_style = ttk.Style()
custom_button_style.configure(
    "Custom.TButton",
    background="#6272a4",
    foreground="#f8f8f2",
    focuscolor="none",
    font=("Code New Roman",12))

# look at a config file that pulls saved options like font size etc


# Buttons  (maybe just create a new window that pops up to change all of this)
color_button = Button(window, text="color", command=change_color)

#color_button.grid(row=0,column=0)

font_box = OptionMenu(window, font_name, *font.families(), command=change_font) # returns all available fonts

#font_box.grid(row=0,column=1)

size_box = Spinbox(window, from_=1, to=100, textvariable=font_size,command=change_font)

#size_box.grid(row=0,column=2)

# Tab Button
tab_button = ttk.Button(window, text=" + ", command=add_tab,style="Custom.TButton",)

# Handle position of Tab Button << TEMPORARY, TABS TO ADD SELECTED FILES NAMES. Len of tab.text + x offset will work better? >>
def update_tab_button(bump):
    global new_tab_button_x
    new_tab_button_x += bump
    tab_button.place(x=new_tab_button_x,y=6)

# Menu setup
menu_bar = Menu(window, background="blue", fg="white")
window.config(menu=menu_bar)
update_tab_button(55)
# File (menu block 1)
file_menu = Menu(menu_bar,tearoff=0) #,background="#6272a4"
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New File", command=new_file,image=openImage,compound="right",font=("Code New Roman",12))
file_menu.add_command(label="Open File", command=open_file,image=openImage,compound="right",font=("Code New Roman",12))
file_menu.add_command(label="Save File", command=save_file,image=saveImage,compound="right",font=("Code New Roman",12))

# Edit (menu block 2)
edit_menu = Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu,font=("Code New Roman",12))
edit_menu.add_command(label="Cut", command=cut,font=("Code New Roman",12))
edit_menu.add_command(label="Copy", command=copy,font=("Code New Roman",12))
edit_menu.add_command(label="Paste", command=paste,font=("Code New Roman",12))

# Functions (menu block 3)
functionMenu = Menu(menu_bar,tearoff=0,font=("Code New Roman",12))
menu_bar.add_cascade(label="Functions",menu=functionMenu,font=("Code New Roman",12))

functionMenu.add_command(label="Base64 Decode",command=base64_decode,font=("Code New Roman",12))
functionMenu.add_command(label="Defang",command=defang,font=("Code New Roman",12))
window.mainloop()
