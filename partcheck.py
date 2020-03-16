# partcheck.py
# Creator: SSpyR
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
                                print(response)
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
                                print(response)
            if data==None:
                print('No PartSet File for said Item Could be Found.')

    # help part method
    def help_part(self):
        print('Use this to search for PartSet files. \nSimply do bal and then the name of the item you want to get the file for. \nMake sure to reference with the naming command and use the full name of the item (should be one word most of the time)')


if __name__ == '__main__':
    EditorHelper().cmdloop()