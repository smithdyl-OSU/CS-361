# Author: Dylan Smith
# Class: CS 361
# Description: This software is a password generator, which takes a desired length and additional, optional user
# parameters such as "needs symbol" and returns a randomized password for the user. Additionally contains the option
# for the user to click a "give me inspiration" button which invokes a webscraper to get Wikipedia article titles for
# inspiration for users to come up with their own human-friendly passwords.

import tkinter as tk
import webbrowser
import random
import string

# Creates the main window of the program
root = tk.Tk()
root.title('Password Generator')
root.geometry('500x250')


def link(url):
    webbrowser.open_new(url)


def advanced():
    window = tk.Toplevel(root)
    window.title('Advanced Settings')
    window.geometry('300x150')
    frame = tk.Frame(window)
    frame.pack(side=tk.LEFT)
    text = tk.Message(frame, text='These options will exclude certain characters, reducing the ambiguity of your '
                                  'password:', width=300, justify='left')
    text.grid(row=0)
    similar_var = tk.IntVar()
    ambiguous_var = tk.IntVar()
    tk.Checkbutton(frame, text='Exclude Similar Characters (e.g. o, O, 0, l, I)',
                   variable=similar_var).grid(row=1, sticky=tk.W)
    tk.Checkbutton(frame, text='Exclude Ambiguous Characters (e.g. "`\'{}()[])',
                   variable=ambiguous_var).grid(row=2, sticky=tk.W)
    close = tk.Button(frame, text='Close', command=window.withdraw)
    close.grid(row=3, column=0)


def about():
    window = tk.Toplevel(root)
    window.title('About')
    window.geometry('450x300')
    frame = tk.Frame(window)
    frame.pack(side=tk.LEFT)
    text = tk.Message(frame, text='Q - What is this program?\n'
                                  'A - This program is meant to help users create secure passwords that they can use '
                                  'for a variety of sites, entering the parameters that their site requires.\n\n'
                                  'Q - What if I don\'t want to input parameters, or don\'t know what to put?\n'
                                  'A - The program will still generate a password, using default conditions.\n'
                                  'The following are the default conditions should the user provide no parameters of '
                                  'their own:\n'
                                  'Password length: 12-16 characters\n'
                                  'Options included: Uppercase letters, lowercase letters, and symbols.\n\n'
                                  'Q - What is the inspiration button for?\n'
                                  'A - This button is meant to provide users with inspiration to create their own '
                                  'passwords instead of using the generator to create a random one. Users are advised '
                                  'that such passwords may not be as secure as randomly generated passwords. To learn '
                                  'more, please navigate to help -> learn more for resources on password security.',
                      width=450, justify='left')
    text.pack()
    close = tk.Button(frame, text='Close')
    close.pack()


def learn():
    window = tk.Toplevel(root)
    window.title('Learn More')
    window.geometry('300x150')
    frame = tk.Frame(window)
    frame.pack(side=tk.LEFT)
    text = tk.Message(frame, text='To learn more about password security, check out the following resources:',
                      width=300, justify='left')
    text.pack()
    link1 = tk.Message(frame, text='https://www.security.org/',
                       fg='blue', cursor='hand2', width=300, justify='left')
    link1.pack()
    link1.bind('<Button-1>', lambda e: link('https://www.security.org/how-secure-is-my-password/'))
    link2 = tk.Message(frame, text='https://www.techsafety.org/',
                       fg='blue', cursor='hand2', width=300, justify='left')
    link2.pack()
    link2.bind('<Button-1>', lambda e: link('https://www.techsafety.org/passwordincreasesecurity'))
    link3 = tk.Message(frame, text='https://www.connectsafely.org/',
                       fg='blue', cursor='hand2', width=300, justify='left')
    link3.pack()
    link3.bind('<Button-1>', lambda e: link('https://www.connectsafely.org/passwords/'))
    close = tk.Button(frame, text='Close')
    close.pack()


# The top menu, includes 'file' and 'about' buttons
menu = tk.Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Clear')
filemenu.add_command(label='Undo')
filemenu.add_command(label='Advanced', command=advanced)
filemenu.insert_separator(index=4)
filemenu.add_command(label='Exit', command=root.quit)
helpmenu = tk.Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=about)
helpmenu.add_command(label='Learn more', command=learn)

# The main frames of the window, where most content will go
frame = tk.Frame(root)
frame.pack(side=tk.LEFT)
rightframe = tk.Frame(root)
rightframe.pack(side=tk.RIGHT)

# Additional bottom frame for organizing features
bottomframe = tk.Frame(root)
bottomframe.pack(side=tk.BOTTOM)

# Creates password options as check boxes
require_upper_case = tk.IntVar()
require_lower_case = tk.IntVar()
require_number = tk.IntVar()
require_symbol = tk.IntVar()
min_chars = tk.StringVar()
max_chars = tk.StringVar()
tk.Checkbutton(frame, text='Include Upper Case Letter (ABCDE)', variable=require_upper_case).grid(row=0, sticky=tk.W)
tk.Checkbutton(frame, text='Include Lower Case Letter (abcde)', variable=require_lower_case).grid(row=1, sticky=tk.W)
tk.Checkbutton(frame, text='Include Numbers (12345)', variable=require_number).grid(row=2, sticky=tk.W)
tk.Checkbutton(frame, text='Include Symbol (!@#$%)', variable=require_symbol).grid(row=3, sticky=tk.W)

# Creates max and min characters needed input boxes
tk.Label(frame, text='Minimum Characters').grid(row=4, column=0)
tk.Label(frame, text='Maximum Characters').grid(row=5)
min_entry = tk.Entry(frame, textvariable=min_chars).grid(row=4, column=1)
max_entry = tk.Entry(frame, textvariable=max_chars).grid(row=5, column=1)

generate_output = tk.Message(frame, text='')
generate_output.grid(row=6, column=0)


def generate_password(length):
    """
    Randomly generates a password for the user.
    :param length: integer, the number of random characters to generate for the password
    :return:
    """
    multi = string.ascii_letters + string.digits + string.punctuation
    temp = ''
    required = generate_required()
    for char in required:
        length -= 1
    if length != 0:
        temp = ''.join(random.choice(multi) for i in range(length))
    temp = temp + required
    password = ''.join(random.sample(temp, len(temp)))
    return password


def generate_required():
    """
    Checks for user specified requirements for password.
    :return: string, containing one randomized character from each category requested by user
    """
    upper_temp = lower_temp = number_temp = symbol_temp = ''
    if require_upper_case.get() == 1:
        upper_temp = ''.join(random.choice(string.ascii_uppercase))
    if require_lower_case.get() == 1:
        lower_temp = ''.join(random.choice(string.ascii_lowercase))
    if require_number.get() == 1:
        number_temp = ''.join(random.choice(string.digits))
    if require_symbol.get() == 1:
        symbol_temp = ''.join(random.choice(string.punctuation))
    return upper_temp + lower_temp + number_temp + symbol_temp


def generate_clicked():
    """
    Displays randomly generated password on GUI.
    """
    length = calc_length(min_chars.get(), max_chars.get())
    password = generate_password(length)
    new_text = "Your password is: " + password
    generate_output.configure(text=new_text)


def calc_length(min_len, max_len):
    """
    :param min_len: string, user input minimum allowed length for password
    :param max_len: string, user input maximum allowed length for password
    :return: integer, the random length between min_len and max_len (8-16 by default if no user input)
    """
    if min_len != '':
        min_len = int(min_len)
    else:
        min_len = 8
    if max_len != '':
        max_len = int(max_len)
    else:
        max_len = 17
    return random.randrange(min_len, max_len + 1)


def inspiration_clicked():
    new_text = "Here's some inspiration: Skouterios"
    inspiration_output.configure(text=new_text)


generate = tk.Button(frame, text='Generate Password', command=generate_clicked)
generate.grid(row=7, column=0)

# Displays explanation of inspiration button
inspiration_text = tk.Message(rightframe, text='Want inspiration to make your own password? Click the \'give me '
                                               'inspiration\' button below, and get some ideas!')
inspiration_text.pack()
filler = tk.Message(rightframe, text='')
filler.pack()

inspiration_output = tk.Message(rightframe, text='')
inspiration_output.pack()

inspiration = tk.Button(rightframe, text='Give me inspiration', command=inspiration_clicked)
inspiration.pack()

root.mainloop()