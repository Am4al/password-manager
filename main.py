from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

def generate_pass():
    letter=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','U','V','W','X','Y','Z']
    number=['0','1','2','3','4','5','6','7','8','9']
    symbol=['@','#','$','&','!','*']

    l=random.randint(4,8)
    n=random.randint(2,4)
    s=random.randint(2,4)

    password=[]
    for i in range(0,l):
        password.append(random.choice(letter))
    for i in range(0,n):
        password.append(random.choice(number))
    for i in range(0,s):
        password += random.choice(symbol)

    random.shuffle(password)

    final_password=""
    for i in password:
        final_password += i

    pass_entry.insert(0,final_password)
    pyperclip.copy(final_password)

def save():
    website = web_entry.get()
    email = email_entry.get()
    password = pass_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please fill every field")
    else:
        try:
            with open("data.json", "r") as data_file:
                #reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data,data_file, indent=4)
        else:
            #updating old data with nem data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                #saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            web_entry.delete(0, END)
            email_entry.delete(0, END)
            pass_entry.delete(0, END)


def find_pass():
    website = web_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website}.")

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="lock.png")
canvas.create_image(110,100,image=logo_img)
canvas.grid(row=0,column=1)

#Labels
website_label = Label(text="Website")
website_label.grid(row=1,column=0)
email_label = Label(text="Email/Username")
email_label.grid(row=2,column=0)
password_label = Label(text="Password")
password_label.grid(row=3,column=0)

#entries
web_entry = Entry(width=32)
web_entry.grid(row=1,column=1)
web_entry.focus()
email_entry = Entry(width=50)
email_entry.grid(row=2,column=1,columnspan=2)
# email_entry.insert(0, "Example@gmail.com")
pass_entry = Entry(width=32)
pass_entry.grid(row=3,column=1)

#button
search_button = Button(text="Search",width=14,command=find_pass)
search_button.grid(row=1,column=2)
generate_password_button = Button(text="Generate Password",width=14, command=generate_pass)
generate_password_button.grid(row=3,column=2)
add_button = Button(text="Add", width=42, command=save)
add_button.grid(row=4,column=1,columnspan=2)


window.mainloop()