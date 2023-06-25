import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import ftplib
import os
import ntpath #This is used to extract filename from path

from tkinter import filedialog
from pathlib import Path


from playsound import playsound
import pygame
from pygame import mixer

PORT  = 8050
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096

name = None
listbox =  None
filePathLabel = None

global song_counter
song_counter = 0

import ftplib
import os
import time
from tkinter import filedialog
from pathlib import Path

def browseFiles():
    global textarea, filepathLabel
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File")
    filepathLabel.configure(text=filename)
    
    HOSTNAME = "127.0.0.1"
    USERNAME = "username"
    PASSWORD = "password"

    with ftplib.FTP(HOSTNAME) as ftp:
        ftp.login(USERNAME, PASSWORD)
        ftp.mkd("sharing_files")
        ftp.cwd("sharing_files")
        
        fname = Path(filename).name
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {fname}", file)
        
        ftp.dir()
        ftp.quit()
        listbox.insert(song_counter,fname)
        song_counter = song_counter + 1
        
        

def download():
    # Get the selected song from the listbox
    selected_song = listbox.get(ANCHOR)

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOSTNAME, PORT))

    # Send authentication details
    client_socket.sendall(f"{USERNAME}:{PASSWORD}".encode())

    # Receive authentication response
    auth_response = client_socket.recv(1024).decode()
    if auth_response != "OK":
        messagebox.showerror("Authentication Error", "Invalid credentials. Please try again.")
        return

    # Send the "download" command with the selected song
    client_socket.sendall(f"download:{selected_song}".encode())

    # Get the path of the file in the Downloads folder
    downloads_folder = os.path.expanduser("~/Downloads")
    file_path = os.path.join(downloads_folder, selected_song)

    # Receive and save the file
    with open(file_path, "wb") as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)

    messagebox.showinfo("Download Complete", f"The file '{selected_song}' has been downloaded to the Downloads folder.")

    # Close the connection
    client_socket.sendall("quit".encode())
    client_socket.close()



def play():
    global song_selected
    song_selected=listbox.get(ANCHOR)
    
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()
    if(song_selected != ""):
        infoLabel.configure(text="Now Playing: " +song_selected)
    else:
       infoLabel.configure(text="")

def stop():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()
    infoLabel.configure(text="")
def resume():
    global song_selected
    mixer.init()
    mixer.music.load("shared_files/" + song_selected)
    mixer.music.play()

   
def musicWindow(): 
    global song_counter
    global filePathLabel
    global listbox
    global infoLabel
    
    window=Tk()
    window.title('Music Window')
    window.geometry("300x300")
    window.configure(bg='LightSkyBlue')
    
    selectlabel = Label(window, text= "Select Song",bg='LightSkyBlue', font = ("Calibri",8))
    selectlabel.place(x=2, y=1)

    resumeButton = Button(window,text = "Resume", command = resume)
    resumeButton.place(x = 30, y= 250)
    
    pauseButton = Button(window,text = "Pause", command = pause)
    pauseButton.place(x = 200, y = 250)
    listbox = Listbox(window,height = 10,width = 39,activestyle = 'dotbox',bg='LightSkyBlue',borderwidth=2, font = ("Calibri",10))
    listbox.place(x=10,y=18)
    for file in os.listdir('shared_files'):
        filename = os.fsdecode(file)
        listbox.insert(song_counter, filename)
        song_counter = song_counter + 1
        
    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)
    
    PlayButton=Button(window,text="Play", width=10,bd=1,bg='SkyBlue',font = ("Calibri",10), command = play)
    PlayButton.place(x=30,y=200)
    
    Stop=Button(window,text="Stop",bd=1,width=10,bg='SkyBlue', font = ("Calibri",10), command = stop)
    Stop.place(x=200,y=200)
    
    Upload=Button(window,text="Upload",width=10,bd=1,bg='SkyBlue', font = ("Calibri",10))
    Upload.place(x=30,y=250)
    
    Download =Button(window,text="Download",width=10,bd=1,bg='SkyBlue', font = ("Calibri",10))
    Download.place(x=200,y=250)
    
    infoLabel = Label(window, text= "",fg= "blue",bg='SkyBlue', font = ("Calibri",8))
    infoLabel.place(x=4, y=280)
    
    window.mainloop()
    
def setup():
    global SERVER
    global PORT
    global IP_ADDRESS
    global song_counter

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    musicWindow()

   
setup()


if __name__ == "__main__":
    browseFiles()

   



