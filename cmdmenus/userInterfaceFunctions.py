#userInterfaceFunctions.py
'''
This module contains all the test user interface function and general formatting tools
'''

import subprocess, click
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
        except IOError:
            raise UserWarning("File Not Found")
        except Exception as E:
            continue
    return None

def inputUniversal(arg):
    return input(arg)

def catchUserWarning(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UserWarning as uw:
            printToScreen(uw)
    return inner

def printToScreen(*args, **kwargs):
    try:
        end = kwargs.pop('end')
    except KeyError:
        end = '\n'
        
    for arg in args:
        print(click.style(str(arg) + ' ', **kwargs), end = ' ')
    print('', end = end)

def pause():
    inputUniversal("Press Enter To Continue")

def clearLines(lines):
    printToScreen("\033[F\033[K" * lines)

def calcScreen():
    try:
        rows, columns = subprocess.check_output(['stty', 'size']).strip().split()
    except:
        rows, columns = [50, 100]
    return [int(rows), int(columns)]

def printSelect(options = None, cursor = ''):
    #options are an array of strings
    uniqueOptions = set(options)
    if(len(uniqueOptions) != len(options)):
        printToScreen(uniqueOptions, options)
        raise UserWarning("None unique options")

    for i, opt in enumerate(options):
        printToScreen("\t%d) %s\n"%(i, opt))

    while True:
        resp = inputUniversal(cursor)
        if(resp.isdigit() and int(resp) < len(uniqueOptions) and int(resp) >= 0):
            return int(resp)

def selectFromList(cursor, options):
    #function the has a list of options, has a quit command and cursor, exists if the user enters one of the options and returns the option
    formatedOptions = set([option[0].title() for option in options])
    for option in formatedOptions:
        printToScreen("%s\t"%(option))

    while True:
        userIn = inputUniversal(cursor).strip().title()
        if userIn in formatedOptions:
            return [True, userIn]
        elif userIn in ['Quit','Exit']:
            return [False, None]
        else:
            printToScreen("Entry %s is not an option. Type quit to return to edit.\n"%(userIn))

def sysMessage(warning='', title='', color=None):
    rows, columns = calcScreen()
    warning.strip('\n')
    warnString = [title.center(columns, ' '), ''.center(columns, '='), warning.center(columns), ''.center(columns, '=')]
    return '\n'.join(warnString)

def userConfirm(promptString = '', checkValue = None, exitStrings = ['q','0','no','quit','exit','edit','n']):
    if(type(checkValue) != list):
        checkValue = str(checkValue).upper()
        checkValue = [checkValue]

    if type(exitStrings) == str:
        exitStrings = [exitStrings]
    exitStrings = [str(exitString).upper() for exitString in exitStrings]

    while(True):
        userInput = str(inputUniversal(promptString)).upper()

        if (userInput in checkValue):
            return checkValue.index(userInput) + 1
        elif(userInput in exitStrings):
            return False
        else:
            continue
