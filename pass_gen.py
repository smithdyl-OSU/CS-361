# Author: Dylan Smith
# Class: CS 361
# Description: This software is a password generator, which takes a desired length and additional, optional user
# parameters such as "needs symbol" and returns a randomized password for the user. Additionally contains the option
# for the user to click a "give me inspiration" button which invokes a webscraper to get Wikipedia article titles for
# inspiration for users to come up with their own human-friendly passwords.

import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import END
from tkinter import messagebox
import webbrowser
import random
import string
import json
import requests
from bs4 import BeautifulSoup


def link(url):
    """
    Opens links in a web browser
    """
    webbrowser.open_new(url)


def advanced():
    """
    Creates the display for the advanced file menu path
    """
    window = tk.Toplevel(root)
    window.title('Advanced Settings')
    window.geometry('300x150')
    frame = tk.Frame(window)
    frame.pack(side=tk.LEFT)
    text = tk.Message(frame, width=300, justify='left',
                      text='These options will exclude certain characters, reducing the ambiguity of your password:')
    text.grid(row=0)
    tk.Checkbutton(frame, text='Exclude Similar Characters (e.g. o, O, 0, l, I)',
                   variable=similar_var).grid(row=1, sticky=tk.W)
    tk.Checkbutton(frame, text='Exclude Ambiguous Characters (e.g. "`\'{}()[])',
                   variable=ambiguous_var).grid(row=2, sticky=tk.W)
    close = tk.Button(frame, text='Close', command=window.withdraw)
    close.grid(row=3, column=0)


def about():
    """
    Creates the display for the about help menu path
    """
    window = tk.Toplevel(root)
    window.title('About')
    window.geometry('450x300')
    frame = tk.Frame(window)
    frame.pack(side=tk.LEFT)
    display_QA(frame)

    close = tk.Button(frame, text='Close', command=window.withdraw)
    close.pack()


def display_QA(frame):
    """
    Displays the Q and A text to the About menu page.
    """
    text = tk.Message(frame, width=450, justify='left', text='Q - What is this program?\n'
                                  'A - This program is meant to help users create secure passwords that they can use '
                                  'for a variety of sites, entering the parameters that their site requires.\n\n'
                                  'Q - What if I don\'t want to input parameters, or don\'t know what to put?\n'
                                  'A - The program will still generate a password, using default conditions.\n'
                                  'The following are the default conditions should the user provide no parameters of '
                                  'their own: \nPassword length: 12-16 characters\n'
                                  'Options included: Uppercase letters, lowercase letters, and symbols.\n\n'
                                  'Q - What is the inspiration button for?\n'
                                  'A - This button is meant to provide users with inspiration to create their own '
                                  'passwords instead of using the generator to create a random one. Users are advised '
                                  'that such passwords may not be as secure as randomly generated passwords. To learn '
                                  'more, please navigate to help -> learn more for resources on password security.')
    text.pack()


def learn():
    """
    Creates the display for the learn help menu path
    """
    window = tk.Toplevel(root)
    window.title('Learn More')
    window.geometry('300x150')
    frame = tk.Frame(window)
    frame.pack(side=tk.LEFT)
    text = tk.Message(frame, text='To learn more about password security, check out the following resources:',
                      width=300, justify='left')
    text.pack()
    display_links(frame)
    close = tk.Button(frame, text='Close', command=window.withdraw)
    close.pack()


def display_links(frame):
    """
    Displays links in the 'Learn More' window.
    """
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


def generate_password(length):
    """
    Randomly generates a password for the user.
    :param length: integer, the number of random characters to generate for the password
    :return: string, the finished password to be displayed to user
    """
    temp = ''
    required = generate_required()
    for char in required:
        length -= 1
    if length != 0:
        rand = generate_options()
        multi = rand[0] + rand[1] + rand[2] + rand[3]
        temp = ''.join(random.choice(multi) for i in range(length))
    temp = temp + required
    password = ''.join(random.sample(temp, len(temp)))
    return password


def generate_options():
    """
    Creates pool of possible characters that can be selected for password.
    :return: list, contains pools of characters allowable in order: upper, lower, digits, punc
    """
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    punc = string.punctuation
    rand = remove_similar(upper, lower, digits, punc)
    rand[3] = remove_ambiguous(rand[3])
    return rand


def remove_similar(upper, lower, digits, punc):
    """
    Removes similar characters from pool of possible characters if user has selected that advanced feature.
    :param upper: string, all ascii uppercase
    :param lower: string, all ascii lowercase
    :param digits: string, all ascii digits
    :param punc: string, all ascii punctuation
    :return: list
    """
    if similar_var.get() == True:
        upper = upper.replace('O', '')
        upper = upper.replace('I', '')
        lower = lower.replace('l', '')
        lower = lower.replace('o', '')
        digits = digits.replace('0', '')
        punc = punc.replace('|', '')
    return [upper, lower, digits, punc]


def remove_ambiguous(punc):
    """
    Removes ambiguous characters from pool of possible characters if user has selected that advanced feature.
    :param punc: string, all ascii punctuation minus those characters removed by remove_similar
    :return: string
    """
    if ambiguous_var.get() == True:
        punc = punc.replace('{', '')
        punc = punc.replace('{', '')
        punc = punc.replace('(', '')
        punc = punc.replace(')', '')
        punc = punc.replace('[', '')
        punc = punc.replace(']', '')
    return punc


def generate_required():
    """
    Checks for user specified requirements for password.
    :return: string, containing one randomized character from each category requested by user
    """
    upper_temp = lower_temp = number_temp = symbol_temp = ''
    rand = generate_options()
    if require_upper_case.get() == 1:
        upper_temp = ''.join(random.choice(rand[0]))
    if require_lower_case.get() == 1:
        lower_temp = ''.join(random.choice(rand[1]))
    if require_number.get() == 1:
        number_temp = ''.join(random.choice(rand[2]))
    if require_symbol.get() == 1:
        symbol_temp = ''.join(random.choice(rand[3]))
    return upper_temp + lower_temp + number_temp + symbol_temp


def generate_clicked():
    """
    Displays randomly generated password on GUI.
    """
    if min_chars.get() > max_chars.get():
        error('mismatch')
    else:
        length = calc_length(min_chars.get(), max_chars.get())
        password = generate_password(length)
        if length < len(password) and len(password) > int(max_chars.get()):
            error('overflow')
        else:
            old_password = output_var.get()
            past_password_text.set(old_password + '\n')
            past_password_scroll.insert(1.0, past_password_text.get())
            output_var.set(password)


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
    """
    Uses API call to webscraper to provide inspiration to user.
    """
    inspiration = api_call()
    new_text = inspiration
    inspiration_output.configure(text=new_text)
    old_inspiration = inspiration_output_var.get()
    past_inspiration_text.set(old_inspiration + '\n')
    past_inspiration_scroll.insert(1.0, past_inspiration_text.get())
    inspiration_output_var.set(new_text)


def api_call():
    """
    Makes call to webscraper using random Wikipedia article, receiving the article's title.
    :return: string
    """
    article = requests.get('https://en.wikipedia.org/wiki/Special:Random').text
    soup = BeautifulSoup(article, 'html.parser')
    h1 = soup.find('h1', id='firstHeading')
    h1 = h1.string
    data = h1.replace(' ', '_')
    response = requests.get('http://flip2.engr.oregonstate.edu:8797/?u=' + data)
    return response.json()['title'][0]



def reset():
    """
    Resets GUI to default state, creating a fresh session
    """
    require_upper_case.set(0)
    require_lower_case.set(0)
    require_number.set(0)
    require_symbol.set(0)
    min_chars.set('')
    max_chars.set('')
    past_password_scroll.delete('0.0', END)
    output_var.set('')
    inspiration_output_var.set('')
    past_inspiration_scroll.delete('0.0', END)


def error(type):
    """
    Displays an error pop-up window explaining what went wrong
    """
    if type == 'mismatch':
        tk.messagebox.showerror(title='Error', message='Minimum characters is more than Maximum characters.\n'
                                                       'Raise Maximum or lower Minimum to proceed.')
    elif type == 'overflow':
        tk.messagebox.showerror(title='Error', message='There are more requirements than the current length allows.\n'
                                                       'Increase maximum characters or remove some requirements.')


root = tk.Tk()
root.title('Password Generator')
root.geometry('550x325')

# The top menu
menu = tk.Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Clear', command=reset)
filemenu.add_command(label='Advanced', command=advanced)
filemenu.insert_separator(index=4)
filemenu.add_command(label='Exit', command=root.quit)
helpmenu = tk.Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=about)
helpmenu.add_command(label='Learn more', command=learn)

# Frames of root window
frame = tk.Frame(root)
frame.pack(side=tk.TOP)
leftframe = tk.Frame(frame)
leftframe.pack(side=tk.LEFT)
rightframe = tk.Frame(frame)
rightframe.pack(side=tk.RIGHT)
bottomframe = tk.Frame(root)
bottomframe.pack(side=tk.BOTTOM)
bottomleftframe = tk.Frame(bottomframe)
bottomleftframe.pack(side=tk.LEFT)
bottomrightframe = tk.Frame(bottomframe)
bottomrightframe.pack(side=tk.RIGHT)

# Creates password options as check boxes
require_upper_case = tk.IntVar()
require_lower_case = tk.IntVar()
require_number = tk.IntVar()
require_symbol = tk.IntVar()
min_chars = tk.StringVar()
max_chars = tk.StringVar()
similar_var = tk.BooleanVar()
ambiguous_var = tk.BooleanVar()
output_var = tk.StringVar()
tk.Checkbutton(leftframe, text='Include Upper Case Letter (ABCDE)', variable=require_upper_case).grid(row=0, sticky=tk.W)
tk.Checkbutton(leftframe, text='Include Lower Case Letter (abcde)', variable=require_lower_case).grid(row=1, sticky=tk.W)
tk.Checkbutton(leftframe, text='Include Numbers (12345)', variable=require_number).grid(row=2, sticky=tk.W)
tk.Checkbutton(leftframe, text='Include Symbol (!@#$%)', variable=require_symbol).grid(row=3, sticky=tk.W)

# Creates max and min characters needed input boxes
tk.Label(leftframe, text='Minimum Characters').grid(row=4, column=0)
tk.Label(leftframe, text='Maximum Characters').grid(row=5)
min_entry = tk.Entry(leftframe, textvariable=min_chars).grid(row=4, column=1)
max_entry = tk.Entry(leftframe, textvariable=max_chars).grid(row=5, column=1)

# Generate password button
generate = tk.Button(leftframe, text='Generate Password', command=generate_clicked)
generate.grid(row=6, column=0)
generate_text = tk.Message(leftframe, text='Your password is: ', width=200, justify='left')
generate_text.grid(row=7, column=0)
generate_output = tk.Message(leftframe, textvariable=output_var, width=500, justify='left')
generate_output.grid(row=8, column=0)

# Past password tracker
past_password_text = tk.StringVar()
past_password_scroll = scrolledtext.ScrolledText(bottomleftframe, undo=True, width=40, height=6)
past_password_scroll.grid(row=8, column=0, columnspan=2)
past_password_scroll.insert(1.0, past_password_text.get())

# Inspiration button
inspiration_text = tk.Message(rightframe, text='\n\n\nWant inspiration to make your own password? Click the \'give me '
                                               'inspiration\' button below, and get some ideas!\n\n', width=200)
inspiration = tk.Button(rightframe, text='Give me inspiration', command=inspiration_clicked)
inspiration_text.pack()
inspiration.pack()
inspiration_output_var = tk.StringVar()
inspiration_output_text = tk.Message(rightframe, text='Your inspiration is: ', width=200, justify='left')
inspiration_output_text.pack()
inspiration_output = tk.Message(rightframe, textvariable=inspiration_output_var, width=200, justify='left')
inspiration_output.pack()

# Past inspiration tracker
past_inspiration_text = tk.StringVar()
past_inspiration_scroll = scrolledtext.ScrolledText(bottomrightframe, undo=True, width=40, height=6)
past_inspiration_scroll.pack()
past_inspiration_scroll.insert(1.0, past_inspiration_text.get())

root.mainloop()
