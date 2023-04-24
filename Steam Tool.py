import requests, os, string, winsound
from bs4 import BeautifulSoup
from itertools import islice, product

# --- SETTINGS | 0 = false | 1 = true (ON BOOLS) ---

# BOOLS
dumptags = 1             # dumps tags into a text file.
debug = 1                # debug mode (just shows more stuff in printing, makes program slightly slower).
skipPrivateGroups = 1    # skips private groups in tag finder, Only displays public groups. THIS ONLY APPLIES TO FILE WRITING WITH DUMPTAGS ENABELD.
# END OF BOOLS

startingpos = "meow"         # where the program will start, like it wont start at A values etc i think :3
filename = "retard"        # file name for tag dump output (KEEP .txt at the end).
MIN_STRING_LENGTH = 2    # minimum character length it will search from (there is no groups with 1 character names so keep it > 2).
duration = 300           # duration of the alert when the program has found the correct tag (milliseconds). 
freq = 600               # Hertz frequency of the alert when the program has found correct tag.
PROGRAM_NAME = "Steam Group Checker" # self explanatory, the program name.

# WARNING --- CHANGING ANYTHING BELOW THIS LINE MIGHT/WILL BREAK THE PROGRAM! --- WARNING

count = 1
tagcount = 1
something = 1
fail = 0
versin = 1.0
updar = 0

def generate_combinations():
    characters = string.ascii_lowercase + string.digits
    for length in range(MIN_STRING_LENGTH, 7):
        for combination in product(characters, repeat=length):
            yield ''.join(combination)

def generate_combinationsCusStart(start_position=''):
    characters = string.ascii_lowercase + string.digits
    length = len(start_position)
    for i in range(length, 7):
        for combination in islice(product(characters, repeat=i), pow(len(characters), length)):
            if ''.join(combination)[:length] < start_position:
                continue
            else:
                yield ''.join(combination)

def checkgroup(url):
    taggercount = 1
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"
    }

    resp = requests.get(url, headers=headers).text
    Group = BeautifulSoup(resp, 'html.parser')

    mydivsgr = Group.find_all("span", {"class": "grouppage_header_abbrev"})
    mydivspriv = Group.find_all("div", {"class": "grouppage_join_area"})


    gr1 = str(mydivsgr).replace(f'[<span class="grouppage_header_abbrev"', '')
    gr2 = str(gr1)[gr1.find('>'):]
    gr3 = str(gr2).replace(f'>', '', 1)
    gr4 = gr3.split('</span>', 1)[0]
    search = gr4.lower()

    priv1 = str(mydivspriv).replace(f'[<div class="grouppage_join_area">\n<a class="btn_green_white_innerfade btn_medium"', '')
    priv2 = str(priv1).replace(f'href="javascript:document.forms[\'join_group_form\'].submit();">\n<span>', '')
    priv3 = priv2.split('</span>', 1)[0]

    if priv3 ==" Request To Join":
        something = 1
        priv3 = f"\033[1;31;40mPrivate\033[0;37;40m"
    else:
        something = 0
        priv3 = f"\033[0;32;40mPublic\033[0;37;40m"

    header = Group.title

    hd1 = str(header).replace(f'<title>Steam Community :: Group :: ', '')
    hd2 = str(hd1).replace(f'</title>', '')

    if gr4 == "" or gr4 == "]":
        taggercount = taggercount + 1
    else:
        if dumptags == 1:
            try:
                if skipPrivateGroups == 1:
                    if something == 0:
                        with open(f"{filename}.txt", "a") as f:
                            f.write(f"URL: {url}   | PRIVACY: Public   | TAG: {gr4} \n")
                else:
                    if something == 0:
                        with open(f"{filename}.txt", "a") as f:
                           f.write(f"URL: {url}   | PRIVACY: Public    | TAG: {gr4} \n")
                    else:
                        with open(f"{filename}.txt", "a") as f:
                            f.write(f"URL: {url}   | PRIVACY: Private   | TAG: {gr4} \n")
            except Exception:
                taggercount = taggercount + 1

    if tag == search:
        os.system("cls")
        winsound.Beep(freq, duration)
        print(f"Steam Tag Finder v1.0")
        print(f"Tag Searched For: {tag}\n\n")
        print(f"Group Name: {combination}")
        print(f"Group Header: {hd2}")
        print(f"Group URL: {url}")
        print(f"Group Tag: {gr4} (MATCHES)")
        print(f"Group Privacy: {priv3}\n")
        os.system("pause")
    else:
        if debug == 1:
            if gr4 == "]" or gr4 == "":
                taggercount = taggercount + 1
            else:
                if something == 0:
                   print(f"{url}  | {priv3}   | {gr4} = NOT A MATCH")
                if something == 1:
                   print(f"{url}  | {priv3}  | {gr4} = NOT A MATCH")

while count:
    os.system("cls")

    print(f"Steam Checker Tool v1.0\nfrax#0333 - discord | Contact for issues :)")
    print(f"\nMethods:")
    print(f"1) by Name")
    print(f"2) by Tag (UNTESTED)")
    print(f"\n")

    selection = input("> ")
    try:
        selection = int(selection)
    except Exception:
        selection = str(selection)

    os.system("cls")
    if selection == 1 or selection =="name":
        print("Steam Group Checker Tool v1.0")
        print(f"Method: by Name\n")

        name = input("Enter Group Name to Check: ")

        url = f"https://steamcommunity.com/groups/{name}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"
        }

        resp = requests.get(url, headers=headers).text
        Group = BeautifulSoup(resp, 'html.parser')

        mydivsgr = Group.find_all("span", {"class": "grouppage_header_abbrev"})
        mydivspriv = Group.find_all("div", {"class": "grouppage_join_area"})


        gr1 = str(mydivsgr).replace(f'[<span class="grouppage_header_abbrev"', '')
        gr2 = str(gr1)[gr1.find('>'):]
        gr3 = str(gr2).replace(f'>', '', 1)
        gr4 = gr3.split('</span>', 1)[0]
        
        priv1 = str(mydivspriv).replace(f'[<div class="grouppage_join_area">\n<a class="btn_green_white_innerfade btn_medium"', '')
        priv2 = str(priv1).replace(f'href="javascript:document.forms[\'join_group_form\'].submit();">\n<span>', '')
        priv3 = priv2.split('</span>', 1)[0]

        if priv3 ==" Request To Join":
            priv3 = f"\033[1;31;40mPrivate\033[0;37;40m"
        else:
            priv3 = f"\033[0;32;40mPublic\033[0;37;40m"

        header = Group.title

        hd1 = str(header).replace(f'<title>Steam Community :: Group :: ', '')
        hd2 = str(hd1).replace(f'</title>', '')

        if hd2 =="<title>Steam Community :: Error":
            os.system("cls")
            print("Group Information Checker v1.0\n")
            print("Group either doesn't exist, is Banned, or there was an error (i dont know)\n")
            os.system("pause")
        else:
            os.system("cls")
            print("Group Information Checker v1.0\n")
            print(f"Group Name: {name}")
            print(f"Group Header(?): {hd2}")
            print(f"Group URL: {url}")
            print(f"Group Tag: {gr4}")
            print(f"Group Privacy: {priv3}\n")
            os.system("pause")

    if selection == 2 or selection =="TAG":
        os.system("cls")
        print(f"Steam Tag Finder v1.0\n\n")

        tag = input("Enter Tag You Would Like to Look for: ")
        tag = tag.lower()

            
        while tagcount:
            os.system("cls")
            print(f"Steam Tag Finder\n\n")
            print(f"Searching for tag: \"{tag}\"...")

            #for combination in generate_combinations():
            #    url = f"https://steamcommunity.com/groups/{combination}"

            if startingpos == "off":
                for combination in generate_combinations():
                    url = f"https://steamcommunity.com/groups/{combination}"
                    checkgroup(url)
            else:
                for combination in generate_combinationsCusStart(start_position=startingpos):
                    url = f"https://steamcommunity.com/groups/{combination}"
                    checkgroup(url)
    else:
        count = count + 1
count = count + 1
