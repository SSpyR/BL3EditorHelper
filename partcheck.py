# partcheck.py
# Creator: SSpyR
# Thanks to Prismatic for Creating the Data Cleaning Functions
# Thanks to A Bird for Creating the Initial File System Collection

# Actually make a GUI
# Make it pretty and simple
# Had to adjust how the methods search for files do to how the exe unpacks it, may fix at some point (results in searching a lot more files than needed)
# Make input take spaces cause apparently it doesnt (maybe not?)

# Balance Alias: Balance, InvBalD
# PartSet Alias: PartSet, Partset, InvPartSet, InvPart, BPInvPartSet

# current version = 0.6.5

from cmd import Cmd
import json
import os
import assets

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
        data=None
        if inp == '':
            print('Please enter a name after the command.')
        else:
            for root, dirs, files in os.walk(os.getcwd()):
                for name in files:
                    if name.startswith('Balance') or name.startswith('InvB'):
                        if inp.lower() in name.lower():
                            target=os.path.join(root, name)
                            with open(target, 'r') as fp:
                                data=json.load(fp)
                                response=json.dumps(data, indent=4)
                                print("\nReading from: "+ target.split("/")[-1])
                                print(getBal(response, target))
            if data==None:
                print('No Balance File for said Item Could be Found.')

    # help bal method
    def help_bal(self):
        print('Use this to search for Balance files. \nSimply do bal and then the name of the item you want to get the file for. \nMake sure to reference with the naming command and use the full name of the item (should be one word most of the time)')

    # part method
    def do_part(self, inp):
        file, target = getPartFile(inp)
        if file!=0:
            print("Reading from: "+target.split("/")[-1])
            print(getParts(file, target))

    # help part method
    def help_part(self):
        print('Use this to search for PartSet files. \nSimply do bal and then the name of the item you want to get the file for. \nMake sure to reference with the naming command and use the full name of the item (should be one word most of the time)')

    # Retrieves anoints relevant to character
    def do_anoints(self, inp, character):
        file, target = getPartFile(inp)
        if file!=0:
            print("Reading from: "+target.split("/")[-1])
            print(getAnoints(file, target, character))
    
    # help anoints method
    def help_anoints(self):
        print("Use this if you just want a list of anoints relevant to your character \n Do anoints then the item your're interested in followed by one of Amara, Fl4k, Moze or Zane.")

# Extracts select information from Partset files.
def getParts(FileContentsAsString, target):
    itemParts, anoints = "", ""
    if "Weapons" in target: 
        content = FileContentsAsString.split("\n")
        
        for i in range(0, len(content)):
            if ("GPart_" in content[i]):
                part = content[i].split("/")
                if len(part)>6:
                    anoints = anoints + "\n" + part[-1][6:len(part[-1])-1]
            elif ("/Gear/Weapons/" in content[i] or "/Elemental/" in content[i]):
                if ("EPartList" not in content[i] and "/EndGameParts/" not in content[i]):
                    part = content[i].split("/")
                    itemParts = itemParts + "\n" + part[-1][:len(part[-1])-1]
                    for n in range(10,0,-1):
                        if ("Min" in content[i-n]):
                            itemParts = itemParts + " - " + content[i-n].strip() + " " + content[i-n+1].strip()
                            break
        return "\nParts: \n" + itemParts +"\n\nAnointments:\n"+anoints+"\n"
                
    elif "[Shields]" in target: return compilePartString("Game/Gear/Shields/_Design/", FileContentsAsString)
    elif "[Grenades]" in target: return compilePartString("Game/Gear/GrenadeMods/_Design/", FileContentsAsString)
    return FileContentsAsString

# Extracts select information from balance files.
def getBal(FileContentsAsString, target):
    if "Weapons" in target: 
        itemParts, anoints = "", ""
        content = FileContentsAsString.split("\n")
        
        for i in range(0, len(content)):
            if ("GPart_" in content[i]):
                part = content[i].split("/")
                if len(part)>6:
                    anoints = anoints + "\n" + part[-1][6:len(part[-1])-1]
            elif ("/Gear/Weapons/" in content[i] or "/Elemental/" in content[i]):
                if ("EPartList" not in content[i] and "/EndGameParts/" not in content[i]):
                    part = content[i].split("/")
                    itemParts = itemParts + "\n" + part[-1][:len(part[-1])-1]
                    for n in range(10,0,-1):
                        if ("Min" in content[i-n]):
                            itemParts = itemParts + " - " + content[i-n].strip() + " " + content[i-n+1].strip()
                            break
        return "\nParts: \n" + itemParts +"\n\nAnointments:\n"+anoints+"\n"

    elif "[Shields]" in target: return compileBalString("Game/Gear/Shields/_Design/", FileContentsAsString)
    elif "[Grenades]" in target: return compileBalString("Game/Gear/GrenadeMods/_Design/", FileContentsAsString)

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
        return anoints+"\n"
    return FileContentsAsString

# Extracts select information from Partset files. Method Specifically intended for nades and shields.
def compilePartString(match, FileContentsAsString):
    itemParts = ""
    content = FileContentsAsString.split("\n")
    for i in range(0, len(content)):
        if (match in content[i]):
            if ("EPartList" not in content[i]):
                part = content[i].split("/")
                itemParts = itemParts + "\n" + part[-1][:len(part[-1])-1]
                for n in range(0,10):
                    if ("Min" in content[i-n]):
                        itemParts = itemParts + " - " + content[i-n].strip() + " " + content[i-n+1].strip()
                        break
    return itemParts +"\n"

# Extracts select information from balance files. Method Specifically intended for nades and shields.
def compileBalString(match, FileContentsAsString):
    itemParts, anoints = "", ""
    content = FileContentsAsString.split("\n")
    for i in range(0, len(content)):
        if (match in content[i]):
            if ("EPartList" not in content[i]):
                part = content[i].split("/")
                itemParts = itemParts + "\n" + part[-1][:len(part[-1])-1]                
                for n in range(0,10):
                    if ("Min" in content[i-n]):
                        itemParts = itemParts + " - " + content[i-n].strip() + " " + content[i-n+1].strip()
                        break
        elif ("/EndGameParts/" in content[i] and "PartChance" not in content[i]):
                part = content[i].split("/")
                if len(part)>6:
                    anoints = anoints + "\n" + part[-1][6:len(part[-1])-1]
    return itemParts +"\n\nAnointments\n"+anoints

# Fetches the partset file and reads it into a string.
def getPartFile(inp):
    inp=inp.replace(' ', '_')
    data=None
    if inp == '':
        print('Please enter a name after the command.')
        return 0, 0
    else:
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name.startswith('Part') or name.startswith('InvPart') or name.startswith('BPInvPart'):
                    if inp.lower() in name.lower():
                        target=os.path.join(root, name)
                        with open(target, 'r') as fp:
                            data=json.load(fp)
                            response=json.dumps(data, indent=4)
                            return response, target
        if data==None:
            print('No PartSet File for said Item Could be Found.')
            return 0, 0


if __name__ == '__main__':
    EditorHelper().cmdloop()