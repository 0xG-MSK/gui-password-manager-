
#=========backend
import tkinter as tk
from tkinter import END
from tkinter import messagebox
import string as s
import math as m
import random as rd
import json

PASSWORD_LENGHT = 16
root = tk.Tk()

def save_details():
    website_name = entry_website.get()
    username_email = entry_email.get()
    password = entry_password.get()
    new_credentials = {
        website_name:{
            "email": username_email,
            "password": password
        }
    }
    
    if len(website_name) <=0 or len(password) <=0 or len(username_email) <=0:
        messagebox.showwarning(title='Empty fields', message="Please fill all fields")
    
    else:
        is_ok = messagebox.askokcancel(title=f'{website_name}? Save it?', message=f"Is it ok to save \nEmail: {username_email} \nPassword: {password}")
        if is_ok:
           try:
               with open("database.json", mode='r') as database:
                   data = json.load(database)
           except:
               with open("database.json", mode="w") as database:
                   json.dump(new_credentials, database, indent=4)   
           else:
               data.update(new_credentials)
               with open("database.json", mode="w") as database:
                   json.dump(data, database, indent=4)
           #clear screen     
           entry_website.delete(0, END)
           entry_email.delete(0, END)
           entry_password.delete(0, END)
           #notify
           def notify():
               notification = tk.Label(root, text="List Updated", 
                   font=('Times New Roman', 7, 'normal'),
                   fg='#237ade', bg='#bfd7e0',
                   command=None,
                   relief=None, bd=None,
                   padx=20, pady=0)
               notification.place(x=550,y=90)
               root.after(3000, lambda: notification.destroy())
           
           notify()
        else:
            pass
            
def show_credentials():
    website = entry_website.get()
    try:
        with open('database.json', mode='r') as database:
            data = json.load(database)
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='Data File Not Found')
    except:
        messagebox.showerror(title='Error', message='No Data Found')
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=f'{website} website', message=f"Username/Email: {email}\nPassword: {password}")
            
#...generate password
#basic characters
letters_lower = list(s.ascii_letters[0:26])
letters_upper = list(s.ascii_letters[26:52])
digits = list(s.digits)
symbols = ['$','(',')','#','!','?','_','&','%','@','.']
#password lenght
pass_lenght= PASSWORD_LENGHT
equal_pass_ratio= round((pass_lenght/4),1)
#
par_password = []
#
for lower in range(0,m.floor(equal_pass_ratio)):
    random_l_lower = rd.choice(letters_lower)
    par_password += random_l_lower
dynamic_condition1= 0
while dynamic_condition1 < m.floor(equal_pass_ratio):
    random_l_upper = rd.choice(letters_upper)
    par_password += random_l_upper
    dynamic_condition1 += 1
for upper in range(m.ceil(equal_pass_ratio)):
    random_digits = rd.choice(digits)
    par_password += random_digits
#remaining
remainder = pass_lenght-len(par_password)
#
dynamic_condition2 = 0
while dynamic_condition2 < remainder:
    random_symbols = rd.choice(symbols)
    par_password += random_symbols
    dynamic_condition2 += 1
#shuffle
rd.shuffle(par_password)
password = "".join(par_password)

def show_password():
    entry_password.insert(0, password)
    
#-----------------------------------------------frontend
root.title("Sitso's Password Generator")
root.config(padx=20, pady=20,)

canvas = tk.Canvas(root, width=200, height=200 ,bg=None)
bg_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=bg_img)
canvas.grid(column=1, row=0, padx=(90,0))

#---website input
label_website = tk.Label(root, text='Website:')
label_website.grid(column=0, row=1)
entry_website = tk.Entry(root, width=21)
entry_website.focus()
entry_website.grid(column=1, row=1, columnspan=None, pady=(0,5), padx=(0, 0))

#>>> search button
button_search = tk.Button(root, text="Search", 
    command=show_credentials,
    width=13, 
    font=('Ariel', 5, 'normal'),
    fg='#1dc9cf', bg=None,
    activebackground='#3283a8')
# Add padding to the button to create space from the entry box
button_search.grid(column=2, row=1, padx=(0, 0), pady=(0, 5))  # Adjust padx as needed

#== email/username input
label_email = tk.Label(root, text='Email/Username:')
label_email.grid(column=0, row=2)
entry_email = tk.Entry(root, width=35)
#entry_email.insert(0, "youremail@host.com")
entry_email.grid(column=1, row=2, columnspan=2, pady=(0, 5))

#___ password input
label_password = tk.Label(root, text="Password:")
label_password.grid(column=0, row=4)
entry_password = tk.Entry(root, width=21)
entry_password.grid(column=1, row=4, padx=(0, 0), pady=(0,0))

#>>>> generate button
button_generate = tk.Button(root, text="Generate password", 
    command=show_password, 
    font=('Ariel', 5, 'normal'),
    fg='#1dc9cf', bg=None,
    activebackground='#3283a8')
button_generate.grid(column=2, row=4, padx=(0, 0), pady=(0, 0))

#add button
button_add = tk.Button(root, text="Update List", 
    command=save_details, 
    font=('Ariel', 5, 'normal'),
    fg='#1dc9cf', bg=None,
    activebackground='#3283a8')
button_add.grid(column=1, row=5, padx=(0, 0), pady=(3, 0))

#main run
root.mainloop()