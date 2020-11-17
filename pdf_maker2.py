from mdutils.mdutils import MdUtils
from mdutils.tools.Html import Html
from PIL import Image, ImageGrab
import os
import pathlib


def getLang(filename):
    ext = os.path.splitext(filename)[1]
    lang = ext[1:]
    langs = {
        ".py": "python",
        ".js": "javascript"
    }
    for x in langs:
        if ext == x:
            lang = langs[x]
    return lang


def getImage(op):
    try:
        img = ImageGrab.grabclipboard()
        if not os.path.exists('.\outputs'):
            os.mkdir("outputs")
        img.save(op, 'PNG')
    except AttributeError:
        check = input("\nNo image copied.\nTry again.\nType \'y\' when done: ")
        getImage(op)


# Reading inputs
j = 1
code = ""
op = ""
lang = ""

# Change your name and college ID
name = "Amaan Mohib"
usn = "1NT19IS012"

n = int(input("Enter the number of questions: "))
title = input("Enter output file name: ")

# filename= usn(name)_title
fn = "{}({})_{}".format(usn, name.replace(" ", "-"), title)
mdFile = MdUtils(file_name=fn)

mdFile.new_line("Name: {}".format(name), 'b')
mdFile.new_line("USN: {}".format(usn), 'b')
mdFile.new_line("----\n\n---")

for i in range(n):
    ques = input("\nQuestion {}: ".format(i+1))
    filename = input("Enter code file path: ")

    while(j > 0):
        if os.path.isfile(filename):
            lang = getLang(filename)
            codeFile = open(r"{}".format(filename), "r")
            code = codeFile.read()
            codeFile.close()
            j = -1
        else:
            print("\nPlease enter correct path or filename.\n")
            filename = input("Enter correct code file path: ")
            j += 1

    cb = input("Are you using clipboard for output (enter y after snipping)? ")
    if cb == "y" or cb == "Y":
        print("\nSaving image from clipboard.")
        op = ".\outputs\{}-op{}.png".format(title, i+1)
        getImage(op)
    else:
        j = 1
        op = input("\nEnter output image path: ")
        while(j > 0):
            if os.path.isfile(op):
                j = -1
            else:
                print("\nPlease enter correct path or filename.\n")
                op = input("\nEnter correct output image path: ")
                j += 1

    mdFile.new_header(level=2, title="**{}. {}**".format(
        i+1, ques), add_table_of_contents='n')
    mdFile.insert_code(code, lang)
    mdFile.new_line("<br>\n\n")
    mdFile.new_header(level=3, title="**Output:**\n<br>",
                      add_table_of_contents='n')
    imgPath = r'{}'.format(op)
    im = Image.open(imgPath)
    w, h = im.size
    if w > 573:
        w = 573
    im.close()
    mdFile.new_paragraph(Html.image(
        path=imgPath, size="{}".format(w)))
    mdFile.new_line("<div class=\"page\"/>\n\n")

mdFile.create_md_file()
print("\nCreated md file at {}\{}.md".format(pathlib.Path().absolute(), fn))
print("\nOpening VS Code.\n")
os.popen("code {}.md".format(fn))
