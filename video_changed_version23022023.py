
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 23:01:03 2023

@author: DELL
"""

import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from tkinter import *
import time
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
import pandas as pd
import os
import re
import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import warnings
import customtkinter as ctk
from moviepy.video.io.VideoFileClip import VideoFileClip
import subprocess
import io

warnings.filterwarnings("ignore")

from day_Sri import *
from date_Sri import *
from hms_Sri import *

#default
name_list = []
time_list = []
intime_list = []
outtime_list = []
matched_name = []
date_list = []
company_list = []
person_data_list = []
option_list=[]
time_to_sec = []
buttons = []
# Initialize an empty list to hold the thumbnail images
thumbnail_images = []
df1 = pd.DataFrame()
# =============================================================================
# #------------------------------------------------------------
# date = datetime.now()
# days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# current_date = time.strftime("%m-%d-%Y ")
# current_year = time.strftime("%Y")
# current_time = time.strftime(" %H:%M:%S")
# #print('today is: ',current_day)
# current_day= days[date.weekday()]
# print('today is: ',current_date + current_day + current_time )
# #-------------------------------------------------------------
# =============================================================================

# initialize the reader

reader = easyocr.Reader(['en'])

# open the video capture
x=6
y=30
w=600
h=60

def popup_showinfo():
    showinfo("Window", "Video Uploaded Successfully")

def popup_showinfo2():
    showinfo("Time Status", "Time Updated Successfully")
def name_search():
    showinfo("Name Search", "Name found in database")
def noname():
    showinfo("Name Search", "No Name found in database. Check your input data")
def name_search1():
    showinfo("Company Search", "Company Name found in database")
def noname1():
    showinfo("Input Data", "No Data Found. Check your input and try again")
def no_video():
    
    showinfo("Video Data", "No Video uploaded. Kindly upload a video for recognition")
def no_excel():
    showinfo("Excel Data", "No Excel uploaded. Kindly upload a excel for fetching data")

def load_video():
    global file_path
    """ loads the video """
    file_path = filedialog.askopenfilename(filetypes=[("Video files", ".mp4 .avi")])
    
    if file_path:
        vid_player.load(file_path)

        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)
        popup_showinfo()
        play_pause_btn.config(state='normal')
        progress_slider.config(state='normal')
        skip_plus_5sec1.configure(state='normal')
        skip_plus_5sec.configure(state='normal')
        ocr()
    else:
        print("no video uploaded")
        no_video()
    
    return file_path


def test1():
    global final_date
    global final_hms
    final_date = "02-01-2023"
    final_time = "08:52:42"
    time_enter()
    return final_date, final_hms
    
def ocr():
    global final_date
    global final_hms
    print("OCR work here")
    cap = cv2.VideoCapture(file_path)
    success, frame = cap.read()

    # Check if the frame was read successfully
    if success:
        # Save the frame as an image
        cv2.imwrite("frame.jpg",frame)
        image = "frame.jpg"
        # Define the command to run the sub script with the image path as an argument
        command = ['python', 'detect13.py','--source',image ]
        
        # Run the command using the subprocess module
        result = subprocess.run(command, capture_output=True)
        f = result.stdout
        # Convert the string to a numpy array
        normal_string = f.decode('utf-8')
        
        print(normal_string) # Output: 'hello'
        # load the image
        frame = cv2.imread(normal_string.strip())
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        inverted_gray = cv2.bitwise_not(gray_image)
        result = reader.readtext(frame)
        #result = reader.readtext(frame[y:y+h, x:x+w])
        #print(result)
        print('=='*8)
        res = []
        for i in range(len(result)):
            res.append(result[i][1])
        print('raw result: ',res)
        if len(res) != 0:
            for i in range(len(res)):
                res[i] = res[i].replace(" ", "")
            print(res)
            res[0] = res[0].replace('z', '2')
            final_day = get_day(res[0])
            final_date = get_date(res[0])
            final_hms = get_hms(res)
        if final_date is None:
            # Separate string into two elements
            # Remove first character in year component
            my_string = res[0]
            my_string = my_string[:0] + my_string[1:]
            # Remove all characters after '11'
            my_string = my_string[:10]
            print(my_string)
            # Convert string to datetime object
            datetime_obj = datetime.datetime.strptime(my_string, "%Y-%m-%d")
                
                # Extract date component and format it as "dd-mm-yy"
            date_str = datetime_obj.date().strftime("%d-%m-%Y")
            final_date = date_str

        print('final day is:: ', final_day)
        print('final date is::  ',final_date)
        print('final time is:: ',final_hms)
        
        try:
            if len(final_hms)>0 and len(final_day)>0 and len(final_date)>0:
                print('Final result: ',final_date+' '+final_day+' '+final_hms)
                print('**'*20)
            else:
                print('oops!  can not display result because format is not valid.')
        except:
            pass
    print("value returned")
    time_enter()
    return final_date, final_hms


def time_enter():
    #enter time
    global time_value
    global time_list
    global my_date
    
    time_value = str(final_hms)
    date_value = str(final_date)
    
    time_list = time_value.split(":")
    date_list = date_value.split("-")
    #YYYY-MM-DD HH:MM:SS.ssssss
    my_date = datetime.datetime(int(date_list[2]),int(date_list[1]),int(date_list[0]),int(time_list[0]),int(time_list[1]),int(time_list[2])) 
    start_timee= str(my_date.time())
    start_time = tk.Label(master=control_frame, text=start_timee, font=('calibre',15, 'bold'))

    start_time.place(relx=0, rely=0.0)
    popup_showinfo2()

    return my_date,time_value
#skip time
def skip_time():
    
    skip_time = jumptime_var.get()
    
    ftr = [3600,60,1]

    x = sum([a*b for a,b in zip(ftr, map(int,skip_time.split(':')))])
    y = sum([a*b for a,b in zip(ftr, map(int,time_value.split(':')))])
    z=x-y
    
    u = progress_slider.get()
    skip(z)
    jumptime_var.set("")
      
def update_duration(event):
    
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    
    my_date_seconds = my_date + datetime.timedelta(seconds = duration)
    
    end_time["text"] = str(my_date_seconds.time().replace(microsecond=0))
    progress_slider["to"] = duration
    
    jumptime_label = ctk.CTkLabel(side_frame, text = 'Enter the Jump time', font=('calibre',10, 'bold'))
    jumptime_label.place(relx=0.12, rely=0.65)
      
    jumptime_entry = tk.Entry(side_frame,textvariable = jumptime_var, font=('calibre',10,'normal'))
    jumptime_entry.place(relx=0.12, rely=0.70)
    jumptime_btn = ctk.CTkButton(side_frame, text="Jump to Time", command=skip_time)
    jumptime_btn.place(relx=0.12, rely=0.75)
    
    
def update_scale(event):
    """ updates the scale value """
    progress_value.set(vid_player.current_duration())


    
def seek(value):
    """ used to seek a specific timeframe """
    vid_player.seek(int(value))


def skip(value: int):
    """ skip seconds """
    if value <6:
        vid_player.seek(int(progress_slider.get())+value)
        progress_value.set(progress_slider.get() + value)
    else:
        vid_player.seek(int(value))
        progress_value.set(value)
def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"
    
    e_btn.configure(state="normal")
def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)

def save_file():
    global filepath
    
    f = asksaveasfile(initialfile = 'trim_output.mp4',
                defaultextension=".mp4",filetypes=[("All Files","*.*"),("Video Files","*.mp4 *.avi")])
    filepath = os.path.abspath(f.name) 
    return filepath
def popup_showinfo1():
    filepathn = filepath.replace('trim_output.mp4','')
    text = "Video Trimmed Successfully and saved to "+ filepathn
    showinfo("Trim Status",text )
    exit1()
def trimv():
    print("Trim_Started")
    
    ftr = [3600,60,1]
    starttime = starttime_var.get()
    endtime = endtime_var.get()
    x = sum([a*b for a,b in zip(ftr, map(int,starttime.split(':')))])
    y = sum([a*b for a,b in zip(ftr, map(int,endtime.split(':')))])
    acttime = sum([a*b for a,b in zip(ftr, map(int,time_value.split(':')))])
    starttime_calculation = x - acttime
    endtime_calculation = y - acttime
    
    
    ffmpeg_extract_subclip(file_path, starttime_calculation, endtime_calculation, targetname=filepath)
    popup_showinfo1()

def trimv1():
    print("Trim_Started")
    ftr = [3600,60,1]
    
    for x in range(len(matched_name)):
        nametext = matched_name[x].replace(" ", "")+".mp4"
        filepathn = filepath.replace('.mp4', nametext)
        starttime = str(intime_list[x])
        endtime = str(outtime_list[x])
        x = sum([a*b for a,b in zip(ftr, map(int,starttime.split(':')))])
        y = sum([a*b for a,b in zip(ftr, map(int,endtime.split(':')))])
        acttime = sum([a*b for a,b in zip(ftr, map(int,time_value.split(':')))])
        starttime_calculation = x - acttime
        endtime_calculation = y - acttime
        
        
        ffmpeg_extract_subclip(file_path, starttime_calculation, endtime_calculation, targetname=filepathn)
    popup_showinfo1()
def excel_uplaod():
    global file_path_excel
    file_path_excel = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])   
    
    if file_path_excel != '':
        search_namee.configure(state='normal')
        search_buttone.configure(state='normal')
    else:
        no_excel()
        
    
    
    
def search_name():
    global intime_list
    global outtime_list
    global person_data_list
    name = input_name.get()
    
    file_input = os.path.abspath(file_path_excel)
    df = pd.read_excel(file_input)
    name_list = df['Name'].values.tolist()
    name_list = [word.lower() for word in name_list]
    name = name.lower()
    result = df.loc[df['Name'].str.lower() == name.lower()]
    if result.empty:
        noname()
    else:
        name_search() 
    #result = df.loc[df['Name'].str.lower() == name.lower()]
    #convert to list 
    
    for i in range(len(name_list)):
        pattern = pattern = '^'+name+'.*'
        if re.search(pattern, name_list[i]):
         
         matched_name.append(name_list[i])
         company = df.Company[df['Name'].str.lower() == name_list[i]].values[0]
         company_list.append(company)
         intime = df.In_time[df['Name'].str.lower() == name_list[i]].values[0]
         
         intime_list.append(str(intime))
         outtime = df.Out_time[df['Name'].str.lower() == name_list[i]].values[0]
         
         outtime_list.append(str(outtime))
         tup = (name_list[i],company,intime,outtime)
         person_data_list.append(tup)
# =============================================================================
#     if result.empty:
#         noname()
#         
#     else:
#         name_search()
#         person_data = df[df['Name'].str.lower() == name.lower()]
#         intime = df.In_time[df['Name'].str.lower() == name.lower()].values[0]
#         intime_list.append(intime)
#         outtime = df.Out_time[df['Name'].str.lower() == name.lower()].values[0]
#         outtime_list.append(outtime)
# =============================================================================
    # print(person_list)
    # for i, row in enumerate(person_data):
    #     for j, cell_value in enumerate(row):
    #         tk.Label(tabel, text=cell_value).grid(row=i, column=j)
    
    # df1.insert(0,column='Name',value=matched_name)
    # df1.insert(1,column='Company',value=company_list)
    # df1.insert(2,column='In_Time',value=intime_list)
    # df1.insert(3,column='Out_Time',value=outtime_list)
    # print(df1)
    thumbnail()
    
    return intime_list,outtime_list,person_data_list
     
def search_company():
    global intime_list
    global outtime_list
    name = input_name.get()
    
    file_input = os.path.abspath(file_path_excel)
    df = pd.read_excel(file_input)
    name = name.lower()
    filtered_df = df[df["Company"].str.lower() == name]
    name_list = filtered_df["Name"].values.tolist()
    name_list = [word.lower() for word in name_list]
    result = df.loc[df['Company'].str.lower() == name.lower()]
    if result.empty:
        print("noname1()")
    else:
        name_search1() 
        
       
    #result = df.loc[df['Name'].str.lower() == name.lower()]
    #convert to list 
    for i in range(len(name_list)):
       
         #person_data = df[df['Name'].str.lower() == name.lower()]
         matched_name.append(name_list[i])
         company = df.Company[df['Name'].str.lower() == name_list[i]].values[0]
         company_list.append(company)
         intime = df.In_time[df['Name'].str.lower() == name_list[i]].values[0]
         
         intime_list.append(str(intime))
         outtime = df.Out_time[df['Name'].str.lower() == name_list[i]].values[0]
         
         outtime_list.append(str(outtime))
         tup = (name_list[i],company,intime,outtime)
         person_data_list.append(tup)
# =============================================================================
#     if result.empty:
#         noname()
#         
#     else:
#         name_search()
#         person_data = df[df['Name'].str.lower() == name.lower()]
#         intime = df.In_time[df['Name'].str.lower() == name.lower()].values[0]
#         intime_list.append(intime)
#         outtime = df.Out_time[df['Name'].str.lower() == name.lower()].values[0]
#         outtime_list.append(outtime)
# =============================================================================
    thumbnail()
    return intime_list,outtime_list   

    
def trim_video():
    global trim
    trim = tk.Toplevel(root)
    trim.title("Trim Video")
    trim.geometry("640x480")
    tabControl = ttk.Notebook(trim)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    
    
    tabControl.add(tab1, text ='Search By Name')
    tabControl.add(tab2, text ='Search By Time')
    tabControl.add(tab3, text ='Search By Company')
    tabControl.pack(expand = 1, fill ="both")
    ####################################### Tab 1 #####################################
    
    
    #Input data here create icon and mention to upload excel file
    upload_excel = tk.Label(tab1, text = "Select Input excel file", font=('calibre',15, 'bold'))
    upload_excel.grid(row = 0, column=0,padx=5,pady=30)
    icon = PhotoImage(file='excel.png')
    file_btn = tk.Button(tab1, image=icon, width=70,height=60,relief=FLAT ,command=excel_uplaod )
    file_btn.image = icon
    file_btn.grid(row=0, column=1,columnspan=2)
    starttime_label = tk.Label(tab1, text = 'Enter the Name', font=('calibre',15, 'bold'))
    starttime_label.grid(row = 1, column=0,padx=5,pady=5)
    starttime_entry = tk.Entry(tab1,textvariable = input_name,width=15, font=('calibre',10, 'bold'),bg = "yellow")
    starttime_entry.grid(row = 1, column = 1,padx=5,pady=5)
    button = tk.Button(tab1, text='Search', command=search_name)
    button.grid(row = 2, column = 1,padx=5,pady=5,columnspan=2)
    # add search name and check whether name present or not. If name present add next button to get in and out time and trim video
    icon = PhotoImage(file='file_1.png')
    icon1 = PhotoImage(file='trim1.png')
    save_location = tk.Label(tab1, text = 'Save File to', font=('calibre',15, 'bold'))
    save_location.grid(row = 3, column=0,padx=5,pady=30)
    file_btn = tk.Button(tab1, image=icon, width=70,height=60,relief=FLAT ,command=save_file )
    file_btn.image = icon
    file_btn.grid(row=3, column=1,columnspan=2)
    trimtex = tk.Label(tab1, text = 'Trim Video', font=('calibre',15, 'bold'))
    trimtex.grid(row = 4, column=0,padx=5,pady=30)
    trim_btn = tk.Button(tab1, image=icon1, width=150,height=150,relief=FLAT ,command=trimv1)
    trim_btn.image = icon1
    trim_btn.grid(row=4, column=1, columnspan = 2)
    
    
    
    
    ######################################## Tab 2 ####################################
    starttime_label = tk.Label(tab2, text = 'Enter the Start time', font=('calibre',15, 'bold'))
    starttime_label.grid(row = 0, column=0,padx=5,pady=5)
    starttime_entry = tk.Entry(tab2,textvariable = starttime_var,width=15, font=('calibre',10, 'bold'),bg = "yellow")
    starttime_entry.grid(row = 1, column = 0,padx=5,pady=5)
    endtime_label = tk.Label(tab2, text = 'Enter the End time', font=('calibre',15, 'bold'))
    endtime_label.grid(row = 0, column=1,padx=5,pady=5)
    endtime_entry = tk.Entry(tab2,textvariable = endtime_var,width=15, font=('calibre',10, 'bold'),bg = "yellow")
    endtime_entry.grid(row = 1, column = 1,padx=5,pady=5)
    icon = PhotoImage(file='file_1.png')
    icon1 = PhotoImage(file='trim1.png')
    save_location = tk.Label(tab2, text = 'Save File to', font=('calibre',15, 'bold'))
    save_location.grid(row = 3, column=0,padx=5,pady=30)
    file_btn = tk.Button(tab2, image=icon, width=70,height=60,relief=FLAT ,command=save_file )
    file_btn.image = icon
    file_btn.grid(row=3, column=1,columnspan=2)
    trimtex = tk.Label(tab2, text = 'Trim Video', font=('calibre',15, 'bold'))
    trimtex.grid(row = 4, column=0,padx=5,pady=30)
    trim_btn = tk.Button(tab2, image=icon1, width=150,height=150,relief=FLAT ,command=trimv)
    trim_btn.image = icon1
    trim_btn.grid(row=4, column=1, columnspan = 2)
    # ffmpeg_extract_subclip("full.mp4", start_seconds, end_seconds, targetname="cut.mp4")
    ############################### Tab 3 ##########################################
    
        #Input data here create icon and mention to upload excel file
    upload_excel = tk.Label(tab3, text = "Select Input excel file", font=('calibre',15, 'bold'))
    upload_excel.grid(row = 0, column=0,padx=5,pady=30)
    icon = PhotoImage(file='excel.png')
    file_btn = tk.Button(tab3, image=icon, width=70,height=60,relief=FLAT ,command=excel_uplaod )
    file_btn.image = icon
    file_btn.grid(row=0, column=1,columnspan=2)
    starttime_label = tk.Label(tab3, text = 'Enter the Company Name', font=('calibre',15, 'bold'))
    starttime_label.grid(row = 1, column=0,padx=5,pady=5)
    starttime_entry = tk.Entry(tab3,textvariable = input_name,width=15, font=('calibre',10, 'bold'),bg = "yellow")
    starttime_entry.grid(row = 1, column = 1,padx=5,pady=5)
    button = tk.Button(tab3, text='Search', command=search_company)
    button.grid(row = 2, column = 1,padx=5,pady=5,columnspan=2)
    # add search name and check whether name present or not. If name present add next button to get in and out time and trim video
    icon = PhotoImage(file='file_1.png')
    icon1 = PhotoImage(file='trim1.png')
    save_location = tk.Label(tab3, text = 'Save File to', font=('calibre',15, 'bold'))
    save_location.grid(row = 3, column=0,padx=5,pady=30)
    file_btn = tk.Button(tab3, image=icon, width=70,height=60,relief=FLAT ,command=save_file )
    file_btn.image = icon
    file_btn.grid(row=3, column=1,columnspan=2)
    trimtex = tk.Label(tab3, text = 'Trim Video', font=('calibre',15, 'bold'))
    trimtex.grid(row = 4, column=0,padx=5,pady=30)
    trim_btn = tk.Button(tab3, image=icon1, width=150,height=150,relief=FLAT ,command=trimv1)
    trim_btn.image = icon1
    trim_btn.grid(row=4, column=1, columnspan = 2)
    
    
    
    
    
    
    
    
    
def exit1():
#=============================================================================
    global name_list
    global time_list
    global intime_list
    global outtime_list
    global matched_name
    global date_list
    global company_list
    global person_data_list
    global option_list
    name_list = []
    time_list = []
    intime_list = []
    outtime_list = []
    matched_name = []
  
    date_list = []
    company_list = []
    person_data_list = []
    option_list=[]
    input_name.set("")
    root.destroy()
#=============================================================================
    
def optionmenu_callback(choice):
    
    print("optionmenu dropdown clicked:", choice)
    option_list.append(choice)
    if choice =="Search By Name":
        search_name()
    elif choice =="Search By Company Name":
        search_company()
        
def search_select():
    value = input_name.get().lower()
    file_input = os.path.abspath(file_path_excel)
    df = pd.read_excel(file_input)
    result = df.loc[df['Name'].str.lower() == value.lower()]
    result1 = df.loc[df["Company"].str.lower() ==  value.lower()]
    choice =''
    if (len(result)!=0):
       search_name()
       choice = "Search By Name"
       option_list.append(choice)
    if (len(result1)!=0):
       search_company()
       choice =="Search By Company Name"
       option_list.append(choice)
    else:
        print("noname1()")
def optionmenu_callback1():
    choice = option_list[0]
    if choice =="Search By Name":
        trimv1()
    elif choice =="Search By Company Name":
        trimv1()
    elif choice =="Search By In-Time":   
        trimv()

def change_appearance_mode_event(new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

def thumbnail():
    global thumbnail_images
    print("Here need to get thumbnail for each names and display in table format with button")
    clip = VideoFileClip(file_path)
    
    for i in range (len(intime_list)):
        
        skip_time = intime_list[i]
        
        ftr = [3600,60,1]
    
        x = sum([a*b for a,b in zip(ftr, map(int,skip_time.split(':')))])
        y = sum([a*b for a,b in zip(ftr, map(int,time_value.split(':')))])
        z=x-y
        time_to_sec.append(z)
          
        # Capture the frame at the specified time
        frame = clip.get_frame(z)
        
        # Convert the NumPy array to a PIL Image object
        image = Image.fromarray(frame)
        # Resize the image to a thumbnail size
        thumbnail_size = (100,60 )
        image.thumbnail(thumbnail_size)

        # Convert the PIL Image object to a PhotoImage object
        photo = ImageTk.PhotoImage(image)
        
        # Append the PhotoImage object to the list of thumbnail images
        thumbnail_images.append(photo)
    table_view()
    # Close the clip
    clip.close()
    
    
    return thumbnail_images
          
# =============================================================================
# def thumbnail_view():
#      # Create the table
#     # table1 = ttk.Treeview(tabel1, show="headings", yscrollcommand=scrollbar.set)
#     # table1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#     # # Set the scrollbar to adjust the table
#     #scrollbar1.config(command=table1.yview)
#     print("view thumbnail in button and assign functions")     
#   
#     search = ctk.CTkLabel(master=side_frame, text="Video Thumbnail results",font=('calibre',20, 'bold'))
#     search.place(relx=0.2, rely=0.6)
#     #for i in range(len(thumbnail_images)):
#     # Convert the PIL image to a tkinter PhotoImage
#         # img = ImageTk.PhotoImage(thumbnail_images[i])
#         # button = tk.Button(tabel1, image=img, command=lambda i=i: skip(time_to_sec[i]))
#         # button.image = img  # Save a reference to the image to prevent garbage collection
#         # button.grid(row=i, column=0)
#         # buttons.append(button)
#         # Add the thumbnail images to buttons
#     for i, image in enumerate(thumbnail_images):
#        
#         
#         button = tk.Button(side_frame, image=image, command=lambda i=i: skip(time_to_sec[i]))
#         
#         button.pack(side=tk.LEFT, padx=10)
#     table_view()
# =============================================================================
    
# =============================================================================
# def table_view():
#     # button_list = []
#     # for i, image in enumerate(thumbnail_images):
#        
#         
#     #     button = tk.Button(side_frame, image=image, command=lambda i=i: skip(time_to_sec[i]))
#         
#     #     button.pack(side=tk.LEFT, padx=10)
#     #     button_list.append(button)
#     #     # create a new list of tuples with the image values inserted into each tuple
#     # new_list = []
#     # for tup, img_val in zip(person_data_list, button_list):
#     #     new_tup = tup + (img_val,)
#     #     new_list.append(new_tup)
#     # Create the table
#     table = ttk.Treeview(tabel, columns=("Name", "Company", "In_Time", "Out_Time"), show="headings", yscrollcommand=scrollbar.set)
#     table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#     
#     # Set the scrollbar to adjust the table
#     scrollbar.config(command=table.yview)
#  
#     # Set the width of each column
#     table.column("Name", width=50, anchor="center")
#     table.column("Company", width=150, anchor="center")
#     table.column("In_Time", width=50, anchor="center")
#     table.column("Out_Time", width=50, anchor="center")
#     
#     # Set the headings for each column
#     table.heading("Name", text="Name")
#     table.heading("Company", text="Company")
#     table.heading("In_Time", text="In_Time")
#     table.heading("Out_Time", text="Out_Time")
#     
#         
#     # Insert the data into the table
#     for i, d in enumerate(person_data_list):
#         table.insert("", "end", values=d)
#          # Create a button for each 
#         button = tk.Button(table, image=thumbnail_images[i], command=lambda i=i: skip(time_to_sec[i]))
#         button.grid(row=i, column=2)
#     table.pack()
#          
#         
# 
# 
# =============================================================================

def table_view():
        # create a frame for the table
    tabel = tk.Frame(main_container, bd=2, relief=tk.SUNKEN, height=200,width=200)
    #tabel = ctk.CTkFrame(main_container)
    tabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Create the scrollbar for the table
    scrollbar = tk.Scrollbar(tabel)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    # create the table header
   # Set the scrollbar to adjust the table
   # scrollbar.config(command=tabel.yview)
#  
    tk.Label(tabel, text="Name", padx=10, pady=10).place(x=50, y=10)
    tk.Label(tabel, text="Company", padx=10, pady=10).place(x=150, y=10)
    tk.Label(tabel, text="In_Time", padx=10, pady=10).place(x=250, y=10)
    tk.Label(tabel, text="Out_Time", padx=10, pady=10).place(x=350, y=10)
    tk.Label(tabel, text="Video_Thumbnail", padx=10, pady=10).place(x=450, y=10)
    
    # loop through the data and create the rows
    for i, (name, company, intime, outtime) in enumerate(person_data_list):
        # add the name, company, intime and outtime to the row
        tk.Label(tabel, text=name, padx=10, pady=10).place(x=50, y=40+i*30)
        tk.Label(tabel, text=company, padx=10, pady=10).place(x=150, y=40+i*30)
        tk.Label(tabel, text=intime, padx=10, pady=10).place(x=250, y=40+i*30)
        tk.Label(tabel, text=outtime, padx=10, pady=10).place(x=350, y=40+i*30)
    
        # add a button with an image to the row
      
        button = tk.Button(tabel, image=thumbnail_images[i], command=lambda i=i: skip(time_to_sec[i]))
        button.image = thumbnail_images[i]
        button.place(x=450, y=40+i*30)
    
    search_namee.configure(state="disabled")
    search_buttone.configure(state="disabled")
    exit_buttone.configure(state='normal')
def selectandplay():
    print("Select video and play")




root = tk.Tk()
root.title("Tkinter media")
root.geometry("1920x1080")
time_var=tk.StringVar()
jumptime_var=tk.StringVar()
starttime_var = tk.StringVar()
input_name = tk.StringVar()
endtime_var = tk.StringVar()
search_var = tk.StringVar()
main_container = tk.Frame(root)
main_container.pack(fill="both")
# Set the maximum size of the frame to 400x400
main_container.pack_propagate(False)
main_container.config(width=750, height=750)
side_frame = ctk.CTkFrame(main_container)
side_frame.pack(side="left", fill="both")

search = ctk.CTkLabel(master=side_frame, text="Search",font=('calibre',20, 'bold'))
search.place(relx=0.2, rely=0.0)
upload_excel = ctk.CTkLabel(master=side_frame, text = "Select Input Excel file", font=('calibre',15, 'bold'))
upload_excel.place(relx=0.1, rely=0.05)
upload_excel.configure(state="disabled")

icon = PhotoImage(file='excel.png')
icon2 = PhotoImage(file='file_1.png')
icon1 = PhotoImage(file='trim1.png')
e_btn = ctk.CTkButton(side_frame, image=icon, width=70,height=60 ,text = "",command=excel_uplaod )
e_btn.image = icon
e_btn.place(relx=0.2, rely=0.12)
e_btn.configure(state="disabled")
search_namee = ctk.CTkEntry(master = side_frame,textvariable = input_name, font=('calibre',20,'normal'))
search_namee.place(relx=0.12, rely=0.25)
search_namee.configure(state="disabled")
search_buttone = ctk.CTkButton(master=side_frame, text = "Search", width=110,height=30,command=search_select)
# file_btn.image = icon
search_buttone.place(relx=0.2, rely=0.35)
search_buttone.configure(state="disabled")

exit_buttone = ctk.CTkButton(master=side_frame, text = "Exit", width=110,height=30,fg_color = 'red',command=exit1)
# file_btn.image = icon
exit_buttone.place(relx=0.2, rely=0.45)
exit_buttone.configure(state="disabled")
# =============================================================================
# combobox = ctk.CTkOptionMenu(master=side_frame,
#                                        values=["Search By Name", "Search By Company Name", "Search by In-Time"],
#                                        command=optionmenu_callback)
# combobox.place(relx=0.1, rely=0.32)
# combobox.set("Search By Name")  # set initial value
# combobox.configure(state="disabled")
# =============================================================================
# save_location = ctk.CTkLabel(master=side_frame, text = 'Save File to', font=('calibre',15, 'bold'))
# save_location.place(relx=0.15, rely=0.40)
# file_btn = ctk.CTkButton(master=side_frame, image=icon2, width=70,height=60,command=save_file,text = "" )
# file_btn.image = icon
# file_btn.place(relx=0.2, rely=0.45)
# file_btn.configure(state="disabled")
# trim_btn = ctk.CTkButton(master=side_frame,command=optionmenu_callback1,text = "Trim")
# trim_btn.place(relx=0.12, rely=0.60)
# trim_btn.configure(state="disabled")
appearance_mode_label = ctk.CTkLabel(side_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.place(relx=0.15, rely=0.85)
appearance_mode_optionemenu = ctk.CTkOptionMenu(side_frame, values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
appearance_mode_optionemenu.place(relx=0.12, rely=0.90)
video_frame = tk.Frame(main_container)
video_frame.pack(side ="right",fill="both", expand=True)
# Set the maximum size of the frame to 400x400
video_frame.pack_propagate(False)
#video_frame.config(width=700, height=700)
load_btn = ctk.CTkButton(master = video_frame, text="Start", command=load_video)
load_btn.pack()

# =============================================================================
# 
# time_label = tk.Label(root, text = 'Enter the time', font=('calibre',10, 'bold'))
# time_label.pack()
# time_label.place(x=0,y=0)
# time_entry = tk.Entry(root,textvariable = time_var,width=15, font=('calibre',10, 'bold'),bg = "yellow")
# time_entry.pack(side="left")
# time_entry.place(x=100,y=0)
# time_btn = tk.Button(root, text="Time Update",font=('calibre',10, 'bold'), command=time_enter)
# time_btn.pack(side="left")
# time_btn.place(x=220,y=0)
# =============================================================================
vid_player = TkinterVideo(scaled=True, master=video_frame)
vid_player.pack(expand = True,fill="both")

control_frame = ctk.CTkFrame(video_frame)
control_frame.pack(fill="x")

play_pause_btn = tk.Button(master=control_frame, text="Play", width=15,height=1,bg="yellow",command=play_pause)
play_pause_btn.pack()
play_pause_btn.configure(state="disabled")
# trim_btn = tk.Button(video_frame, text="Trim Video",font=('calibre',15, 'bold'), bg="lightblue" , command=trim_video)
# trim_btn.pack(side="left", expand=True)
# trim_btn.place(x=950,y=0)

skip_plus_5sec1 = ctk.CTkButton(master=control_frame, text="Skip -5 sec", command=lambda: skip(-5),fg_color = 'green')

skip_plus_5sec1.place(relx=0.225, rely=0)
skip_plus_5sec1.configure(state="disabled")

progress_value = ctk.IntVar(master=control_frame)

progress_slider = tk.Scale(control_frame, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
# progress_slider.bind("<ButtonRelease-1>", seek)
progress_slider.pack(side="left", fill="x", expand=True)
progress_slider.configure(state="disabled")
end_time = tk.Label(master=control_frame, text=str(datetime.timedelta(seconds=0)), font=('calibre',15, 'bold'))
end_time.place(relx=0.92, rely=0.0)

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended )

skip_plus_5sec = ctk.CTkButton(master=control_frame, text="Skip +5 sec", command=lambda: skip(5),fg_color = 'green')
skip_plus_5sec.place(relx=0.65, rely=0)
skip_plus_5sec.configure(state="disabled")

# # Create the scrollbar for the table
# scrollbar1 = tk.Scrollbar(side_frame)
# scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)


root.mainloop()