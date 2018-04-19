
from .Misc_Classes import *
from .Template import *
import pygame
from pygame.locals import *

class MainMenu(State):

	def __init__(self,screen):
		self.screen = screen
		self.screenWidth,self.screenHeight = self.screen.get_size()
		self.nextState = "menu"
		self.isTwoPlayer = False
		self.reset = True
		self.backgroundColour = (0,0,0)

		self.buttonTextCol = (0, 0, 75)
		self.buttonCol = (204, 102, 0)
		self.titleFont = pygame.font.Font(None,100)
		self.titleText = self.titleFont.render("Snake Game", True, (0,75,0))
		self.titleRect = self.titleText.get_rect(center=(int(self.screenWidth/2),int(self.screenHeight/2)-80))

		self.buttonList = [Button(self.screen, "gameplay", False, "1 Player", 40, self.buttonTextCol, self.buttonCol, (0,0)),
						   Button(self.screen, "gameplay", True, "2 Player", 40, self.buttonTextCol, self.buttonCol, (0,40))]

	def startup(self,persistentVar):
		self.nextState = "menu"
		self.isTwoPlayer,self.reset = persistentVar

	def exit(self):
		return self.isTwoPlayer,True

	def getEvent(self,event):
		if event.type == MOUSEBUTTONUP:
			mousePos = pygame.mouse.get_pos()
			for button in self.buttonList:
				if button.isClicked(mousePos):
					self.nextState = button.nextState
					self.isTwoPlayer = button.nextStateArgs


	def draw(self):
		self.screen.fill(self.backgroundColour)
		mousePos = pygame.mouse.get_pos()
		for button in self.buttonList:
			button.draw(mousePos)
		self.screen.blit(self.titleText,self.titleRect)

	def update(self):
		pass
