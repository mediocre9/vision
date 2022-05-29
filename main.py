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

confirmationFlag = True


# reads config.ini file and returns last auto saved IP address.
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
            for (x, y, w, h) in bodies:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
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
            messagebox.showerror('Connection Error', 'Cannot connect to the local IP address.')
            print(f'{Fore.LIGHTRED_EX}Fatal Error: Not connected to local server!')
            print(f'\nLog Exception: {str(err)}')
            break

        except cv2.error as msg:
            confirmationFlag = True
            cv2.destroyAllWindows()
            messagebox.showerror('Connection Error', f'Lost the connection!\n\nLog Exception: \n{msg}')
            print(f'{Fore.LIGHTRED_EX}Fatal Error: connection lost!')
            print(f'{Fore.LIGHTRED_EX}Log Exception: {str(msg)}')
            break


# GUI layer for other component operations.
root = Tk()
icon = PhotoImage(file=AppInfo().APP_ICON)
os.system(AppInfo().CONSOLE_TITLE)
root.title(AppInfo().APP_NAME)
root.iconphoto(False, icon)
root.geometry(AppInfo().WINDOW_DIMENSION)
root.resizable(False, False)
root.configure(bg=AppInfo().BACK_THEME)

menubar = Menu(root)
root.config(menu=menubar)
aboutMenu = Menu(menubar, tearoff=0)
aboutMenu.add_command(label='View Help', command=lambda: messagebox.showinfo('Help', AppInfo().HELP))
aboutMenu.add_separator()
aboutMenu.add_command(label='View About', command=lambda: messagebox.showinfo('About', AppInfo().ABOUT))
menubar.add_cascade(label='Help', menu=aboutMenu)

link = Label(root, text="Download Ip Webcam", font=('Helveticabold', 15, 'underline'), cursor="hand2",
             bg=AppInfo().BACK_THEME, fg='blue')
link.pack()
link.bind("<Button-1>", lambda e:
webbrowser.open(AppInfo().HYPERLINK))

link = Label(root, text="Github", font=('Helveticabold', 15, 'underline'), cursor="hand2", bg=AppInfo().BACK_THEME,
             fg='blue')
link.pack()
link.bind("<Button-1>", lambda e:
webbrowser.open(AppInfo().GITHUB))

link = Label(root, text="VR Author Github", font=('Helveticabold', 15, 'underline'), cursor="hand2",
             bg=AppInfo().BACK_THEME, fg='blue')
link.pack()
link.bind("<Button-1>", lambda e:
webbrowser.open(AppInfo().SKYLINE_VR))

ipAddressLabel = Label(root, text='IP:', font=('Consolas', 24), bg=AppInfo().BACK_THEME, fg=AppInfo().FORE_THEME)
ipAddressField = Entry(root, width=20, font=('Consolas', 17))
ipAddressField.insert(0, getIpAddress()[0:0])
btnCapture = Button(text='CAPTURE', font=('Consolas', 14), height=2, width=35, command=capture)
ipAddressLabel.place(x=25, y=125)
ipAddressField.place(x=90, y=130)
btnCapture.place(x=20, y=200)
root.mainloop()
