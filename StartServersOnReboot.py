from os.path import expanduser
import datetime

import os

# import pyautogui, time

try:
    # os.chdir("/home/jetson-tx2-nx/Desktop/JetsonServer:7038")

    # command="python3 manage.py runserver 0.0.0.0:7038"
    # os.system("dbus-launch gnome-terminal -e 'bash -c \""+command+";bash\"'")
    os.chdir(expanduser("~") + '/Desktop')
    # print(os.walk(os.getcwd()))
    # print([x[0] for x in os.walk(os.getcwd())])
    # for item in os.listdir():
    #     print(os.path.splitext(item))
    outputList = []
    for root, dirs, files in os.walk(os.getcwd()):
        # print(root)
        # print(dirs)
        # print(files)
        for item in dirs:
            # print(item)
            os.chdir(f"/home/jetson-tx2-nx/Desktop/{item}")
            port = item.split(":")[1]
            command=f"python3 manage.py runserver 0.0.0.0:{port}"
            os.system("dbus-launch gnome-terminal -e 'bash -c \""+command+";bash\"'")
        break
except Exception as e:
    file = open(expanduser("~") + '/Desktop/terminal-hata.txt', 'w')
    file.write(str(e) + " \n" + str(datetime.datetime.now()))
    file.close()

