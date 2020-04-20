# partcheck.py
# Creator: SSpyR
# Main Contributor: Prismatic
# Thanks to A Bird for Creating the Initial File System Collection

# Actually make a GUI
# Make it pretty and simple
# Had to adjust how the methods search for files do to how the exe unpacks it, may fix at some point (results in searching a lot more files than needed)
# Make input take spaces cause apparently it doesnt (maybe not?)

# Balance Alias: Balance, InvBalD
# PartSet Alias: PartSet, Partset, InvPartSet, InvPart, BPInvPartSet

# current version = 0.9.5

from cmd import Cmd
import json
import os
import assets

import xlrd as xls

class EditorHelper(Cmd):
    prompt='bl3edit> '
    intro='Welcome to the BL3 Item Editor Helper! Use the help command to get started.'

    # exit method
    def do_exit(self, inp):
        print('Exiting..')
        return True

    # naming method
    def do_naming(self, inp):
        filename='FilesNaming.txt'
        with open((filename), 'r') as foo:
            for line in foo:
                print(line)

    # help naming method
    def help_naming(self):
        print('Gives a list of items that have different names in the files compared to in-game, \nuse this as a resource to better find what you are looking for')

    # bal method
    def do_bal(self, inp):
        inp=inp.replace(' ', '_')
        if inp == '':
            print('Please enter a name after the command.')
        else:
            response, target = getFile(inp, "Balance", "Balance", "InvB")
            print(sortDuplicates(getParts(response, target)))

    # help bal method
    def help_bal(self):
        print('Use this to search for Balance files. \nSimply do bal and then the name of the item you want to get the file for. \nMake sure to reference with the naming command and use the full name of the item (should be one word most of the time)')

    # part method
    def do_part(self, inp):
        file, target = getPartFile(inp)
        if file!=0:
            print(sortDuplicates(getParts(file, target)))

    # help part method
    def help_part(self):
        print('Use this to search for PartSet files. \nSimply do bal and then the name of the item you want to get the file for. \nMake sure to reference with the naming command and use the full name of the item (should be one word most of the time)')

    # Retrieves anoints relevant to character
    def do_anoints(self, inp):
        inparr=inp.split(" ")
        file, target = getPartFile(inparr[0])
        if "Weapons" not in target: file, target = getFile(inparr[0], "Balance", "Balance", "InvB")
        if file!=0:
            print(getAnoints(file, target, inparr[1]))
    
    # help anoints method
    def help_anoints(self):
        print("Use this if you just want a list of anoints relevant to your character \n Do anoints then the item your're interested in followed by one of Amara, Fl4k, Moze or Zane.")

    # List
    def do_list(self,inp):
        for root, dirs, files in os.walk(os.getcwd()):
            for dir in dirs:
                if dir.lower().startswith(inp.lower()):
                    if "Balance" in os.path.join(root, dir): 
                        for gun_types in os.walk(os.path.join(root, dir)):
                            print(gun_types[0].split("/")[-1],end="\n\n")
                            for gun in gun_types[2]:
                                gunArr = gun.split("_")
                                gunArr[-1]=gunArr[-1][0:len(gunArr[-1])-5]
                                for i in range(1,len(gunArr)):
                                    print(gunArr[i],end=" ")
                                print("")
                            print("")

    # help list method
    def help_list(self):
        print("Lists all itmes by the specified manufacturer. \n EG list Maliwan")

    # provides part info
    def do_partinfo(self, inp):
        file, target = getPartFile(inp)
        toReturn = ""
        if "Weapons" in target and file!=0:
            partsSTR = getParts(file, target)
            parts = partsSTR.split("\n")
            part_info_book = xls.open_workbook("part_info.xlsx") 

            sheet = parts[3].upper().split(" ")[0][5:11]
            try: gunTypeInfo = part_info_book.sheet_by_name(sheet)
            except:
                sheetArr = sheet.split("_")
                sheet = sheetArr[1]+"_"+sheetArr[0]
                gunTypeInfo = part_info_book.sheet_by_name(sheet)
            
            length = gunTypeInfo.nrows
            for i in range(3, len(parts)-3):
                if parts[i][0:4]!="Part": break
                for n in range(1, length):
                    if parts[i].split(" ")[0] in gunTypeInfo.cell_value(n, 0):
                        toReturn = toReturn + "\n"+parts[i]
                        if gunTypeInfo.cell_value(n, 4)!="": toReturn = toReturn + "\n"+"    " + gunTypeInfo.cell_value(n, 4)
                        if gunTypeInfo.cell_value(n, 3)!="": toReturn = toReturn + "\n"+"    " + gunTypeInfo.cell_value(n, 3)
                        if gunTypeInfo.cell_value(n, 1)!="": toReturn = toReturn + "\n"+"    " + gunTypeInfo.cell_value(n, 1)
                        if gunTypeInfo.cell_value(n, 2)!="": toReturn = toReturn + "\n"+"    " + gunTypeInfo.cell_value(n, 2)
                        toReturn = toReturn + "\n"
                        break
            print(addDependencyInfo(toReturn))
        else: print("Sorry Part info can only be displaeyd for weapons currently, try 'shield' or 'art' as a command")

    # help partinfo method
    def help_partinfo(self):
        print("Lists all parts and their effects on the weapon, please be aware this database was built by players and is liable to have mistakes or be outdated. Use with discretion.")

    # # Lists artifact stats
    # def do_artifacts(self):
    #     part_info_book = xls.open_workbook("part_info.xlsx") 
    #     artifact = part_info_book.sheet_by_name("Artifact")
    #     length = artifact.nrows
    #     i = 59
    #     while i<length and artifact.cell_value(i, 0)!="":
    #         print(artifact.cell_value(i, 0).split(".")[0] + "\n" + artifact.cell_value(i, 1), end="\n\n")
    #         i += 1
        
    #     i=51
    #     print("\n -------------------------------------------- \nThese stats replace section A on artifacts by the same name")
    #     while artifact.cell_value(i, 0)!="":
    #         print(artifact.cell_value(i, 0).split(".")[0] + "\n    " + artifact.cell_value(i, 1), end="\n\n")
    #         i += 1

    # # help shield method
    # def help_artifacts(self):
    #     print("Lists artifact parts, their effects and the stat rolls that are possible.")

    # # lists shield parts
    # def do_shield(self):
    #     part_info_book = xls.open_workbook("part_info.xlsx") 
    #     shield = part_info_book.sheet_by_name("Shield")
            
    #     length = shield.nrows
    #     i = 23
    #     while i<length and shield.cell_value(i, 0)!="":
    #         print(shield.cell_value(i, 0).split(".")[0] + "\n" + shield.cell_value(i, 1), end="\n\n")
    #         i += 1
    #     print("\n---------------------------------------------------------------------------------------- \n")
            
    #     i=65
    #     print()
    #     while i<length and shield.cell_value(i, 0)!="":
    #         print(shield.cell_value(i, 0).split(".")[0] + "\n    " + shield.cell_value(i, 1), end="\n\n")
    #         i += 1
   
    # # help shield method
    # def help_shield(self):
    #     print("Lists Shield parts and their effects")

    # prints the partset in full
    def do_partSet(self, inp):
        response, target = getPartFile(inp)
        print(response)

    def help_partSet(self):
        print("prints the partset in full")
    
    # prints the balance in full
    def do_balance(self, inp):
        response, target = getFile(inp, "Balance", "Balance", "InvB")
        print(response)

    def help_balance(self):
        print("prints the balance in full")

# Extracts select information from Partset files.
def getParts(FileContentsAsString, target):
    itemParts, anoints = "", ""
    if "Weapons" in target or "[Shields]" in target or "[Grenades]" in target: 
        content = FileContentsAsString.split("\n")
        offset, hasAnoints = 1, False
        for i in range(0, len(content)):
            if ("PartData" in content[i]):
                if ("GPart_" in content[i+offset]): 
                    anoints = anoints + "\n" + content[i+offset].strip().strip(",").strip("\"")
                    hasAnoints = True
                else: itemParts = addPartToList(content, i+offset, itemParts)
        itemParts = "\nParts: \n" + itemParts + "\n"
        if hasAnoints: itemParts = itemParts +"\nAnointments:\n"+anoints+"\n"
        return itemParts
    return FileContentsAsString

# Returns Anoints relevant to the specified character
def getAnoints(FileContentsAsString, target, character):
    if "Weapons" in target: 
        anoints = ""
        content = FileContentsAsString.split("\n")
        character = character.lower()
        for i in range(0, len(content)):
            if ("GPart_" in content[i]):
                part = content[i].split("/")
                if len(part)>6:
                    if part[-1][6:9] == "All": anoints = anoints + "\n" + part[-1][6:len(part[-1])-1]
                    else:
                        if character=="amara":
                            if part[-1][6] == "S": anoints = anoints + "\n" + part[-1][12:len(part[-1])-1]
                        elif character=="fl4k" or character=="flak":
                            if part[-1][6] == "B": anoints = anoints + "\n" + part[-1][12:len(part[-1])-1]
                        elif character=="moze":
                            if part[-1][6] == "G": anoints = anoints + "\n" + part[-1][13:len(part[-1])-1]
                        elif character=="zane":
                            if part[-1][6] == "O" or part[-1][6] == "C":
                                anoints = anoints + "\n" + part[-1][16:len(part[-1])-1]
            elif ("/Gear/Weapons/" in content[i] and "Att_EndGame" not in content[i]): break
        return anoints+"\n"
    return FileContentsAsString

# Fetches the partset file and reads it into a string.
def getPartFile(inp):
    inp=inp.replace(' ', '_')
    if inp == '':
        print('Please enter a name after the command.')
        return 0, 0
    else:
        response, target = getFile(inp, "PartSet", "Part", "InvPart", "BPInvPart")
        return response, target

def getFile(file, searchType, match1, match2, match3="ZZZ"):
    data=None
    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            if name.startswith(match1) or name.startswith(match2) or name.startswith(match3):
                if file.lower() in name.lower():
                    target=os.path.join(root, name)
                    with open(target, 'r') as fp:
                        data=json.load(fp)
                        response=json.dumps(data, indent=4)
                        print("\nReading from: "+ target.split("/")[-1])
                        return response, target
    if data==None:
            print('No ' + searchType + ' File for said Item Could be Found.')
            return 0, 0

def addPartToList(content, i, itemParts):
    if "export" in content[i]: return itemParts
    itemParts = itemParts + "\n" + content[i].strip().strip(",").strip("\"")             
    if ("Min" in content[i-7]):
        itemParts = itemParts + " - " + content[i-7].strip() + " " + content[i-6].strip()
    return itemParts

def sortDuplicates(stringInput):
    stringArr = stringInput.split("\n")
    toReturn = stringArr[0]
    line = 1
    while line < len(stringArr)-2:
        if len(stringArr[line])<3: toReturn = toReturn + "\n"
        else:
            if stringArr[line+1] in stringArr[line] and len(stringArr[line+1])>3:
                if stringArr[line+2] in stringArr[line]:
                    toReturn = toReturn + "\n    3x " + stringArr[line]
                    line=line+1
                else: toReturn = toReturn + "\n    2x " + stringArr[line]
                line=line+1
            else: toReturn = toReturn + "\n    " + stringArr[line]
        line=line+1
    return toReturn

def addDependencyInfo(PartInfoStr):
    parts = PartInfoStr.split("\n")
    excluder_book = xls.open_workbook("dependencies.xlsx") 
    gunPartInfo = excluder_book.sheet_by_name("Weapons")

    length = gunPartInfo.nrows
    for i in range(3, len(parts)-1):
        if parts[i][0:4] =="Part":
            for n in range(1, length):
                if parts[i].split(" ")[0] in gunPartInfo.cell_value(n, 8):
                    p=i
                    for m in range(i, i+5):
                        if len(parts[m])<2: 
                            p=m
                            break
                    try: 
                        if gunPartInfo.cell_value(n, 7)!=1:parts[p]=parts[p] + "    Weight: " + str(gunPartInfo.cell_value(n, 7 )) + "\n"
                    except: pass
                    try: 
                        if gunPartInfo.cell_value(n, 9)!="": parts[p]=parts[p] + "    Requires: " + gunPartInfo.cell_value(n, 9) + "\n"
                    except: pass
                    try: 
                        if gunPartInfo.cell_value(n, 10)!="": parts[p]=parts[p] + "    Excludes: " + gunPartInfo.cell_value(n, 10) + "\n"
                    except: pass
                    break
    
    toReturn = ""
    for line in parts:
        toReturn = toReturn + "\n"+line
    return toReturn

if __name__ == '__main__':
    EditorHelper().cmdloop()