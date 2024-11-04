import tkinter.messagebox
from tkinter import *
import string
import random
import json


# -----------------------------------Submit button------------------------------------ #
def submission():
    website_name = website.get()
    email_name = email_var.get()
    pw_name = pw_var.get()
    passcodes = {
        website_name: {
            "email": email_name,
            "password": pw_name
        }
    }

    txt_data = f"{website_name} | {email_name} | {pw_name}"

    if len(website_name) == 0 or len(email_name) == 0 or len(pw_name) == 0:
        tkinter.messagebox.showinfo("ALERT MESSAGE", "Please fill all the columns")
        passcodes = None
    else:
        # save to text file for reference
        txt_manager = open("passcode.txt", "a")
        txt_manager.write(txt_data + '\n')
        tkinter.messagebox.showinfo("MESSAGE", "Successfully saved!")

        # save to json file
        try:
            with open('passcode.json', 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('passcode.json', 'w') as data_file:
                json.dump(passcodes, data_file, indent=4)
        else:
            data.update(passcodes)

            with open("passcode.json", 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            pw_entry.delete(0, END)


# -----------------------------------Generate Button------------------------------------ #
def gen_pw():
    string_gen = ''
    i = 0
    small = list(string.ascii_lowercase)
    large = list(string.ascii_uppercase)
    special = list(string.punctuation)
    while i < 18:
        choose = random.choice([small, large, special])
        char = random.choice(choose)
        string_gen += char
        i += 1

    pw_var.set(string_gen)


# -----------------------------------Search the password------------------------------------ #
def find_password():
    site = website_entry.get()
    with open('passcode.json', 'r') as data_file:
        data = json.load(data_file)
        if site in data.keys():
            answer = tkinter.messagebox.askokcancel("Pop-up message",
                                                    "Data saved already! Auto-fill the login details?")
            if answer:
                email_var.set(data[site]["email"])
                pw_var.set(data[site]["password"])
        else:
            print('nothing else')


# -----------------------------------UI SETUP------------------------------------ #
root = Tk()
root.title("Password Manager")
# root.geometry('600x400')
root.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
pw_locker = PhotoImage(file="logo.png")
canvas.create_image(100, 112, image=pw_locker)
canvas.grid(column=1, row=0)

website = StringVar()
email_var = StringVar()
pw_var = StringVar()

website_label = Label(text="Website", font=('Calibri', 10, 'bold'))
website_entry = Entry(textvariable=website)
website_entry.focus()
website_label.grid(column=0, row=2)
website_entry.grid(column=1, row=2, columnspan=3)

email_label = Label(text="Email/Username", font=('Calibri', 10, 'bold'))
email_entry = Entry(textvariable=email_var)
email_label.grid(column=0, row=3)
email_entry.grid(column=1, row=3, columnspan=3)

pw_label = Label(text="Password", font=('Calibri', 10, 'bold'))
pw_entry = Entry(textvariable=pw_var)
pw_label.grid(column=0, row=4)
pw_entry.grid(column=1, row=4)

search_button = Button(text="Search", font=('Calibri', 10, 'bold'), highlightthickness=0, command=find_password)
search_button.grid(column=4, row=2)

generate_button = Button(text="Generate", font=('Calibri', 10, 'bold'), highlightthickness=0, command=gen_pw)
generate_button.grid(column=4, row=4)

submit = Button(text='Add', highlightthickness=0, font=('Calibri', 10, 'normal'), command=submission)
submit.grid(column=1, row=5, columnspan=3)

root.mainloop()
