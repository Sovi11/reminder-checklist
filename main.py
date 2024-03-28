# I want to create a file that will open a window every morning and every night to remind me to do my daily tasks in the morning
# and ask me what have I done at the night and then store that information in a file
# I will use the tkinter library to create the window

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import simpledialog
import webbrowser
import schedule
import time 

class Task : 
    def __init__(self, name, description,link=""):
        self.name = name
        self.description = description
        self.done = False
        self.link = link
    
    def display(self):
        print(f"Task: {self.name} - {self.description} - Done: {self.done}")
        # here should be a clickable link to the task
        print(f"Link: {self.link}")

    def open_link(self):
        webbrowser.open(self.link)
    
class Tasks : 
    def __init__(self):
        self.tasks = []
    
    def add(self, task):
        self.tasks.append(task)
    
    def display(self):
        "Task list"
        for task in self.tasks:
            task.display()

    def morning(self):
        root = tk.Tk()
        ## I just want to display all the text on the window
        root.title("Tasks for the day")
        for task in self.tasks:
            task.link = task.link.strip()
            label = tk.Label(root, text= "Name : " + task.name + " \nDescription : " + task.description +"\n")
            if ((len(task.link) == 0) ):
                pass
            else:
                link = tk.Label(root, text="Link : " + task.link, fg="blue", cursor="hand2")
                link.bind("<Button-1>", lambda e: task.open_link())
                link.pack()
            label.pack()
        root.geometry("600x600")
        def done():
            root.destroy()
        # make a button that says read and destroys the window 
        close_button = tk.Button(root, text="Read", command=done)
        close_button.pack()
        root.mainloop()




    def night(self):
        root = tk.Tk()
        root.title("Tasks for the day")

        def save_and_close():
            for idx, task in enumerate(self.tasks):
                task.done = checkboxes[idx].get()
            self.save()
            root.destroy()

        checkboxes = []

        for task in self.tasks:
            done_var = tk.BooleanVar(value=False)
            c = tk.Checkbutton(root, text=task.name, variable=done_var)
            c.pack(anchor=tk.W)
            checkboxes.append(done_var)
        root.geometry("600x400")
        save_button = tk.Button(root, text="Save and Close", command=save_and_close)
        save_button.pack()
        root.mainloop()

    def save(self):
        with open("log.txt", "a") as file:
            file.write("\n")
            file.write(f"{datetime.now().date()}\n")
            for task in self.tasks:
                done = "Yes" if task.done else "No"
                file.write(f"{task.name} - {task.description} - {done}\n")
        print("Tasks saved")

    def load(self):
        with open("tasks.txt", "r") as file:
            for line in file:
                try : name, description , link = line.split(" - ")
                except : name, description = line.split(" - ")
                if (len(link) == 0): 
                    task = Task(name, description)
                else :
                    task = Task(name, description,link)
                self.add(task)
        print("Tasks loaded")


# tasks = Tasks()
# tasks.add(Task("Exercise", "30 minutes of exercise"))
# tasks.add(Task("Meditation", "10 minutes of meditation"))
# tasks.add(Task("Reading", "30 minutes of reading"))

# # tasks.display()
# tasks.night()

def perform_morning_tasks():
    tasks = Tasks()
    tasks.load()
    tasks.morning()

def perform_night_tasks():
    tasks = Tasks()
    tasks.load()
    tasks.night()

perform_morning_tasks()
perform_night_tasks()

# Schedule the function to run every morning at 7:00 AM
schedule.every().day.at("07:00").do(perform_morning_tasks)
schedule.every().day.at("19:00").do(perform_night_tasks)
# Run pending scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(60) 