from States.Gameplay import *
from States.Main_Menu import *
from States.Pause_Menu import *

import pygame
from pygame.locals import *


class Control:

	def __init__(self):
		pygame.init()
		self.screenWidth = 500
		self.screenHeight = 500
		self.screen = pygame.display.set_mode((self.screenWidth,self.screenHeight))

		self.done = False
		self.clock = pygame.time.Clock()
		self.FPS = 8
		self.stateKeys = ["menu", "gameplay", "pause", "gameover"]
		self.statesDict = {"gameplay":Gameplay(self.screen, True),
						   "gameover":GameOver( self.screen,False),
						   "menu":MainMenu(self.screen),
						   "pause":PauseMenu(self.screen)}

		self.activeState = self.statesDict[self.stateKeys[0]]
		self.lastState = self.activeState
		self.persistentVar = False

	def gameloop(self):
		while not self.done:
			dt = self.clock.tick(self.FPS)
			nextState = self.statesDict[self.activeState.nextState]

			if self.activeState == nextState:
				for event in pygame.event.get():
					if event.type == QUIT:
						self.activeState.exit()
						self.done = True
					self.activeState.getEvent(event)
				self.activeState.update()
				self.activeState.draw()

				pygame.display.update()
			else:
				self.persistentVar = self.activeState.exit()
				self.activeState = nextState
				self.activeState.startup(self.persistentVar)


control = Control()
control.gameloop()
