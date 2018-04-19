from .Template import *
from .Misc_Classes import *
import pygame
from pygame.locals import *

class PauseMenu:

	def __init__(self, screen):
		self.nextState = "pause"
		self.isTwoPlayer = False
		self.reset = True

		self.screen = screen
		self.screenWidth,self.screenHeight = self.screen.get_size()
		self.backgroundColour = (0,0,0)
		self.buttonTextCol = (0, 0, 75)
		self.buttonCol = (204, 102, 0)

		self.titleFont = pygame.font.Font(None, 80)
		self.titleText = self.titleFont.render("Pause", True, (0,75,0))
		self.titleRect = self.titleText.get_rect(center=(int(self.screenWidth/2),int(self.screenHeight/2)-100))
		self.buttonList = [Button(self.screen, "gameplay", (self.isTwoPlayer,False), "continue", 40, self.buttonTextCol, self.buttonCol,(0,0)),
						   Button(self.screen, "menu", (self.isTwoPlayer,True), "Main Menu", 40, self.buttonTextCol, self.buttonCol,(0,40))]


	def startup(self,persistentVar):
		self.nextState = "pause"
		self.isTwoPlayer = persistentVar[0]

	def exit(self):
		return (self.isTwoPlayer,False)

	def getEvent(self,event):
		if event.type == MOUSEBUTTONUP:
			mousePos = pygame.mouse.get_pos()
			for button in self.buttonList:
				if button.isClicked(mousePos):
					self.nextState = button.nextState
					self.reset = button.nextStateArgs[1]

		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.nextState = "gameplay"

	def update(self):
		pass

	def draw(self):
		self.screen.fill(self.backgroundColour)
		mousePos = pygame.mouse.get_pos()
		for button in self.buttonList:
			button.draw(mousePos)
		self.screen.blit(self.titleText, self.titleRect)
