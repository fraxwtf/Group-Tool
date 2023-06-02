try:
    import os, string, winsound, sys
    import requests
    from bs4 import BeautifulSoup
    from itertools import islice, product
except Exception:
    sys.exit(f"Please run 'pip install reuqiremts.txt' inside command prompt, in the working directory, to use this tool...")

# --- SETTINGS | 0 = false | 1 = true (ON BOOLS) ---

# BOOLS
dumptags = 1             # dumps tags into a text file.
debug = 1                # debug mode (just shows more stuff in printing, makes program slightly slower).
skipPrivateGroups = 1    # skips private groups in tag finder, Only displays public groups. THIS ONLY APPLIES TO FILE WRITING WITH DUMPTAGS ENABELD.
# END OF BOOLS

DATE_FOUNDED = "0"      # finds groups from a specific year, debug mode required.
filename = "big"        # file name for tag dump output
MIN_STRING_LENGTH = 2    # minimum character length it will search from (there is no groups with 1 character names so keep it > 2).
duration = 300           # duration of the alert when the program has found the correct tag (milliseconds). 
freq = 600               # Hertz frequency of the alert when the program has found correct tag.
PROGRAM_NAME = "Steam Group Checker" # self explanatory, the program name.

# WARNING --- CHANGING ANYTHING BELOW THIS LINE MIGHT/WILL BREAK THE PROGRAM! --- WARNING

count = 1
tagcount = 1
startingpos = ""
dumptagsNEW = "n"
versin = "1.5" #dont change this to bypass the update thing (or do idc but things might have new features in future versions idk why u would wanna miss out on them:3
nourlcount = 0

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

def checkgroup(url, nourlcount):
    taggercount = 1
    something = 3
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"
    }

    resp = requests.get(url, headers=headers).text
    Group = BeautifulSoup(resp, 'html.parser')

    mydivsgr = Group.find_all("span", {"class": "grouppage_header_abbrev"})
    mydivspriv = Group.find_all("div", {"class": "grouppage_join_area"})
    mydivsfounded = Group.find_all("div", {"class": "data"})
    mydivsbanned = Group.find_all("div", {"id": "message"})

    mydivsbanned = str(mydivsbanned).replace(f'<div id=\"message\"', '')
    mydivsbanned = str(mydivsbanned).replace(f'<h1>', '')
    mydivsbanned = str(mydivsbanned).replace(f'</h1>', '')
    mydivsbanned = str(mydivsbanned).replace(f'<h3>', '')
    mydivsbanned = str(mydivsbanned).replace(f'\n', '')
    mydivsbanned = str(mydivsbanned).replace(f'[>Sorry!<p class=\"sectionText\"', '')
    mydivsbanned = str(mydivsbanned).replace('  ', '')
    mydivsbanned = str(mydivsbanned).replace('d ', 'd')
    mydivsbanned = mydivsbanned.split(f'for', 1)[0]
    before, sep, after = mydivsbanned.partition('</p>')
    mydivsbanned2 = after
    if mydivsbanned2 == "This group has been removed" and DATE_FOUNDED == "0":
        mydivsbanned2 = f"This group has been \033[1;31;40mremoved\033[0;37;40m."
        print(f'{url}  | {mydivsbanned2}' )

    gr1 = str(mydivsgr).replace(f'[<span class="grouppage_header_abbrev"', '')
    gr2 = str(gr1)[gr1.find('>'):]
    gr3 = str(gr2).replace(f'>', '', 1)
    gr4 = gr3.split('</span>', 1)[0]
    search = gr4.lower()

    priv1 = str(mydivspriv).replace(f'[<div class="grouppage_join_area">\n<a class="btn_green_white_innerfade btn_medium"', '')
    priv2 = str(priv1).replace(f'href="javascript:document.forms[\'join_group_form\'].submit();">\n<span>', '')
    priv3 = priv2.split('</span>', 1)[0]

    founded = str(mydivsfounded).replace(f'[<div class="data">', '')
    founded = founded.split('</div>', 1)[0]
    before, sep, after = founded.partition(', ')
    founded2 = after
    #foundeddiff = str(foundeddiff)
    #foundeddiff = int(foundeddiff)

    if priv3 ==" Request To Join":
        something = 1
        priv3 = f"\033[1;31;40mPrivate\033[0;37;40m"
    if priv3 == " Join Group":
        something = 0
        priv3 = f"\033[0;32;40mPublic\033[0;37;40m"
    if mydivsbanned2 =="This group has been removed":
        something = 2
        priv3 = f"\033[1;31;40mBanned\033[0;37;40m"

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
                        with open(f"{filename} - PUBLIC.txt", "a") as f:
                           f.write(f"URL: {url}   | PRIVACY: Public    | TAG: {gr4} \n")
                    if something == 1:
                        with open(f"{filename} - PRIVATE.txt", "a") as f:
                            f.write(f"URL: {url}   | PRIVACY: Private   | TAG: {gr4} \n")
            except Exception:
                taggercount = taggercount + 1

    if DATE_FOUNDED != "0":
        if DATE_FOUNDED  == founded2:
            if something == 0:
                print(f"{url}  | {priv3}   | {gr4} = NOT A MATCH | Date Founded: {founded2}")
            if something == 1:
                print(f"{url}  | {priv3}  | {gr4} = NOT A MATCH | Date Founded: {founded2}")
    else:
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
                if something == 0:
                    print(f"{url}  | {priv3}   | {gr4} = NOT A MATCH | Date Founded: {founded}")
                if something == 1:
                    print(f"{url}  | {priv3}  | {gr4} = NOT A MATCH | Date Founded: {founded}")
                if mydivsbanned == "test":
                    print(f"{url}  | {priv3}")

while count:

    vurl = f"https://github.com/fraxwtf/Steam-Group-Checker-Tag-Generator/releases"
    vheaders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"
    }

    vresp = requests.get(vurl, headers=vheaders).text
    VersionPage = BeautifulSoup(vresp, 'html.parser')
    
    Version = VersionPage.find_all("div", {"class": "markdown-body my-3"})
    V1 = str(Version).split('</p>', 1)[0]
    point_to_keep = "Version"
    index = V1.find(point_to_keep)
    NewVersion = V1[index:]
    New_Version = NewVersion.replace('Version ', '')
    os.system("cls")

    if versin != New_Version:
        #print(Version)
        print("Warning! Outdated Version!")
        print(f"The Version you have is NOT up to date! (\033[1;31;40m{versin}\033[0;37;40m) Get the Latest Version (\033[0;32;40m{New_Version}\033[0;37;40m) From my Github page!")
        print(f"\nhttps://github.com/fraxwtf/Steam-Group-Checker-Tag-Generator/releases")
        print(f"\nContact:\n - discord: \033[1;35;40mhttps://discord.gg/NCdHqhA6ht\033[0;37;40m\n - Twitter: @fraxiscool")
    else:
        print(f"Steam Checker Tool\n\033[1;34;40mhttps://discord.gg/NCdHqhA6ht\033[0;37;40m - discord | Contact for issues :)")
        print(f"Version: {versin} \033[0;32;40mUp to Date!\033[0;37;40m")
        print(f"\nMethods:")#		Others:")
        print(f" 1) Group by Name")#	Settings")
        print(f" 2) Group by Tag")
        print(f" 3) Dump All Tags")
        print(f"\n")

        selection = input("> ")
        selection.lower()
        try:
            selection = int(selection)
        except Exception:
            selection = str(selection)

        os.system("cls")
        if selection == 1 or selection =="name":
            print("Steam Group Checker Tool {versin}")
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
            mydivsfounded = Group.find_all("div", {"class": "data"})


            gr1 = str(mydivsgr).replace(f'[<span class="grouppage_header_abbrev"', '')
            gr2 = str(gr1)[gr1.find('>'):]
            gr3 = str(gr2).replace(f'>', '', 1)
            gr4 = gr3.split('</span>', 1)[0]
          
            priv1 = str(mydivspriv).replace(f'[<div class="grouppage_join_area">\n<a class="btn_green_white_innerfade btn_medium"', '')
            priv2 = str(priv1).replace(f'href="javascript:document.forms[\'join_group_form\'].submit();">\n<span>', '')
            priv3 = priv2.split('</span>', 1)[0]

            founded = str(mydivsfounded).replace(f'[<div class="data">', '')
            founded = founded.split('</div>', 1)[0]
 
            if priv3 ==" Request To Join":
                priv3 = f"\033[1;31;40mPrivate\033[0;37;40m"
            else:
                priv3 = f"\033[0;32;40mPublic\033[0;37;40m"

            header = Group.title

            hd1 = str(header).replace(f'<title>Steam Community :: Group :: ', '')
            hd2 = str(hd1).replace(f'</title>', '')

            if hd2 =="<title>Steam Community :: Error":
                os.system("cls")
                print("Group Information Checker {versin}\n")
                print("Group either doesn't exist, is Banned, or there was an error (i dont know)\n")
                os.system("pause")
            else:
                os.system("cls")
                print("Group Information Checker {versin}\n")
                print(f"Group Name: {name}")
                print(f"Group Header(?): {hd2}")
                print(f"Group URL: {url}")
                print(f"Group Tag: {gr4}")
                print(f"Group Privacy: {priv3}")
                print(f"Group Founded: {founded}")
                os.system("pause")

        if selection == 2 or selection =="tag":
            os.system("cls")
            print(f"Steam Tag Finder {versin}\n\n")

            
            tag = input("Enter Tag You Would Like to Look for: ")
            startingpos = input(f"Enter Position to start from (leave blank if you want to start from minimum character length!): ")
            tag = tag.lower()

            
            while tagcount:
                os.system("cls")
                print(f"Steam Tag Finder {versin}\n\n")
                print(f"Searching for tag: \"{tag}\"...")

            #for combination in generate_combinations():
            #    url = f"https://steamcommunity.com/groups/{combination}"

                if startingpos == "":
                    for combination in generate_combinations():
                        url = f"https://steamcommunity.com/groups/{combination}"
                        checkgroup(url)
                else:
                    for combination in generate_combinationsCusStart(start_position=startingpos):
                        url = f"https://steamcommunity.com/groups/{combination}"
                        checkgroup(url)

        if selection == 3 or selection =="dump":
            os.system("cls")
            print(f"Steam Tag Dumper {versin}\n\n")

            startingpos = input(f"Enter Position to start from (leave blank if you want to start from minimum character length!): ")

            
            while tagcount:
                os.system("cls")
                print(f"Steam Tag Dumper {versin}\n\n")


                if startingpos == "":
                    for combination in generate_combinations():
                        tag = "THISISPLACEHOLDERSOITDOESNTFINDTHETAGLMAO"
                        url = f"https://steamcommunity.com/groups/{combination}"
                        checkgroup(url, nourlcount)
                else:
                    print(f"if your start position thing was long, it may take a minute to get to it :)\n")
                    for combination in generate_combinationsCusStart(start_position=startingpos):
                        tag = "THISISPLACEHOLDERSOITDOESNTFINDTHETAGLMAO"
                        url = f"https://steamcommunity.com/groups/{combination}"
                        checkgroup(url, nourlcount)

        #if selection == "settings" or selection =="setting":
        #    os.system("cls")
         #   settingcount = 1

            

         #   while settingcount:
         #       os.system("cls")
          #      print(f"Steam Tool Settings\n\n")
          #      print(f"Settings:\n - Dump Tags (dt)")

          #     selection = input ("> ")
           #     selection.lower()

           #     if selection == "dump tag" or selection == "dt":
           #         if dumptagsNEW == "n":
           #             print(f"do you want to turn dump tags on? - y/n")
           #             selection = input ("> ")
             #           if selection == "y":
             #               dumptagsNEW = "y"
             #               count = count + 1
             #           else:
             #               count = count + 1
            #        if dumptagsNEW == "y":
            #            print(f"do you want to turn dump tags off? - y/n")
             #           selection = input ("> ")
             #           if selection == "n":
             #               dumptagsNEW = "n"
             #               count += 1
             #           else:
             #               count = settingcount + 1
             #   else:
             #       count = count + 1
        
   
            
        else:
            count = count + 1
count = count + 1
