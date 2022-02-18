#importing tkinter module
from tkinter import *
import tkinter.messagebox
import time
import os
import threading
from PIL import Image,ImageTk,ImageSequence

 
#importing pygame library for sound
from pygame import mixer

#importing dialog file
from tkinter import filedialog

#importing mutagen to store data of mp3 file
from mutagen.mp3 import MP3

#initializing mixer object
#mixer.init(45000, -16, 2, 400)
mixer.pre_init(44200,-16,2,1024)
mixer.init()

#creating an object
root = Tk()


#giving dimension to the window
root.geometry('500x600')

#title to the opening window
root.title("KG player")



#functions having different functionality

def browse_file():
    global filename
    filename = filedialog.askopenfilename()
    add_to_list(filename)

playlist = []

# playlist - contains the full path + filename
# listbox - contains just the filename
# Fullpath + filename is required to play the music inside play  load function

def add_to_list(f):
    f = os.path.basename(f)
    index = 0
    list_box.insert(index,f)
    playlist.insert(index,filename)
    index += 1



def show_all(play_song):
    file_data = os.path.splitext(play_song)      #this divides the path into two parts (name,extension)
    if file_data[1] == '.mp3' :
        audio = MP3(play_song)
        total_length = audio.info.length    #this will get length of sound track
        print(total_length)
    else :
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins,secs = divmod(total_length,60)
    mins = round(mins)
    secs = round(secs)
    time_format = "{:02d}:{:02d}".format(mins,secs)    
    lengthlabel['text'] = 'Total length' + ' - ' + time_format

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            l2['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play() :
    global paused
    if paused :
        mixer.music.unpause()
        status_bar['text'] = "Music resumed"   
        paused = FALSE
    
    # if initialized it will resume the music      
    else : 
        try :
            #stop.music()
            #time.sleep(1)
            selected_song = list_box.curselection()     #this returns value in 0,1 in form of tuple
            selected_song = int(selected_song[0])       #taking the first indiex of tuple and converting into integer
            play_this = playlist[selected_song]         #passing this integer in list, now this list contains full file path
            mixer.music.load(play_this)
            mixer.music.play()
            status_bar['text']= "Playing" + ' - ' + os.path.basename(play_this)
            show_all(play_this)
        except : 
            messagebox.showerror("Unknown Error","Couldn't open the file, Please try again")
    
        
def stop() :
    mixer.music.stop()
    status_bar['text']= "Music Stopped"

paused = FALSE

def pause():
    global paused
    paused = True
    mixer.music.pause()
    status_bar['text'] = "Music paused"

def rewind():
    play()
    status_bar['text'] = "Music rewinded"

def set_vol(val):
    volume = int(val)/100   # set_volume of mixer takes value only from 0 to 1.
    if volume == 1 :
        messagebox.showwarning("Warning","Max Volume reached\nPlease lower it down")
    else :        
        mixer.music.set_volume(volume)    


muted = FALSE

def mute():
    global muted
    
    if muted :      #unmuted
        mixer.music.set_volume(0.50)
        vol_slider.set(50)
        mute_button.configure(image = img6)
        muted = FALSE

    else :          #loop to mute
        mixer.music.set_volume(0)
        vol_slider.set(0)
        mute_button.configure(image = img7)
        muted = TRUE

def delete():
    selected_song = list_box.curselection()     #this returns value in 0,1 in form of tuple
    selected_song = int(selected_song[0])
    list_box.delete(selected_song)
    playlist.pop(selected_song)


#creating status bar
status_bar = Label(root, text = 'Created by Kisalay Ghosh', font= ('Times 13 italic'),relief=FLAT,anchor=W)
status_bar.pack(fill=X)


lower_frame =  Frame(root, width = 500, height = 200)
lower_frame.pack(side=BOTTOM)

#dividing the frame into two halves
upper_frame = Frame(root, width = 500, height = 400)
upper_frame.pack(side=TOP)

#inserting image into background
img_ = PhotoImage(file="pic01.png")
label_image_ = Label(upper_frame, image=img_)
label_image_.pack()

#inserting image into background
img = PhotoImage(file="pic02.png")
label_image = Label(lower_frame, image=img)
label_image.pack()


#creating label for viewing length of the soundtrack
lengthlabel = Label(lower_frame ,text = "Total length --:--")
#lengthlabel.configure(relief=FLAT)
lengthlabel.place(x=5,y=20)

#current time label
l2 = Label(lower_frame, text="Current length --:--")
#l2.configure(relief=FLAT)
l2.place(x=350,y=20)


#creating image button to play the song
img1 = PhotoImage(file="pic03.png")
play_button = Button(lower_frame ,image=img1,command=play)
#play_button.configure(relief=FLAT)
play_button.place(x=120,y=100)


#creating image button to stop the song
img2 = PhotoImage(file="pic04.png")
stop_button = Button(lower_frame, image=img2,command=stop)
#stop_button.configure(relief=FLAT)
stop_button.place(x=200,y=100)  


#creating volume slider to change intensity
vol_slider = Scale(lower_frame, from_=100, to=0,command=set_vol)
vol_slider.configure(width=30,length=100,sliderrelief=SUNKEN,fg="black")
vol_slider.set(50)
mixer.music.set_volume(0.5)
vol_slider.place(x=420,y=70)

#creating pause button
img4 = PhotoImage(file='pic05.png')
pause_button = Button(lower_frame, image=img4,command=pause)
#pause_button.configure(relief=FLAT)
pause_button.place(x=280,y=100)

#creating rewind button
img5 = PhotoImage(file="pic06.png")
rewind_button = Button(lower_frame, image = img5,command=rewind)
#rewind_button.configure(relief=FLAT)
rewind_button.place(x=70,y=120)

#creating forwardbutton
img9 = PhotoImage(file="pic07.png")
forward_button = Button(lower_frame, image = img9)
#forward_button.configure(relief=FLAT)
forward_button.place(x=360,y=120)

#creating mute button
img6 = PhotoImage(file="volume up.png")
img7 = PhotoImage(file="volume down.png")
mute_button = Button(lower_frame,image=img6,command=mute)
#mute_button.configure(relief=FLAT)
mute_button.place(x=20,y=120)


list_box = Listbox(upper_frame)
list_box.configure(width=40,height=3,bg='lightgrey')
list_box.place(x=10,y=10)


#creating delete button
img8 = PhotoImage(file="delete.png")
del_button = Button(upper_frame, image=img8,cursor="hand",command=delete)
#del_button.configure(relief=FLAT)
del_button.place(x=390,y=40)

label_img8 = Label(upper_frame,text="Add",font= ('Times 15 bold'),relief=FLAT)
label_img8.place(x=420,y=10)

label_img3 = Label(upper_frame,text="Delete",font= ('Times 15 bold'),relief=FLAT)
label_img3.place(x=420,y=40)

#creating button to add music
img3 = PhotoImage(file="addmusic.png")
add_button = Button(upper_frame, image=img3,command=browse_file, cursor="hand")
#add_button.configure(relief=FLAT)
add_button.place(x=390,y=10)


def on_closing():
    mixer.music.stop()
    messagebox.showinfo("Enjoy","Thanks for choosing Kisalay's music player \nSee you soon!!")
    root.destroy()
    
root.resizable(False, False) # not resizable in both directions  
root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()