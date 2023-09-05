from tkinter import *
import base64
from tkinter import filedialog, font
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import ttk
import os
import codecs
from tkinter import messagebox
import urllib.parse
import webbrowser
import ipaddress

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
            pass
        finally:
            try:
                file.close()
            except AttributeError:
                pass
         
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
            pass
        finally:
            try:
                file.close()
            except AttributeError:
                pass
        
def messagebox_handler(title,message):
    messagebox.showinfo(title=title,message=message)   
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
        if text_widget.tag_ranges(SEL):
            convertsample = str(text_widget.get(SEL_FIRST,SEL_LAST))
            convertsample = str(text_widget.get(1.0,END))
            # converting the base64 code into ascii characters
            convertbytes = convertsample.encode("ascii")
            # converting into bytes from base64 system
            convertedbytes = base64.b64decode(convertbytes)
            # decoding the ASCII characters into alphabets
            decodedsample = convertedbytes.decode("ascii") 
            text_widget.insert(SEL_FIRST, decodedsample)
            text_widget.tag_config("start", foreground="red")
            text_widget.delete(SEL_FIRST, SEL_LAST)
            start_position = text_widget.index(INSERT)
            end_position = text_widget.index(f"{INSERT}+{len(decodedsample)}c")
            text_widget.tag_add("start", start_position, end_position)
            
        else:
            convertsample = str(text_widget.get(1.0,END))
            # converting the base64 code into ascii characters
            convertbytes = convertsample.encode("ascii")
            # converting into bytes from base64 system
            convertedbytes = base64.b64decode(convertbytes)
            # decoding the ASCII characters into alphabets
            decodedsample = convertedbytes.decode("ascii") 
            text_widget.delete(1.0, END)
            text_widget.insert(1.0, decodedsample)
            text_widget.tag_config("start", foreground="#ffb86c")
            text_widget.tag_add("start",1.0, END)          
    except:
        messagebox_handler("Failed","Please select a valid Base64 Encoded string.")

def base_urlQuery():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    text_widget = get_currentText()
    try:
        if text_widget.tag_ranges(SEL): 
            text_content = text_widget.get("1.0", "end-1c")
            text_content = text_content.replace("https://","")
            text_content = text_content.replace("http://","")
            try:
                if ipaddress.ip_address(text_content):
                    virusTotal = "https://www.virustotal.com/gui/ip-address/"
                    request = virusTotal + text_content
                    webbrowser.open(request, new= 2)
            except ValueError:  # ipaddress will always throw this if it's a domain or null
                    virusTotal = "https://www.virustotal.com/gui/domain/"
                    request = virusTotal + text_content
                    webbrowser.open(request, new= 2)         
        else:
            messagebox_handler("Failed","Please select a single URL/IP.")
    except Exception as e:
        pass #add
        
        
    #later if encoding needed
    #encoded_content = urllib.parse.quote(text_content)
    #print(encoded_content)
def hex_decode():
    try: # Handling diff due to working with raw 
        text_widget = get_currentText()
        if text_widget.tag_ranges(SEL):
            text_content = text_widget.get("1.0", "end-1c")  # Get the text content
            text_content = text_content.replace("\\x", "")
            decoded_sample = bytes.fromhex(text_content).decode('utf-8')
            text_widget.insert(SEL_FIRST, decoded_sample)
            text_widget.delete(SEL_FIRST, SEL_LAST)
        else:
            text_content = text_widget.get("1.0", "end-1c")  # Get the text content
            text_content = text_content.replace("\\x", "")
            decoded_sample = bytes.fromhex(text_content).decode('utf-8')
            text_widget.delete(1.0, END)
            text_widget.insert(1.0, decoded_sample)
            text_widget.tag_config("start", foreground="#ffb86c")
            text_widget.tag_add("start",1.0, END)        
    except:
        messagebox_handler("Failed","Please select a valid HEX Encoded string.")
        
def defang():
    text_widget = get_currentText()
    # Check if something is selected
    if text_widget.tag_ranges(SEL):
        # Get selected text and replace then delete
        domain = str(text_widget.get(SEL_FIRST,SEL_LAST)) # ref to selected string
        text_widget.insert(SEL_FIRST,domain.replace(".","[.]"))
        text_widget.delete(SEL_FIRST,SEL_LAST)
    # If nothing selected, it will iterate over the whole body
    else:
        text_widget = get_currentText()
        domain = str(text_widget.get(1.0,END)) # need to work on this
        text_widget.delete(1.0,END)
        text_widget.insert(1.0,domain.replace(".","[.]"))

def add_tab():
    global new_tab_button_x, counter
    new_tab = ttk.Frame(notebook)
    notebook.add(new_tab, text="Tab " + str(notebook.index("end") +1))
    # Create text area for new tab and store it inside the text_areas dict
    new_text_area = Text(new_tab,undo=True)
    new_text_area.pack(fill="both",expand=True)
    text_widgets.append(new_text_area)
    # Scroll bar addition
    scroll_bar = Scrollbar(new_text_area)
    scroll_bar.pack(side=RIGHT, fill=Y)
    # Text Area color
    new_text_area.config(yscrollcommand=scroll_bar.set,bg=giga_color,fg="#f8f8f2",font=("Code New Roman",15))
    new_text_area.tag_configure("sel",foreground="#282a36", background="#6272a4")
    counter += 1
    print(counter)
    if counter >= 9:
        update_tab_button(56)
    else:    
        update_tab_button(50)
def echo_select():
    defang()
    
def get_currentText():
    tab_index = notebook.index(notebook.select())  # Get the index of the currently selected tab
    return text_widgets[tab_index]  # Get the Text widget associated with the selected tab
   
window = Tk()

# Keybinds

window.bind("<Control-s>",save_file)
window.bind("<Control-o>",open_file)
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

# Styles
style = ttk.Style()
style.theme_create( "style_obj", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [10, 5],"borderWidth": 0, "focuscolor": "none","background": "#6272a4" },
                          "map": {
                              "background": [("selected", "#282a36")],
                              "foreground": [("selected", "white")],
                          }}})

# Button Styles
custom_button_style = ttk.Style()
custom_button_style.configure(
    "Custom.TButton",background="#6272a4", foreground="#f8f8f2",focuscolor="none",
    font=("Code New Roman",12))

style.theme_use("style_obj")

# Images & general variables
openImage = PhotoImage(file="openfile.png")
saveImage = PhotoImage(file="save_file.png")
notebook = ttk.Notebook(window,width=600,height=600)
new_tab_button_x = 0
counter = 0
window.title("Cyberpad")
file = None
text_widgets = []
# Set dimensions and positions
giga_color = "#282a36"
# Font settings
font_name = StringVar(window)
font_size = StringVar(window)
font_name.set("Code New Roman")
font_size.set(15)

# Icon and window bg color
icon = PhotoImage(file='icon.png') 
window.iconphoto(True,icon) 
window.config(background="#44475a") 

# Init tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")
# Text Area in Tab 1
text_area1 = Text(tab1,undo=True)
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
text_area1.config(yscrollcommand=scroll_bar.set,bg=giga_color,fg="#f8f8f2",font=("Code New Roman",15))
# Highlight color
text_area1.tag_configure("sel",foreground="#282a36", background="#6272a4")

# Top menus (Frames atm, change to menu)
frame = Frame(notebook)
frame.grid()

# look at a config file that pulls saved options like font size etc

# Buttons  (maybe just create a new window that pops up to change all of this)
color_button = Button(window, text="color", command=change_color)

#color_button.grid(row=0,column=0)

font_box = OptionMenu(window, font_name, *font.families(), command=change_font) # returns all available fonts

#font_box.grid(row=0,column=1)

size_box = Spinbox(window, from_=1, to=100, textvariable=font_size,command=change_font)

#size_box.grid(row=0,column=2)

# Tab Button
tab_button = ttk.Button(window, text=" + ", command=add_tab,style="Custom.TButton")

# Handle position of Tab Button
def update_tab_button(bump):
    global new_tab_button_x
    new_tab_button_x += bump
    tab_button.place(x=new_tab_button_x,y=6)

# Menu setup
menu_bar = Menu(window)
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
functionMenu.add_command(label="Defang IP/URL",command=defang,font=("Code New Roman",12))
functionMenu.add_command(label="Hex Decode",command=hex_decode,font=("Code New Roman",12))
functionMenu.add_command(label="Check with VirusTotal",command=base_urlQuery,font=("Code New Roman",12))
window.mainloop()
