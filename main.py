# import webbrowser as web
import webbrowser

import requests
import cv2
import numpy as np
import imutils
from tkinter import *
from tkinter import messagebox
import os
from colorama import Fore
from app_info import *

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
    url = f"http://{address}:8080/shot.jpg"
    cascade = cv2.CascadeClassifier(AppInfo().CASCADE)
    print(f"{Fore.LIGHTGREEN_EX}Establishing connection to local server IP: {address} . . .")

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
            for (offsetX, offsetY, width, height) in bodies:
                cv2.rectangle(img, (offsetX, offsetY), (offsetX + width, offsetY + height), (0, 255, 0), 2)
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
            print(f'{Fore.LIGHTRED_EX}Fatal Error: Connection cannot be established to the local server!')
            break

        except cv2.error as msg:
            confirm_flag = True
            cv2.destroyAllWindows()
            messagebox.showerror('Connection Error', 'Lost the connection!')
            print(f'{Fore.LIGHTRED_EX}Fatal Error: connection lost!')
            break


# GUI layers for component interactions and operations.

root = Tk()
root.title(AppInfo().APP_NAME)
os.system(AppInfo().CONSOLE_TITLE)
icon = PhotoImage(file=AppInfo().APP_ICON)
root.iconphoto(False, icon)
root.geometry(AppInfo().GEOMETRY)
root.configure(bg=AppInfo().BACK_THEME)
canvas = Canvas(
    root,
    bg=AppInfo().BACK_THEME,
    height=400,
    width=600,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file=f"assets//app//background.png")
background = canvas.create_image(
    300.0, 200.0,
    image=background_img)

about_image = PhotoImage(file=f"assets//app//about.png")
btn_about = Button(
    image=about_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: messagebox.showinfo('About',AppInfo().ABOUT),
    cursor="hand2",
    relief="sunken")

btn_about.place(
    x=553, y=17,
    width=33,
    height=15)

help_img = PhotoImage(file=f"assets//app//help.png")
btn_help = Button(
    image=help_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: messagebox.showinfo('Help',AppInfo().HELP),
    cursor="hand2",
    relief="sunken")

btn_help.place(
    x=516, y=17,
    width=25,
    height=15)

capture_img = PhotoImage(file=f"assets//app//capture.png")
capture_hover_img = PhotoImage(file=f"assets//app//capture_hover.png")
btn_capture = Button(
    image=capture_img,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2",
    command=capture,
    relief="sunken")

btn_capture.bind('<Enter>', lambda e: e.widget.config(image=capture_hover_img))
btn_capture.bind('<Leave>', lambda e: e.widget.config(image=capture_img))

btn_capture.place(
    x=220, y=263,
    width=160,
    height=46)

field_img = PhotoImage(file=f"assets//app//field.png")
field = canvas.create_image(
    300.0, 226.0,
    image=field_img)

entry_ip = Entry(
    bd=0,
    bg="#e8e8e8",
    font=18,
    highlightthickness=0)

entry_ip.place(
    x=156.0, y=206,
    width=288.0,
    height=38)

skyline_img = PhotoImage(file=f"assets//app//skyline.png")
btn_skyline = Button(
    image=skyline_img,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2",
    command=lambda: webbrowser.open(AppInfo().SKYLINE_VR),
    relief="sunken")

btn_skyline.place(
    x=522, y=369,
    width=24,
    height=22)

git_img = PhotoImage(file=f"assets//app//git.png")
btn_git = Button(
    image=git_img,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2",
    command=lambda: webbrowser.open(AppInfo().GITHUB),
    relief="sunken")

btn_git.place(
    x=558, y=369,
    width=24,
    height=22)

root.resizable(False, False)
root.mainloop()
