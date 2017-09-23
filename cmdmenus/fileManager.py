import os
from . import *

def listDir(*args, **kwargs):
    ents = os.listdir(*args, **kwargs)
    for ent in ents:
        if os.path.isdir(ent):
            printToScreen(click.style(ent, fg = 'blue'), end = ' ')
        else:
            printToScreen(click.style(ent), end = ' ')
    printToScreen()
    
def chdir(dirName = "/home"):
    try:
        os.chdir(dirName)
    except FileNotFoundError:
        pass

def fileManager(mode = 'SELECTDIR'):
    mode = mode.upper()
    def fManagerGet(prompt = "Enter a directory", fileMustNotExist = False, fileMustExists = False, isDir = True):
        availCmds = {'ls':listDir, 'pwd': os.getcwd, 'cd': chdir}
        while True:
            loc = inputUniversal(prompt + ": ").strip()
            if len(loc.split(' ')) > 1:
                words = loc.split(' ')
                if words[0] in availCmds:
                    try:
                        availCmds[words[0]](" ".join(words[1:]))
                    except TypeError:
                        availCmds[words[0]]()
                else:
                    printToScreen("Unknown entry, no spaces allowed in path names or command unknown")
            elif( loc in availCmds ):
                try: 
                    out = availCmds[loc]()
                    if out is not None:
                        printToScreen(out)
                except NotADirectoryError:
                    pass
            elif fileMustExists and not os.path.isfile(loc): # not a file
                printToScreen("File {} does not exist. Commands {} are available".format(loc, list(availCmds)))
            elif fileMustNotExist and os.path.isfile(loc): # is a file
                printToScreen("File {} already exists, delete the file or choose a new file name". format(loc))
            elif isDir and not os.path.isdir(loc):
                printToScreen("Directory {} does not exist. Commands {} are available".format(loc, list(availCmds)))
            else:
                return loc

    if mode == 'SELECTDIR':
        return fManagerGet(prompt = "Enter a directory", fileMustNotExist = False, fileMustExists = False, isDir = True)

    elif mode == 'NEWFILE':
        return fManagerGet(prompt = "Enter a file name", fileMustNotExist = True, fileMustExists = False, isDir = False)

    elif mode == 'SELECTFILE':
        return fManagerGet(prompt = "Select a file", fileMustNotExist = False, fileMustExists = True, isDir = False)
    else:
        raise Exception('Unknown mode %s'%mode)

def getEncoding(fileName):
    '''
    return the encoding type of a file
    '''
    encodings = ['ascii','utf-8','cp1250']
    for encoding in encodings:
        try:
            f = open(fileName, 'r', encoding=encoding)
            f.read()
            f.close()
            return encoding
        except Exception as E:
            continue
    return None

