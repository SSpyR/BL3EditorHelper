# partcheck.py
# Creator: SSpyR
# Thanks to Prismatic for Creating the data cleaning functions
# Thanks to A Bird for Creating the Initial File System Collection

# Actually make a GUI
# Make it pretty and simple
# Had to adjust how the methods search for files do to how the exe unpacks it, may fix at some point (results in searching a lot more files than needed)
# Make input take spaces cause apparently it doesnt (maybe not?)

# Balance Alias: Balance, InvBalD
# PartSet Alias: PartSet, Partset, InvPartSet, InvPart, BPInvPartSet

# current version = 0.5.0

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
                                print(getBal(response, target))
            if data==None:
                print('No Balance File for said Item Could be Found.')

    # help bal method
    def help_bal(self):
        print('Use this to search for Balance files. \nSimply do bal and then the name of the item you want to get the file for. \nMake sure to reference with the naming command and use the full name of the item (should be one word most of the time)')

    # part method
    def do_part(self, inp):
        inp=inp.replace(' ', '_')
        data=None
        if inp == '':
            print('Please enter a name after the command.')
        else:
            for root, dirs, files in os.walk(os.getcwd()):
                for name in files:
                    if name.startswith('Part') or name.startswith('InvPart') or name.startswith('BPInvPart'):
                        if inp.lower() in name.lower():
                            target=os.path.join(root, name)
                            with open(target, 'r') as fp:
                                data=json.load(fp)
                                response=json.dumps(data, indent=4)
                                print(getParts(response, target))
            if data==None:
                print('No PartSet File for said Item Could be Found.')

    # help part method
    def help_part(self):
        print('Use this to search for PartSet files. \nSimply do bal and then the name of the item you want to get the file for. \nMake sure to reference with the naming command and use the full name of the item (should be one word most of the time)')

    # Retrieves anoints relevant to character
    def do_anoints(self, inp, character):
        inp=inp.replace(' ', '_')
        data=None
        if inp == '':
            print('Please enter a name after the command.')
        else:
            for root, dirs, files in os.walk(os.getcwd()):
                for name in files:
                    if name.startswith('Part') or name.startswith('InvPart') or name.startswith('BPInvPart'):
                        if inp.lower() in name.lower():
                            target=os.path.join(root, name)
                            with open(target, 'r') as fp:
                                data=json.load(fp)
                                response=json.dumps(data, indent=4)
                                print(getAnoints(response, target, character))
            if data==None:
                print('No PartSet File for said Item Could be Found.')
    
    # help anoints method
    def help_anoints(self):
        print("Use this if you just want a list of anoints relevant to your character \n Do anoints then the item your're interested in followed by one of Amara, Fl4k, Moze or Zane.")

# Extracts select information from Partset files.
def getParts(FileContentsAsString, target):
    if "Weapons" in target: 
        toReturn = ""
        anoints = ""
        content = FileContentsAsString.split("\n")
        
        for i in range(0, len(content)):
            if ("GPart_" in content[i]):
                part = content[i].split("/")
                if len(part)>6:
                    anoints = anoints + "\n" + part[-1][6:len(part[-1])-1]
            elif ("/Gear/Weapons/" in content[i] or "/Elemental/" in content[i]):
                if ("EPartList" not in content[i] and "/EndGameParts/" not in content[i]):
                    part = content[i].split("/")
                    toReturn = toReturn + "\n" + part[-1][:len(part[-1])-1]
                    for n in range(10,0,-1):
                        if ("Min" in content[i-n]):
                            toReturn = toReturn + " - " + content[i-n].strip() + " " + content[i-n+1].strip()
                            break
                
        return "\nParts: \n" + toReturn +"\n\nAnointments:\n"+anoints+"\n"
    elif "[Shields]" in target: return compilePartString("Game/Gear/Shields/_Design/", FileContentsAsString)
    elif "[Grenades]" in target: return compilePartString("Game/Gear/GrenadeMods/_Design/", FileContentsAsString)
    return FileContentsAsString

# Extracts select information from balance files.
def getBal(FileContentsAsString, target):
    if "Weapons" in target: 
        toReturn = ""
        anoints = ""
        content = FileContentsAsString.split("\n")
        
        for i in range(0, len(content)):
            if ("GPart_" in content[i]):
                part = content[i].split("/")
                if len(part)>6:
                    anoints = anoints + "\n" + part[-1][6:len(part[-1])-1]
            elif ("/Gear/Weapons/" in content[i] or "/Elemental/" in content[i]):
                if ("EPartList" not in content[i] and "/EndGameParts/" not in content[i]):
                    part = content[i].split("/")
                    toReturn = toReturn + "\n" + part[-1][:len(part[-1])-1]
                    for n in range(10,0,-1):
                        if ("Min" in content[i-n]):
                            toReturn = toReturn + " - " + content[i-n].strip() + " " + content[i-n+1].strip()
                            break

    elif "[Shields]" in target: return compileBalString("Game/Gear/Shields/_Design/", FileContentsAsString)
    elif "[Grenades]" in target: return compileBalString("Game/Gear/GrenadeMods/_Design/", FileContentsAsString)
    return "\nParts: \n" + toReturn +"\n\nAnointments:\n"+anoints+"\n"

def getAnoints(FileContentsAsString, target, character):
    if "Weapons" in target: 
        anoints = ""
        content = FileContentsAsString.split("\n")
        for i in range(0, len(content)):
            if ("GPart_" in content[i]):
                part = content[i].split("/")
                if len(part)>6:
                    if part[-1][6:9] == "All": anoints = anoints + "\n" + part[-1][6:len(part[-1])-1]
                    else:
                        if character=="Amara":
                            if part[-1][6] == "S": anoints = anoints + "\n" + part[-1][12:len(part[-1])-1]
                        elif character=="Fl4k":
                            if part[-1][6] == "B": anoints = anoints + "\n" + part[-1][12:len(part[-1])-1]
                        elif character=="Moze":
                            if part[-1][6] == "G": anoints = anoints + "\n" + part[-1][13:len(part[-1])-1]
                        elif character=="Zane":
                            if part[-1][6] == "O" or part[-1][6] == "C":
                                anoints = anoints + "\n" + part[-1][16:len(part[-1])-1]
        return anoints+"\n"
    return FileContentsAsString

# Extracts select information from Partset files. Method Specifically intended for nades and shields.
def compilePartString(match, FileContentsAsString):
    toReturn = ""
    content = FileContentsAsString.split("\n")
    for i in range(0, len(content)):
        if (match in content[i]):
            if ("EPartList" not in content[i]):
                part = content[i].split("/")
                toReturn = toReturn + "\n" + part[-1][:len(part[-1])-1]
                
                for n in range(0,10):
                    if ("Min" in content[i-n]):
                        toReturn = toReturn + " - " + content[i-n].strip() + " " + content[i-n+1].strip()
                        break
    return toReturn +"\n"

def compileBalString(match, FileContentsAsString):
    toReturn = ""
    anoints = ""
    content = FileContentsAsString.split("\n")
    for i in range(0, len(content)):
        if (match in content[i]):
            if ("EPartList" not in content[i]):
                part = content[i].split("/")
                toReturn = toReturn + "\n" + part[-1][:len(part[-1])-1]                
                for n in range(0,10):
                    if ("Min" in content[i-n]):
                        toReturn = toReturn + " - " + content[i-n].strip() + " " + content[i-n+1].strip()
                        break
        elif ("/EndGameParts/" in content[i] and "PartChance" not in content[i]):
                part = content[i].split("/")
                if len(part)>6:
                    anoints = anoints + "\n" + part[-1][6:len(part[-1])-1]
    return toReturn +"\n\nAnointments\n"+anoints


if __name__ == '__main__':
    EditorHelper().cmdloop()