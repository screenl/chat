#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

'''
12.7 changelog:
+ GUI.parseOutput() - markdown notation of bold and italic / time notations
+ help - explains
'''
helpTextString = r'''
\t for time (e.g. 13:36:58)
\d for date (e.g. Apr 30 2021)
\* for the character *
**text** for bold
*text* for italic
'''
# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from chat_utils import *
import json
import re
import time
import os
from tkinter import messagebox

# GUI class for the chat


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        self.player = 0



    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Gobang game")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=500,
                             height=400)
        # create a Label
        self.pls = Label(self.login,
                         text="Gobang game",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.4,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Username: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)
        self.labelName02 = Label(self.login,
                               text="Password: ",
                               font="Helvetica 12")

        self.labelName02.place(relheight=0.2,
                             relx=0.1,
                             rely=0.4)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)
        self.entryName02 = Entry(self.login,
                               font="Helvetica 14")
        self.entryName02.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.4)

        self.labelPasswd = Label(self.login,
                               text="Password: ",
                               font="Helvetica 12")

        self.labelPasswd.place(relheight=0.2,
                             relx=0.1,
                             rely=0.4)

        # create a entry box for
        # tyoing the message
        self.entryPasswd = Entry(self.login,
                               font="Helvetica 14")

        self.entryPasswd.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.4)
        # set the focus of the curser
        self.entryName.focus()
        
        # create a Continue Button
        # along with action
        self.log = Button(self.login,
                         text="Login",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get(),self.entryPasswd.get()))

        self.log.place(relx=0.4,
                      rely=0.75)
        self.Window.mainloop()

    def goAhead(self, name,passwd):
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name, "passwd": passwd})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state=NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")
                self.textCons.insert(END, menu + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
                process = threading.Thread(target=self.proc)
                process.daemon = True
                process.start()
            else:
                messagebox.showerror('Error', response["message"])
        # the thread to receive messages

    # The main layout of the chat
    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=600,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.textCons.tag_config('b',font='Helvetica 14 bold')
        self.textCons.tag_config('i',font='Helvetica 14 italic')

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.5,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        def plus():
            self.entryMsg.insert(END, "+")

        self.buttonPlus = Button(self.labelBottom,
                                text="+",
                                font="Helvetica 20 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: plus())
        self.buttonPlus.place(relx=0.52,rely=0.008,relheight=0.029,relwidth=0.22)


        def help():
            helpWindow = Toplevel(self.Window)
            helpWindow.title("Help")
            helpText = Text(helpWindow, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
            helpText.place(relheight=1,relwidth=1)
            helpText.insert(END, helpTextString)
            helpText.config(state=DISABLED)

        self.buttonHelp = Button(self.labelBottom,
                                text="?",
                                font="Helvetica 20 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: help())

        self.buttonHelp.place(relx=0.52,rely = 0.039,relheight=0.029,relwidth=0.22)
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.75,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.24)


        self.textCons.config(cursor="arrow")
        

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def parseOutput(self, msg):
        msg = re.sub(r'\\t',time.strftime("%H:%M:%S", time.localtime()), msg)
        msg = re.sub(r'\\d',time.strftime("%b %d %Y", time.localtime()), msg)
        #mark time and date

        msg = re.sub(r'\\\*',chr(27), msg)
        def reduce(a):
            return re.sub(chr(27), '*', a)
        #'\*' -> '*'

        f = 0
        for i in re.split(r'\*\*',msg):
            if f == 0:
                g = 0
                for j in re.split(r'\*',i):
                    if g == 0:
                        self.textCons.insert(END, reduce(j))
                        g = 1
                    elif g == 1:
                        self.textCons.insert(END, reduce(j), 'i')
                        g = 0
                f = 1
            elif f == 1:
                self.textCons.insert(END, reduce(i), 'b')
                f = 0
        #mark bold and italic

        self.textCons.insert(END, '\n')
        return msg

    def sendButton(self, msg):
        # self.textCons.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        #self.textCons.insert(END, msg + "\n")
        self.parseOutput(msg)
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state=NORMAL)
                #self.textCons.insert(END, self.system_msg + "\n\n")
                self.parseOutput(self.system_msg+'\n')
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
    
    def opengame(self):
        if self.player == 0:
            self.player += 1
            os.system('python chess_server.py')
        elif self.player == 1:
            self.player += 1
            os.system('python chess_client.py')
        elif self.player >= 2:
            self.messagebox.showinfo(title= 'report',info = 'players are enough')
            
            

    def run(self):
        self.login()


# create a GUI class object
if __name__ == "__main__":
    # g = GUI()
    pass
