import os
import cv2
import imutils
import requests
import webbrowser
import numpy as np
from tkinter import *
from colorama import Fore
from tktooltip import ToolTip
from tkinter import messagebox
from app_info import AppInfo

# global confirmation dialog box flag
confirm_flag = True


# reads config.ini file and returns the last saved IP address.
def get_ip_address():
    ip = entry_ip.get()

    if os.path.isfile(AppInfo().CONFIG_FILE) and not ip:
        config = open(AppInfo().CONFIG_FILE, 'r')
        data = config.read()
        ip = data
    else:
        saveIpAddress = open(AppInfo().CONFIG_FILE, 'w')
        saveIpAddress.write(ip)
        saveIpAddress.close()

    entry_ip.delete(0, END)
    entry_ip.insert(0, ip)
    return ip


# main process that connects to the local server for image processing
def capture():
    address = get_ip_address()
    url = f'http://{address}:8080/shot.jpg'
    cascade = cv2.CascadeClassifier(AppInfo().CASCADE)
    print(f'{Fore.LIGHTGREEN_EX}Establishing connection to local server IP: {address} . . .')

    while True:
        global confirm_flag
        try:
            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)
            img = imutils.resize(img, width=1000, height=1800)

            fonts = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, f'IP Address : {address} [ESC] to exit', (50, 50),
                        fonts, 1,
                        (0, 255, 255),
                        2,
                        cv2.FILLED)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.namedWindow(f'{AppInfo().APP_NAME} Streaming . . .', cv2.WINDOW_NORMAL)

            bodies = cascade.detectMultiScale(gray, 1.1, 3)
            for (off_set_x, off_set_y, width, height) in bodies:
                cv2.rectangle(img, (off_set_x, off_set_y), (off_set_x + width, off_set_y + height), (0, 255, 0), 2)
            cv2.imshow(f'{AppInfo().APP_NAME} is live . . .', img)

            # Press Esc key to exit
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                messagebox.showinfo(f'{get_ip_address()}', 'Connection has been stopped.')
                print(f'{Fore.LIGHTWHITE_EX}Disconnected!')
                confirm_flag = True
                break

            if confirm_flag:
                messagebox.showinfo(f'{get_ip_address()}', 'Connection has been successfully established!')
                print(f'{Fore.LIGHTCYAN_EX}Connected to {get_ip_address()}!')
                confirm_flag = False

        except requests.exceptions.ConnectionError as err:
            confirm_flag = True
            messagebox.showerror('Connection Error', 'Cannot connect to the local server.')
            print(f'{Fore.LIGHTRED_EX}Fatal Error: Connection cannot be established to the local server!\nLog: {err}')
            break

        except cv2.error as msg:
            confirm_flag = True
            cv2.destroyAllWindows()
            messagebox.showerror('Connection Error', 'Lost the connection!')
            print(f'{Fore.LIGHTRED_EX}Fatal Error: connection lost!\nLog: {msg}')
            break


# GUI layers for component interactions and operations.
root = Tk()
root.title(AppInfo().APP_NAME)
os.system(AppInfo().CONSOLE_TITLE)
icon = PhotoImage(file=AppInfo().APP_ICON)
root.iconphoto(False, icon)
root.geometry(AppInfo().GEOMETRY)
root.configure(bg=AppInfo().BACK_THEME)

# background layout canvas
canvas = Canvas(
    root,
    bg=AppInfo().BACK_THEME,
    height=400,
    width=600,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)


# reads settings.ini file for dark and light mode themes
def read_theme_config():
    setting = ''
    # if file exists save option menu list data
    if os.path.isfile(AppInfo().SETTING_FILE):
        app_theme = open(AppInfo().SETTING_FILE, 'r')
        data = app_theme.read()
        setting = data
    else:
        set_theme = open(AppInfo().SETTING_FILE, 'w')
        set_theme.write('Light mode')
        set_theme.close()
    return setting

# writes OptionMenu selected value into settings.ini file 
def set_theme_config(options):
    setting = var.get()
    set_theme = open(AppInfo().SETTING_FILE, 'w')
    set_theme.write(setting)
    set_theme.close()
    root.destroy()
    os.startfile('main.py')
    return setting



# reads and returns the saved settings value to set
# assets path to switch app theme...
theme_path = read_theme_config().split()[0]
background_img = PhotoImage(file=f"assets//{theme_path}//background.png")
background = canvas.create_image(
    300.0, 200.0,
    image=background_img)



about_image = PhotoImage(file=f"assets//{theme_path}//about.png")
btn_about = Button(
    image=about_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: messagebox.showinfo('About', AppInfo().ABOUT),
    cursor="hand2",
    relief="flat")

btn_about.place(
    x=553, y=17,
    width=33,
    height=15)


help_img = PhotoImage(file=f"assets//{theme_path}//help.png")
btn_help = Button(
    image=help_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: messagebox.showinfo('Help', AppInfo().HELP),
    cursor="hand2",
    relief="flat")

btn_help.place(
    x=516, y=17,
    width=25,
    height=15)

capture_img = PhotoImage(file=f"assets//{theme_path}//capture.png")
capture_hover_img = PhotoImage(file=f"assets//{theme_path}//capture_hover.png")

btn_capture = Button(
    image=capture_img,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2",
    command=capture,
    relief="flat")
    
btn_capture.bind('<Enter>', lambda e: e.widget.config(image=capture_hover_img))
btn_capture.bind('<Leave>', lambda e: e.widget.config(image=capture_img))

btn_capture.place(
    x=220, y=263,
    width=160,
    height=46)

field_img = PhotoImage(file=f"assets//{theme_path}//field.png")

field = canvas.create_image(
    300.0, 226.0,
    image=field_img)

entry_ip = Entry(
    bd=0,
    bg="#e8e8e8",
    font=18,
    highlightthickness=0)


ToolTip(entry_ip, msg="Enter IP Address", delay=0.2)
entry_ip.place(
    x=156.0, y=206,
    width=288.0,
    height=38)

skyline_img = PhotoImage(file=f"assets//{theme_path}//skyline.png")
btn_skyline = Button(
    image=skyline_img,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2",
    command=lambda: webbrowser.open(AppInfo().SKYLINE_VR),
    relief="flat")

btn_skyline.place(
    x=522, y=369,
    width=24,
    height=22)

ToolTip(btn_skyline, msg="Github Skyline", delay=0.2)

git_img = PhotoImage(file=f"assets//{theme_path}//git.png")
btn_git = Button(
    image=git_img,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2",
    command=lambda: webbrowser.open(AppInfo().GITHUB),
    relief="flat")

btn_git.place(
    x=558, y=369,
    width=24,
    height=22)


ToolTip(btn_git, msg="Github", delay=0.2)
settings_img = PhotoImage(file=f"assets//{theme_path}//settings.png")
btn_settings = Button(
    image=settings_img,
    borderwidth=0,
    highlightthickness=0,
    relief="flat")

theme_list = ['Light mode', 'Dark mode']
var = StringVar()
dropdown = OptionMenu(
    root,
    var,
    *theme_list,
    command=set_theme_config
)


def show_drop_down(event):
    dropdown.place(x=19, y=372, width=13,height=13)


def hide_drop_down(event):
    dropdown.place_forget()


btn_settings.bind('<Enter>', show_drop_down)
canvas.bind('<Leave>', hide_drop_down)

btn_settings.place(
    x=15, y=369,
    width=20,
    height=21)
root.resizable(False, False)
root.mainloop()
