
class State:
	""" an empty class used as a marker for other state classes """
	def __init__(self):
		pass

	def startup(self,persistentVar):
		pass

	def exit(self):
		persistentVar = "anything"
		return persistentVar

	def draw(self):
		pass

	def update(self):
		pass

	def getEvent(self,event):
		pass
