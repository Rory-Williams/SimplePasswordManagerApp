import tkinter.messagebox
from tkinter import *
from random import randint, choice, shuffle
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def gen_pw():
    pw_entry.delete(0,END)
    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    shuffle(password_list)
    password_list = ''.join(password_list)
    pw_entry.insert(0, password_list)
    window.clipboard_clear()
    window.clipboard_append(password_list)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_pw():
    website = web_entry.get()
    user = email_entry.get()
    password = pw_entry.get()
    if len(website)*len(user)*len(password)==0:
        print('opps')
        empty_warn = tkinter.messagebox.askyesno(title='Missing Entry', message='Missing entry, continue?')
        print(empty_warn)
        if empty_warn:
            save_pw(website, user, password)
    else:
        save_pw(website, user, password)

def save_pw(website, user, password):
    pw_data = f'{website} | {user} | {password}\n'
    new_data = {
        website: {
            'email' : user,
            'password' : password
        }
    }
    save_warn = tkinter.messagebox.askyesno(title='Save entry?', message=f'Save entry?: \n {pw_data}')
    if save_warn:
        # with open('passwords.txt', 'a') as file:
        #     file.write(pw_data)
        try:
            with open('passwords.json', 'r') as file:
                #Read data
                json_data = json.load(file)
                #Update data
                json_data.update(new_data)

            with open('passwords.json', 'w') as file:
                json.dump(json_data, file, indent=4)
        except FileNotFoundError:
            with open('passwords.json', 'w') as file:
                json.dump(new_data, file, indent=4)
                print('created new json file')

        web_entry.delete(0, END)
        pw_entry.delete(0, END)
        email_entry.delete(0, END)
        email_entry.insert(0, '@hotmail.co.uk')

def search():
    try:
        with open('passwords.json', 'r') as file:
            # Read data
            stored_data = json.load(file)
            website = web_entry.get()
        if len(web_entry.get())>0:
            if website in stored_data:
                stored_email = stored_data[website]['email']
                stored_pw = stored_data[website]['password']
                print(f'{website}, {stored_email}, {stored_pw}')
                email_entry.delete(0, END)
                email_entry.insert(0, stored_email)
                pw_entry.delete(0, END)
                pw_entry.insert(0, stored_pw)
            else:
                tkinter.messagebox.showinfo(title='PWFile Error', message='No Passwords exist for that website')
        else:
            tkinter.messagebox.showinfo(title='PWFile Error', message='Please enter website to search for')

    except FileNotFoundError:
        tkinter.messagebox.showinfo(title='PWFile Error',message='No Passwords Storage Created')




# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Generator')
window.config(padx=20, pady=20) #add padding to window component

canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file='logo.png')
canvas.create_image(100,100,image=img)
canvas.grid(column=2,row=1)

web_label = Label(text='Website:', font=('Arial',12,'bold'))
web_label.grid(column=1,row=2,sticky=E)
web_label.config(padx=20, pady=20)

user_label = Label(text='Email/Username:', font=('Arial',12,'bold'))
user_label.grid(column=1,row=3,sticky=E)
user_label.config(padx=20, pady=20)

pw_label = Label(text='Password:', font=('Arial',12,'bold'))
pw_label.grid(column=1,row=4,sticky=E)
pw_label.config(padx=20,pady=20)

gen_button = Button(text='Generate Password', command=gen_pw)
gen_button.grid(column=3,row=4,sticky=W)
gen_button.config(padx=0, pady=5, height=1, width=15)

add_button = Button(text='Add', command=add_pw)
add_button.grid(column=2,row=5,columnspan=2)
add_button.config(padx=0, pady=10, height=1, width=40)

search_button = Button(text='Search', command=search)
search_button.grid(column=3,row=2)
search_button.config(padx=0, pady=5, height=1, width=15)

web_entry = Entry(width=25)
web_entry.grid(column=2,row=2,sticky=W)
web_entry.focus()

email_entry = Entry(width=50)
email_entry.grid(column=2,row=3,columnspan=2,sticky=W)
email_entry.insert(0,'@hotmail.co.uk')

pw_entry = Entry(width=25)
pw_entry.grid(column=2,row=4, sticky=W)

window.mainloop()