import webbrowser as web
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
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


root = Tk()
icon = PhotoImage(file=AppInfo().APP_ICON)
os.system(AppInfo().CONSOLE_TITLE)
root.title(AppInfo().APP_NAME)
root.iconphoto(False, icon)
root.geometry(AppInfo().GEOMETRY)
root.resizable(False, False)
root.configure(bg=_from_rgb(AppInfo().BACK_THEME))

menubar = Menu(root)
root.config(menu=menubar)
aboutMenu = Menu(menubar, tearoff=0)
aboutMenu.add_command(label='View Help', command=lambda: messagebox.showinfo('Help', AppInfo().HELP))
aboutMenu.add_separator()
aboutMenu.add_command(label='View About', command=lambda: messagebox.showinfo('About', AppInfo().ABOUT))
menubar.add_cascade(label='Help', menu=aboutMenu)

link = Label(root, text="Download Ip Webcam", font=('Helvetica bold', 15, 'underline'), cursor="hand2",
             bg=_from_rgb(AppInfo().BACK_THEME), fg='blue')
link.pack()
link.bind("<Button-1>", lambda e:
web.open(AppInfo().IP_WEBCAM))

link = Label(root, text="Github", font=('Helvetica bold', 15, 'underline'), cursor="hand2",
             bg=_from_rgb(AppInfo().BACK_THEME),
             fg='blue')
link.pack()
link.bind("<Button-1>", lambda e:
web.open(AppInfo().GITHUB))

link = Label(root, text="VR Author Github", font=('Helvetica bold', 15, 'underline'), cursor="hand2",
             bg=_from_rgb(AppInfo().BACK_THEME), fg='blue')
link.pack()
link.bind("<Button-1>", lambda e:
web.open(AppInfo().SKYLINE_VR))

ipAddressLabel = Label(root, text='IP Address:', font=('Helvetica bold', 14), bg=_from_rgb(AppInfo().BACK_THEME),
                       fg=AppInfo().FORE_THEME)
ipAddressField = Entry(root, width=20, font=('Helvetica bold', 17), relief='flat')
ipAddressField.insert(0, getIpAddress()[0:0])
btnCapture = Button(text='CAPTURE', font=('Helvetica bold', 14), height=1, width=32, command=capture,
                    bg=_from_rgb((45, 45, 46)), relief='groove', fg=AppInfo().FORE_THEME)
ipAddressLabel.place(x=75, y=115)
ipAddressField.place(x=80, y=150)
btnCapture.place(x=20, y=200)
root.mainloop()
