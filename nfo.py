import os
import sys
import re
import string
import readline

# list of file extension for which we create a .nfo file
ext = [".mp4", ".mkv"]

# function to ask user for input while specifying an editable default
def rlinput(prompt, prefill=""):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return raw_input(prompt)
    finally:
        readline.set_startup_hook()

# show dir struct must be show/seasons or modules/episodes

# base path for show
if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = sys.argv[2]
    switch = sys.argv[1]
    
# if .nfo file doesn't exist for the show
# create it and write xml data
if not os.path.isfile(path + "tvshow.nfo"):
    showtitle = raw_input("Enter show title:")
    year = raw_input("Enter year:")

    fd = open(path + "tvshow.nfo", "w")
    fd.write("<tvshow>\n")
    fd.write("<title>%s</title>\n"%showtitle)
    fd.write("<showtitle>%s</showtitle>\n"%showtitle)
    fd.write("<year>%s</year>\n"%year)
    fd.write("</tvshow>")
    
for root, dirs, files in os.walk(path): # for each files in every subdirectory
    for file in files: 
        # get filename
        full_path = os.path.join(root, file)
        filename = full_path.split(os.sep)[-1]

        # if file is not a video it
        if filename[-4:] not in ext:
            continue

        season_name = full_path.split(os.sep)[-2]
        show_name = full_path.split(os.sep)[-3]

        season = re.search(r"\d+", season_name).group()
        episode = re.search(r"\d+", filename).group()
        title = re.search(r"[a-zA-Z].*", filename).group()[:-4]

        # replace extension with nfo
        nfo_name = string.replace(full_path, filename[-4:], ".nfo")

        # if .nfo file doesn't exist for episode
        # create it and write xml data
        if not os.path.isfile(nfo_name):
            title = rlinput("Choose episode title:", title)

            fd = open(nfo_name, "w")
            fd.write("<episodedetails>\n")
            fd.write("<title>%s</title>\n"%title)
            fd.write("<season>%s</season>\n"%season)
            fd.write("<episode>%s</episode>\n"%episode)
            fd.write("</episodedetails>")
            fd.close()
