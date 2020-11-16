from PyQt5 import QtCore, QtGui #General import for creating and managing user interface elements.
from PyQt5.QtWidgets import * #Used to import all of the widgets such as buttons, labels etc.
import sys, time #Sys used with the pyqt5 library and time is used in the threading modules.
from glob import glob #Glob library used for finding the files.
from random import choice
from os import remove

from Threads import Update, Sleeping, Sick


class MainMenu(QMainWindow):

	"""
	The Main Menu of the Application.
	"""

	def __init__(self, parent, tamagotchi):

		"""
		Initialise the window with correct sizing and titles.
		"""

		super().__init__() # Initialise the parent class, in this case QMainWindow

		self.setFixedSize(600, 600)
		self.setWindowTitle('Tamagotchi - Main Menu')
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))

		self.tamagotchi = tamagotchi
		
		with open('./styles/' + self.tamagotchi.style_name + '.css') as file:
			css = file.read()
			self.setStyleSheet(css)
		self.tamagotchi.style_sheet = css

		
		"""
		Initialise the user interface,
		this includes buttons and labels
		and their respective sizes / positions.
		"""
		
		HEADING_FONT = QtGui.QFont('Ariel', 36)
		NORMAL_FONT = QtGui.QFont('Ariel', 10)

		TITLE_TEXT = QLabel('Tamagotchi Game')
		TITLE_TEXT.setFont(HEADING_FONT)
		NEW_GAME_BUTTON = QPushButton('New Tamagotchi')
		LOAD_GAME_BUTTON = QPushButton('Load Save File')
		LOAD_GAME_BUTTON.setFixedWidth(150)

		#Style selector dropdown
		self.styles_button = QComboBox(self)
		THEMES = ['Dark Theme', 'Light Theme', 'Pink Theme']
		self.styles_button.addItem(self.tamagotchi.style_name)
		for theme in THEMES:
			if theme != self.tamagotchi.style_name:
				self.styles_button.addItem(theme)
		self.styles_button.activated[str].connect(self.select_style)

		self.find_saves()


		win = QWidget(self)
		self.setCentralWidget(win)
		grid = QVBoxLayout()
		win.setLayout(grid)

		#Sets out the buttons in a grid.
		grid.addWidget(TITLE_TEXT)
		grid.addWidget(NEW_GAME_BUTTON)
		grid.addWidget(self.styles_button)

		
		
		bar_layout = QHBoxLayout()
		bar_layout.addWidget(self.save_files)
		bar_layout.addWidget(LOAD_GAME_BUTTON)

		grid.addLayout(bar_layout)
		grid.addWidget(QLabel(''))

		grid.setAlignment(TITLE_TEXT, QtCore.Qt.AlignCenter)
		grid.setAlignment(NEW_GAME_BUTTON, QtCore.Qt.AlignCenter)
		grid.setAlignment(LOAD_GAME_BUTTON, QtCore.Qt.AlignCenter)
		grid.setAlignment(self.styles_button, QtCore.Qt.AlignCenter)


		NEW_GAME_BUTTON.clicked.connect(self.new_game)
		LOAD_GAME_BUTTON.clicked.connect(self.select_save)

	def find_saves(self):
		"""
		finds all of the save files and adds 
		then to the save file drop box
		"""
		self.save_files = QComboBox(self)
		self.save_files.setFixedWidth(150)
		self.save_files.clear()
		for file in glob('./saves/*.TAMA'):
			self.save_files.addItem(file[8:-5])
		

		



	def select_save(self):

		"""
		Initialises the Game Class with the data
		obtained from the save file given by the user.
		"""

		fileName = self.save_files.currentText()
		if fileName:
			with open('./saves/' + fileName + '.TAMA', 'r') as f:
				contents = f.read().split('\n')
				self.tamagotchi.start_game(*contents)
					

	def select_style(self, style):

		"""
		Allows the user to make the users selected
		css style take effect in the window.
		"""

		self.setStyleSheet('')
		with open('./styles/' + style + '.css') as file:
			css = file.read()
			self.setStyleSheet(css)

			self.tamagotchi.style_name = style
			self.tamagotchi.style_sheet = css
					
	def new_game(self):

		"""
		Promts the user for a name and then
		initialises the Game class with the default
		values.
		"""
		style_name = self.styles_button.currentText()
		text, valid = QInputDialog.getText(self, 'Tamagotchi Input Dialog', 'Enter your Tamagotchi name:')
		if valid and text:
			self.tamagotchi.start_game(text, 100, 100, 100, style_name, 1)


class Game(QMainWindow):
	"""
	The Game class contains the main window of the tamagotchi game.
	"""

	def __init__(self, parent, tamagotchi):

		"""
		On initialisation the class creates the window and sets the 
		variables.
		"""

		super().__init__() # Initialise the parent class, in this case QMainWindow.

		self.tamagotchi = tamagotchi
		self.parent = parent

		self.setFixedSize(750, 600)
		self.setWindowTitle('Tamagotchi')
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))


		HEADING_FONT = QtGui.QFont('Ariel', 36)
		NORMAL_FONT = QtGui.QFont('Ariel', 16)

		#Declare buttons
		main_menu = QPushButton('Main Menu')
		self.save_game = QPushButton('Save Current Game')
		self.discipline = QPushButton('Discipline')
		self.duck = QPushButton('Duck')
		self.feed = QPushButton('Feed Pet')
		self.game = QPushButton('Play with Pet')
		self.medicine = QPushButton('Medicine')
		self.sleep = QPushButton('Sleep')

		main_menu.setToolTip('Return to the main menu.')
		self.save_game.setToolTip('Automatically save the current tamagotchi.')

		#Create window layout
		win = QWidget()
		self.setCentralWidget(win)
		grid = QVBoxLayout()
		win.setLayout(grid)

		top_row = QHBoxLayout()
		top_row.addWidget(main_menu)
		top_row.addWidget(self.save_game)
		top_row.addWidget(self.discipline)
		top_row.addWidget(self.duck)

		grid.addLayout(top_row)


		middle_row = QHBoxLayout()

		self.img = QLabel()

		self.progress_health = QProgressBar(self)
		self.progress_hunger = QProgressBar(self)
		self.progress_happiness = QProgressBar(self)

		self.label_name = QLabel()
		self.label_name.setFont(HEADING_FONT)

		label_health = QLabel('Health: ')
		label_health.setFont(NORMAL_FONT)
		label_hunger = QLabel('Hunger: ')
		label_hunger.setFont(NORMAL_FONT)
		label_happiness = QLabel('Happiness: ')
		label_happiness.setFont(NORMAL_FONT)

		bar_layout = QVBoxLayout()
		bar_layout.addWidget(self.label_name)

		bar_layout.addWidget(label_health)
		bar_layout.addWidget(self.progress_health)

		bar_layout.addWidget(label_hunger)
		bar_layout.addWidget(self.progress_hunger)

		bar_layout.addWidget(label_happiness)
		bar_layout.addWidget(self.progress_happiness)

		self.status = QLabel('')
		self.status.setFont(NORMAL_FONT)
		self.status.setFont(QtGui.QFont('Ariel', 18))
		bar_layout.addWidget(self.status)


		middle_row.addWidget(self.img)
		middle_row.addLayout(bar_layout)
		#grid.addLayout(bar_layout, 1, 2, 1, 2)
		grid.addLayout(middle_row)
		#Add the bottom row of buttons

		bottom_row = QHBoxLayout()

		bottom_row.addWidget(self.feed)
		bottom_row.addWidget(self.game)
		bottom_row.addWidget(self.medicine)
		bottom_row.addWidget(self.sleep)

		grid.addLayout(bottom_row)

		#Define button on-click events
		main_menu.clicked.connect(self.menu_button)
		self.save_game.clicked.connect(self.save_current_game)

		
		self.medicine.clicked.connect(lambda: self.onSick(2))
		self.feed.clicked.connect(lambda: self.update_stats('hunger', self.progress_hunger, 10))
		self.game.clicked.connect(lambda: self.parent.frames[HappinessGame].layout())
		self.sleep.clicked.connect(self.change_lights)

		self.duck.clicked.connect(self.clean_tamagotchi)
		self.discipline.clicked.connect(self.discipline_tamagotchi)


		self.progress_health.setMaximum(100)

		self.progress_health.setTextVisible(False)

		self.progress_hunger.setMaximum(100)
		self.progress_hunger.setTextVisible(False)

		self.progress_happiness.setMaximum(100)
		self.progress_happiness.setTextVisible(False)


	def init_stats(self):

		"""
		Sets the variables of the game window.
		Is used when reopening the game window to reset the stats.
		"""

		#opens the selected stylesheet and sets the style to it.
		with open('./styles/' + self.tamagotchi.style_name + '.css') as file:
			css = file.read()
			self.setStyleSheet(css)

		gif = QtGui.QMovie(self.tamagotchi.DIRECTORY + str(self.tamagotchi.age) + '.gif')
		gif.setScaledSize(QtCore.QSize().scaled(300, 300, QtCore.Qt.KeepAspectRatio))
		self.img.setMovie(gif)
		gif.start()

		#resest all of the stats for either save file or new tamagotchi
		self.label_name.setText(self.tamagotchi.name)
		self.progress_health.setValue(int(self.tamagotchi.health))
		self.progress_hunger.setValue(int(self.tamagotchi.hunger))
		self.progress_happiness.setValue(int(self.tamagotchi.happiness))

		self.disable_enable_buttons(True)
		self.save_game.setEnabled(True)

		self.status.setText('')

		self.discipline.setEnabled(False)
		self.duck.setEnabled(False)
		#self.new_stats.start()

	def clean_tamagotchi(self):
		"""
		cleans the tamagotchi
		"""
		self.tamagotchi.needs_cleaning = False
		#if the tamagotchi still needs disciplinng change the stats to disciplining
		if self.tamagotchi.needs_discipline == True:
			self.status.setText(self.tamagotchi.name.strip()+' needs Disciplining')

		elif self.tamagotchi.sleeping == True:
			self.status.setText('')
		else:
			self.disable_enable_buttons(True)
			self.status.setText('')
		self.duck.setEnabled(False)

	def discipline_tamagotchi(self):
		"""
		disciplines the tamagotchi
		"""
		self.tamagotchi.needs_discipline = False
		#if the tamagotchi still needs cleaning change the stats to cleaning
		if self.tamagotchi.needs_cleaning == True:
			self.status.setText(self.tamagotchi.name.strip()+' needs Cleaning')
		elif self.tamagotchi.sleeping == True:
			self.status.setText('')

		else:
			self.disable_enable_buttons(True)
			self.status.setText('')
			
		self.discipline.setEnabled(False)
		

	def disable_enable_buttons(self, state):
		self.sleep.setEnabled(state)
		self.game.setEnabled(state)
		self.feed.setEnabled(state)
		self.medicine.setEnabled(state)


	def change_lights(self):
		"""
		changes the tamagotchi gif to sleeping or awake
		starts the Sleeping thread
		"""

		if not self.tamagotchi.sleeping:

			gif = QtGui.QMovie(self.tamagotchi.DIRECTORY + str(self.tamagotchi.age) + '-Sleep.gif')
			gif.setScaledSize(QtCore.QSize().scaled(300, 300, QtCore.Qt.KeepAspectRatio))
			self.img.setMovie(gif)
			gif.start()
			self.disable_enable_buttons(False)
			self.parent.threads[Sleeping].start()

		else:
			gif = QtGui.QMovie(self.tamagotchi.DIRECTORY + str(self.tamagotchi.age) + '.gif')
			gif.setScaledSize(QtCore.QSize().scaled(300, 300, QtCore.Qt.KeepAspectRatio))
			self.img.setMovie(gif)
			gif.start()
		
		self.tamagotchi.sleeping = not self.tamagotchi.sleeping

	def getting_sick(self):
		"""
		the tamagotch doesnt get sick till it wakes up
		sets the sprite to the sick tamagotchi sprite
		"""
		
		if not self.tamagotchi.sleeping:

			self.tamagotchi.sick = True
			self.status.setText(self.tamagotchi.name.strip() + ' needs medicine.')
			pixmap = QtGui.QPixmap(self.tamagotchi.DIRECTORY + str(self.tamagotchi.age) + '-Sick.png').scaled(300, 300)
			self.img.setPixmap(pixmap)
			#disables all buttons excepet for medicine
			self.sleep.setEnabled(False)
			self.game.setEnabled(False)
			self.medicine.setEnabled(True)
			self.parent.threads[Sick].start()


	def onSleep(self, value):
		"""
		increases the tamagotchi's health and stops the health and hunger from changing
		"""

		bars = [self.progress_health, self.progress_hunger, self.progress_happiness]
		stats = ['health', 'hunger', 'happiness']

		if value == 0:
			self.update_stats(stats[value], bars[value], 5)

		elif value == 2:
			self.update_stats(stats[value], bars[value], 1)

		elif value == 3:
			self.change_lights()
			self.disable_enable_buttons(True)

	def onSick(self, value):
		"""
		when the tamagotchi is sick he health and happiness of the tamagotchi decrease faster
		and eneables the medicin button
		"""
		if value == 1:
			self.update_stats('health', self.progress_health, -5)
			self.update_stats('happiness', self.progress_happiness, -3)
			
		if value == 2 and not self.tamagotchi.dead:
			self.sleep.setEnabled(True)
			self.game.setEnabled(True)
			self.tamagotchi.sick = False
			self.tamagotchi.medicine_pressed = True
			self.status.setText('')
			self.update_stats('hunger', self.progress_hunger, 20)
			self.update_stats('happiness', self.progress_happiness, 20)
			self.tamagotchi.medicine_pressed = False
			gif = QtGui.QMovie(self.tamagotchi.DIRECTORY + str(self.tamagotchi.age) + '.gif')
			gif.setScaledSize(QtCore.QSize().scaled(300, 300, QtCore.Qt.KeepAspectRatio))
			self.img.setMovie(gif)
			gif.start()


	def onCountChanged(self, value):

		"""
		A method for the game class that is controlled by the StatChange class.
		This method is called periodically throughout the running of the code.
		"""

		if self.tamagotchi.playing_with_pet:
			return

		bars = [self.progress_health, self.progress_hunger, self.progress_happiness]
		stats = ['health', 'hunger', 'happiness']

		if value < 3:
			self.update_stats(stats[value], bars[value], -1)

			for bar in bars[1:]:
				if bar.value() <= 0:

					self.getting_sick()

			if self.progress_health.value() <= 0:

				self.tamagotchi.dead = True
				self.dead_tamagotchi()

			if not self.tamagotchi.sick:
				self.medicine.setEnabled(False)

		#if the age of the tamagotchi is above 3 so it has aged past old age it dies
		if value == 3:
			self.tamagotchi.age += 1
			if self.tamagotchi.age > 3:
				self.tamagotchi.dead = True
				self.dead_tamagotchi()
			#change the sprite of the tamagotchi to an older version of it
			else:
				gif = QtGui.QMovie(self.tamagotchi.DIRECTORY + str(self.tamagotchi.age) + '.gif')
				gif.setScaledSize(QtCore.QSize().scaled(300, 300, QtCore.Qt.KeepAspectRatio))
				self.img.setMovie(gif)
				gif.start()

		if value == 5 and self.tamagotchi.sick == False:
			self.status.setText(self.tamagotchi.name.strip() + ' needs Disciplining')
			self.tamagotchi.needs_discipline = True
			self.discipline.setEnabled(True)
			self.disable_enable_buttons(False)

		if value == 6 and self.tamagotchi.sick == False and self.tamagotchi.sleeping == False:
			self.status.setText(self.tamagotchi.name.strip() + ' needs Cleaning')
			self.tamagotchi.needs_cleaning = True
			self.duck.setEnabled(True)
			self.disable_enable_buttons(False)



	def menu_button(self):

		"""
		Method is called when the user presses the button to
		go back to the main menu.
		"""
		#reloads all of the save files
		self.parent.frames[MainMenu].save_files.clear()
		for file in glob('./saves/*.TAMA'):
			self.parent.frames[MainMenu].save_files.addItem(file[8:-5])
		self.parent.show_window(MainMenu)
		self.parent.threads[Update].quit()
		self.hide()


	def update_stats(self, stat, bar, amount):

		"""
		Method called whenever the user presses either
		of the happines, hunger or health button.
		"""
		#if the increase is above 100 it sets the amount to 100
		if bar.value() + amount >= 100:
			amount = 100
		else:
			amount = bar.value() + amount
		bar.setValue(amount)
		exec('self.tamagotchi.' + stat + ' = str(bar.value())')
		

	def save_current_game(self):
		"""
		Saves the current game file.
		"""
		self.status.setText('File has been saved!')
		self.save_game.setToolTip('File has been saved!')
		saved_contents = self.tamagotchi.name+'\n'+self.tamagotchi.health+'\n'+self.tamagotchi.hunger+'\n'+self.tamagotchi.happiness+'\n'+self.tamagotchi.style_name+'\n'+str(self.tamagotchi.age)

		with open('saves/'+self.tamagotchi.name+'.TAMA', 'w') as file:
			file.write(saved_contents)


	def dead_tamagotchi(self):
		"""
		chnages th tamagotchi to the dead sprite
		disables all buttons except for main menu
		delete the tamagotchi's save file
		"""
		pixmap = QtGui.QPixmap('./img/dead.png').scaled(300, 300)
		self.status.setText(self.tamagotchi.name.strip() + ' has died')
		self.img.setPixmap(pixmap)
		self.disable_enable_buttons(False)
		self.discipline.setEnabled(False)
		self.duck.setEnabled(False)
		self.save_game.setEnabled(False)
		if self.tamagotchi.name in [file[8:-5] for file in glob('./saves/*.TAMA')]:
			remove('./saves/' + self.tamagotchi.name + '.TAMA')


class HappinessGame(QMainWindow):
	"""
	this class contains the happiness mini game
	"""
	def __init__(self, parent, tamagotchi):

		super().__init__()

		self.tamagotchi = tamagotchi
		self.parent = parent

		#Create window layout
		self.setFixedSize(500, 400)
		self.setWindowTitle('Tamagotchi')
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))
		

		win = QWidget()
		self.setCentralWidget(win)
		grid = QGridLayout()
		win.setLayout(grid)

		#Creates left and right guess buttons
		self.guess_left = QPushButton('Left')
		self.guess_right = QPushButton('Right')
		self.confirm = QPushButton('OK')

		self.img = QLabel(self)
		self.results = QLabel('')
		self.results.setFont(QtGui.QFont('Ariel', 12))

		grid.addWidget(self.img, 0, 0, 1, 2)
		grid.addWidget(self.guess_left, 1, 0)
		grid.addWidget(self.guess_right, 1, 1)
		grid.addWidget(self.results, 2, 0)
		grid.addWidget(self.confirm, 2, 1)


		self.confirm.clicked.connect(self.confirmed)
		self.guess_left.clicked.connect(lambda: self.guessed(0))
		self.guess_right.clicked.connect(lambda: self.guessed(1))

		

	def layout(self):

		"""
		Chnages the layout of the happiness game window
		and chooses a direction for the tamagotchi to move
		"""
		self.parent.hide_window(Game)
		self.guess_left.setEnabled(True)
		self.guess_right.setEnabled(True)
		self.confirm.setEnabled(False)
		self.won_game = False
		self.tamagotchi.playing_with_pet = True
		

		with open('./styles/' + self.tamagotchi.style_name + '.css') as file:
			css = file.read()
			self.setStyleSheet(css)

		self.random = choice([0,1])
		#sets the sprite of the tamagotchi to the direction chosen
		if self.random == 0:
			pixmap = QtGui.QPixmap(self.tamagotchi.DIRECTORY + str(self.tamagotchi.age) + '-Left.png').scaled(300, 300)
			self.img.setPixmap(pixmap)
		elif self.random == 1:
			pixmap = QtGui.QPixmap(self.tamagotchi.DIRECTORY + str(self.tamagotchi.age) + '-Right.png').scaled(300, 300)
			self.img.setPixmap(pixmap)

		self.parent.frames[Game].disable_enable_buttons(False)
		self.hide()
		self.show()


	def guessed(self, direction):
		"""
		Creates a random number from when the user presses a button 
		Making a direction for the tamagotchi. 1/2 times the user will be correct.
		"""

		self.guess_left.setEnabled(False)
		self.guess_right.setEnabled(False)
		self.confirm.setEnabled(True)
		
		if direction == self.random:
			self.won_game = True
			self.results.setText('You Guessed Correct.')
		else:
			self.results.setText('You Guessed Wrong')


	def confirmed(self):
		"""
		resets the results and reopens the game window
		updates the happiness stat if you win
		"""
		self.results.setText('')
		if self.won_game:
			self.parent.frames[Game].update_stats("happiness", self.parent.frames[Game].progress_happiness, 50)

		self.tamagotchi.playing_with_pet = False
		self.parent.frames[Game].disable_enable_buttons(True)
		self.parent.frames[Game].medicine.setEnabled(False)
		self.hide()
		self.parent.show_window(Game)


	def closeEvent(self, event):
		"""
		if the user closes the happiness game window it will reopen the game window 
		and enable all the buttons
		"""
		self.parent.show_window(Game)
		self.parent.frames[Game].disable_enable_buttons(True)
		self.parent.frames[Game].medicine.setEnabled(False)
		self.tamagotchi.playing_with_pet = False
