#menuClasses.py
'''
Menu is the base for all menus, options are objects with a 'run' member function
'''
import subprocess, os, textwrap
from heodb.interface import sysMessage, printToScreen, inputUniversal, calcScreen

global linePad
linePad = 50
class Menu(object):
	'''
	Menu is the base class for all menus
	'''
	def __init__(self, db, description, cursor):
		self.db = db
		self.cursor = cursor
		self.title = "Hobbs ElectroOptics Database: %s"%(os.environ['dataBase'])
		self.description = description
		self.MenuOptions = []
		self.GeneralOptions = []

		self.SQLOption = self.addGeneralOption(SQLCall(db))
		self.QuitOption = self.addGeneralOption(Quit(db))

	def run(self):
		printToScreen(self.makeScreen())
		while True:
			userInput = inputUniversal(self.cursor).upper().strip()
			if(userInput in ['0','Q','QUIT','EXIT']):
				self.QuitOption.run()

			if(userInput in ['CLEAR', 'C']):
				os.system('clear')
				printToScreen(self.makeScreen())

			elif(userInput in ['S']):
				self.SQLOption.run()

			elif(userInput in ['H', '?','HELP']):
				os.system("echo '%s' | less"%(self.helpScreen()))

			elif(userInput.isdigit() and int(userInput) <= len(self.MenuOptions)):
				try:
					if(self.MenuOptions[int(userInput) -1].clear):
						os.system('clear')
					self.MenuOptions[int(userInput) -1].run()
					if(self.MenuOptions[int(userInput) -1].commit):
						self.db.commit()
				except KeyboardInterrupt:
					break
				except UserWarning as uw:
					printToScreen(uw)
					continue


	def addOption(self, option):
		self.MenuOptions.append(option)
		return option

	def addGeneralOption(self, option):
		self.GeneralOptions.append(option)
		return option

	def numberedLine(self, text, count):
		rows, columns = calcScreen()
		return ("\t\t%d)  %s"%(count, text)).ljust(linePad, ' ').center(columns).title()

	def borderString(self):
		rows, columns = calcScreen()
		return ''.center(columns,'#')

	def underLine(self, inStr = None, minLength = 12):
		if len(inStr) < minLength:
			return '='*minLength
		return len(inStr) * '='

	def makeTitle(self, title, description):
		titleString = []
		rows, columns = calcScreen()
		titleString.append(self.borderString())
		titleString.append('\n\n')
		titleString.append(title.center(columns))
		titleString.append('\n')
		titleString.append('%s'%(self.underLine(inStr=title).center(columns)))
		titleString.append('\n\n')
		titleString.append(('    %s:'%(description)).center(columns).title())
		titleString.append('\n\n')
		return titleString

	def makeScreen(self):
		screen = self.makeTitle(self.title, self.description)

		screen.extend("%s"%(self.numberedLine(self.MenuOptions[i].title, i + 1)) + '\n' for i in range(len(self.MenuOptions)))

		screen.append('\n\n')
		screen.append(self.borderString())
		screen.append('\n\n')
		return ''.join(screen)

	def helpLine(self, columns):
		for i in range(len(self.MenuOptions)):
			y = ['%d'%(i+1)]
			y.append( ("%s"%(self.numberedLine(self.MenuOptions[i].title, i + 1))) )
			y.append('\n')
			y.append( ("\t   -%s"%('\n'.join(textwrap.wrap(self.MenuOptions[i].description)))) )
			y.append('\n')
			for obj in y:
				yield obj

	def helpScreen(self):
		rows, columns = calcScreen()
		if columns > 70:
			helpColumns = 60
		else:
			helpColumns = columns-8

		screen = self.makeTitle('Help', 'Help Menu')
		helpTups = [(option.title.title(), option.description.capitalize()) for option in self.MenuOptions]
		numedTups = tuple(zip(range(1, len(helpTups) +1), helpTups))
		for numedTup in numedTups:
			screen.append("   %d) %s\n\t%s\n\n"%(numedTup[0], numedTup[1][0], '\n\t'.join(textwrap.wrap(numedTup[1][1], width=helpColumns)) ))
		screen.append('\n\n')
		screen.append(self.borderString())
		screen.append('\n\n')
		return ''.join(screen)

class MenuOption(object):
	def __init__(self, db = None, title = None, description = None, commit = False, clear = True):
		self.db = db
		self.title = title
		self.description = description
		self.commit = commit
		self.clear = clear
		self.typeCheck()

	def typeCheck(self):

		if(not type(self.commit) == bool):
			raise UserWarning('commit must be a boolean')
		if(not type(self.clear) == bool):
			raise UserWarning('clear must be a boolean')

	def run(self):
		pass

class SQLCall(MenuOption):
	def __init__(self, db):
		MenuOption.__init__(self, db, title = 'Enter MYSQL DB', description = 'Enter the MYSQL command line', commit = True, clear = True)

	def run(self):
		os.system('mysql -u $user -p$pass $dataBase')

class Quit(MenuOption):
	def __init__(self, db):
		MenuOption.__init__(self, db, title = 'Quit', description = 'Return to previous menu', commit = True, clear = True)

	def run(self):
		raise KeyboardInterrupt

if ( __name__ == "__main__" ):

	os.environ['program'] = os.getcwd()
	db=sql.connect(host = "localhost", user = os.environ['user'], passwd = os.environ['pass'], db = os.environ['dataBase'])
	DBCore(db).run()
