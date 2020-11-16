#To run properly, you need the PyQt5 Library.
#pip install PyQt5-tools is the command to install it.
#Project was created in sublime text  + visual studio code in  Python version 3.7

from PyQt5.QtWidgets import * #Used to import all of the widgets such as buttons, labels etc.
import sys, time #Sys used with the pyqt5 library and time is used in the threading modules.

#imports the other classes
from Windows import MainMenu, Game, HappinessGame
from Threads import Update, Sleeping, Sick


class AppWindow():
	"""
	Manages the other screens and threads
	run all of the __init__ methods of classes
	"""
	def __init__(self):

		tamagotchi = Tamagotchi(self)

		#Creates all of the windows
		self.frames = {}
		for f in (MainMenu, Game, HappinessGame):
			frame = f(self, tamagotchi)
			self.frames[f] = frame
		
		#creates all of the threads
		self.threads = {}
		for t in (Update, Sleeping, Sick):
			thread = t(self, tamagotchi)
			self.threads[t] = thread

		self.show_window(MainMenu)

		#Connect the threads to their respective methods.
		self.threads[Update].countChanged.connect(self.frames[Game].onCountChanged)
		self.threads[Sleeping].sleeping.connect(self.frames[Game].onSleep)
		self.threads[Sick].sick.connect(self.frames[Game].onSick)

	#Methods for showing and hiding windows, respectively.
	def show_window(self, window):
		window = self.frames[window]
		window.show()
	def hide_window(self, window):
		window = self.frames[window]
		window.hide()


class Tamagotchi():
	"""
	hold all of the information about the tamagotchi
	and handles the starting of the game
	"""
	def __init__(self, parent):
		"""
		Sets all of the Tamamgotchi states
		"""
		self.parent = parent
		self.sick = False
		self.dead = False
		self.medicine_pressed = False
		self.playing_with_pet = False
		self.needs_discipline = False
		self.needs_cleaning = False
		self.style_name = 'Light Theme'



	def start_game(self, name, health, hunger, happiness, style, age):
		"""
		Sets all of the tamagotchi's stats and starts the threads
		"""

		self.name = name
		self.health = str(health)
		self.hunger = str(hunger)
		self.happiness = str(happiness)
		self.style_name = style

		self.age = int(age)

		self.DIRECTORY = './img/Eggplant/Eggplant'

		self.sleeping = False
		self.dead = False
		self.sick = False
		
		#Initialise stats, start the threads and show/hide relevant windows.
		self.parent.frames[Game].init_stats()
		self.parent.threads[Update].start()
		self.parent.hide_window(MainMenu)
		self.parent.show_window(Game)

#Initialise the application.
app = QApplication(sys.argv)
controller = AppWindow()
app.exec_()