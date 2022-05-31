# import webbrowser as web
import requests
import cv2
import numpy as np
import imutils
from tkinter import *
from tkinter import messagebox
import os
from colorama import Fore
from app_info import *

confirmationFlag = True


# reads config.ini file and returns the last saved IP address.
def getIpAddress():
    ip = ipAddressField.get()

    if os.path.isfile(AppInfo().CONFIG_FILE) and not ip:
        config = open(AppInfo().CONFIG_FILE, 'r')
        data = config.read()
        ip = data
    else:
        saveIpAddress = open(AppInfo().CONFIG_FILE, 'w')
        saveIpAddress.write(ip)
        saveIpAddress.close()

    ipAddressField.delete(0, END)
    ipAddressField.insert(0, ip)
    return ip


# main process that connects to the local web server for image projection
def capture():
    address = getIpAddress()
    url = f"http://{address}:8080/shot.jpg"
    cascade = cv2.CascadeClassifier(AppInfo().CASCADE)
    print(f"{Fore.LIGHTGREEN_EX}Establishing connection to local server IP: {getIpAddress()} . . .")

    while True:
        global confirmationFlag
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
            cv2.namedWindow('RT Video Camera Streaming . . .', cv2.WINDOW_NORMAL)

            bodies = cascade.detectMultiScale(gray, 1.1, 3)
            for (offsetX, offsetY, width, height) in bodies:
                cv2.rectangle(img, (offsetX, offsetY), (offsetX + width, offsetY + height), (0, 255, 0), 2)
            cv2.imshow("RT Video Camera Streaming . . .", img)

            # Press Esc key to exit
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                messagebox.showinfo(f'{getIpAddress()}', 'Connection has been stopped.')
                print(f'{Fore.LIGHTWHITE_EX}Disconnected!')
                confirmationFlag = True
                break

            if confirmationFlag:
                messagebox.showinfo(f'{getIpAddress()}', 'Connection has been successfully established!')
                print(f'{Fore.LIGHTCYAN_EX}Connected to {getIpAddress()}!')
                confirmationFlag = False

        except requests.exceptions.ConnectionError as err:
            confirmationFlag = True
            messagebox.showerror('Connection Error', f'Cannot connect to the local server. \n\nLog Exception : \n{err}')
            print(f'{Fore.LIGHTRED_EX}Fatal Error: Connection cannot be established to the local server!')
            print(f'\nLog Exception: {str(err)}')
            break

        except cv2.error as msg:
            confirmationFlag = True
            cv2.destroyAllWindows()
            messagebox.showerror('Connection Error', f'Lost the connection!\n\nLog Exception: \n{msg}')
            print(f'{Fore.LIGHTRED_EX}Fatal Error: connection lost!')
            print(f'{Fore.LIGHTRED_EX}Log Exception: {str(msg)}')
            break


# GUI layers for component interactions and operations.
root = Tk()
root.title(AppInfo().APP_NAME)
os.system(AppInfo().CONSOLE_TITLE)
root.geometry(AppInfo().GEOMETRY)
icon = PhotoImage(file=AppInfo().APP_ICON)
root.iconphoto(False, icon)
root.configure(bg=AppInfo().BACK_THEME)
canvas = Canvas(
    root,
    bg=AppInfo().BACK_THEME,
    height=400,
    width=570,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

backgroundImg = PhotoImage(file=f"assets//app//background.png")
background = canvas.create_image(
    285.0, 200.0,
    image=backgroundImg)

aboutImg = PhotoImage(file=f"assets//app//about.png")
btnAbout = Button(
    image=aboutImg,
    borderwidth=0,
    highlightthickness=0,
    cursor='hand2',
    command=lambda: messagebox.showinfo('About', AppInfo().ABOUT),
    relief="flat")

btnAbout.place(
    x=520, y=372,
    width=33,
    height=15)

helpImg = PhotoImage(file=f"assets//app//help.png")
btnHelp = Button(
    image=helpImg,
    borderwidth=0,
    highlightthickness=0,
    cursor='hand2',
    command=lambda: messagebox.showinfo('Help', AppInfo().HELP),
    relief="flat")

btnHelp.place(
    x=480, y=372,
    width=28,
    height=15)

captureImg = PhotoImage(file=f"assets//app//capture.png")
btnCapture = Button(
    image=captureImg,
    borderwidth=0,
    highlightthickness=0,
    command=capture,
    cursor='hand2',
    relief="flat")

btnCapture.place(
    x=299, y=258,
    width=145,
    height=33)

ipFieldImg = PhotoImage(file=f"assets//app//field.png")
ipAddressFieldLayout = canvas.create_image(
    368.0, 219.5,
    image=ipFieldImg)

ipAddressField = Entry(
    bd=0,
    bg="#e8e8e8",
    highlightthickness=0)
ipAddressField.insert(0, getIpAddress()[0:0])
ipAddressField.place(
    x=256.0, y=200,
    width=224.0,
    height=37)

root.resizable(False, False)
root.mainloop()
