#userInterfaceFunctions.py
'''
This module contains all the test user interface function and general formatting tools
'''

import npyscreen, os, subprocess, click
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

def sigFigs(x, n):
    import math
    try:
        return round(float(x), int(n - math.ceil(math.log10(abs(x)))))
    except:
        if(x == 0):
            return 0
        else:
            return 'NULL'

def isNumber(num):
    num = str(num)
    try:
        float(num)
        if(num.isalpha()): # removes inf, nan
            return False
        else:
            return True
    except ValueError:
        return False

def findSciNote(varIn, sciNote):
    import string
    if(isNumber(varIn)):#no sciNote
        return [('',1), float(varIn)]

    varIn = str(varIn).strip(string.punctuation).strip()#strip all symbols

    if(isNumber(varIn)):#no sciNote
        return [('',1), float(varIn)]

    def numCheck(varIn, sciSymbol):
        if(varIn.count(sciSymbol)):
            splitNum = str(varIn).split(sciSymbol)[0]
            if isNumber(splitNum):
                return splitNum
        return False

    for sciSymbol in sciNote:
        num = numCheck(varIn, sciSymbol[0])
        if num is not False:
            return [sciSymbol, float(num)]

    varTest = None
    for i in range(len(varIn)):
        if(isNumber(varIn[:i+1])):
            varTest = varIn[:i+1]
            continue
        else:
            break
    if(isNumber(varTest)):#no sciNote
        return [('',1), float(varTest)]

    raise ValueError('%s is not a recognizable number'%(varIn))

def orderOfMagnitude(varIn):
    decLength = 8
    sciNote = tuple(zip(['f', 'p',  'n',  'u',  'm', 'K', 'k', 'M', 'G',  'T'],[1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1e3, 1e3, 1e6, 1e9, 1e12]))

    try:
        sciSymbol, num = findSciNote(varIn, sciNote)
        floatVal = num * sciSymbol[1]
    except ValueError:
        return (varIn,'NULL')
    sciIndex = None
    for sciSymbol in sciNote:
        if(abs(floatVal) >= sciSymbol[1]):
            sciIndex = sciSymbol
        else:
            break

    #check if 1 is the best sciNote
    if(1 <= abs(floatVal) < 1000 or abs(floatVal) < sciNote[0][1] or abs(floatVal) == 0.):
        val = sigFigs(floatVal,decLength)
        return str(val), val

    else:
        return ("{}{}".format(sigFigs(floatVal/sciIndex[1],decLength), sciIndex[0])), sigFigs(floatVal,decLength)

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
