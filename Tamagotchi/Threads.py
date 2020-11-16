from PyQt5.QtCore import QThread, pyqtSignal #import all of the threading related classes and methods.
import sys, time #Sys used with the pyqt5 library and time is used in the threading modules.



class Update(QThread):

	"""
	A class purely for managing the
	threading behind changing values for the 
	tamagotchis health, hunger and happines over time.
	"""
	countChanged = pyqtSignal(int)
	
	def __init__(self, parent, tamagotchi):
		super().__init__()

		self.parent = parent
		self.tamagotchi = tamagotchi



	def run(self):
		clock = 1
		while not self.tamagotchi.dead:
			"""
			Main loop that runs while the tamagotchi is not dead.
			"""
			time.sleep(0.1)
			#The integer that is emitted refers to a task to be run.
			if not clock % 2:
				self.countChanged.emit(1)
			if not clock % 3:
				self.countChanged.emit(2)
			if not clock % 5:
				self.countChanged.emit(0)

			if not clock % 200:
				self.countChanged.emit(5)

			if not clock % 250:
				self.countChanged.emit(6)

			if not clock % 600:
				self.countChanged.emit(3)

			clock += 1
			
class Sleeping(QThread):

	"""
	A thread that only runs while the tamagotchi is sleeping.
	"""

	sleeping = pyqtSignal(int)

	def __init__(self, parent, tamagotchi):
		super().__init__()

		self.parent = parent
		self.tamagotchi = tamagotchi

	
	def run(self):
		#Loop of events to occur while the tamagotchi is sleeping.
		for clock in range(1, 51):
			if not clock % 10:
				self.sleeping.emit(2)
			if not clock % 5:
				self.sleeping.emit(0)
			time.sleep(0.1)
		self.sleeping.emit(3)


class Sick(QThread):

	"""
	A thread that only runs while the tamagotchi is sick.
	"""

	sick = pyqtSignal(int)

	def __init__(self, parent, tamagotchi):
		super().__init__()

		self.parent = parent
		self.tamagotchi = tamagotchi

	def run(self):
		#Loop of events that run while the tamagotchi is sick.
		while not self.tamagotchi.medicine_pressed and self.tamagotchi.sick:
			self.sick.emit(1)
			time.sleep(1)
		self.sick.emit(2)