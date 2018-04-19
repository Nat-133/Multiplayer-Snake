"""
Contains classes relating to the gameplay states (1player, 2player and Game Over)
"""
from .Template import *
import random
import pygame
from pygame.locals import *
import pickle
import os


class Gameplay(State):

	score = 0

	def __init__(self, screen, twoPlayer):
		self.nextState = "gameplay"
		self.screenWidth, self.screenHeight = screen.get_size()
		self.screen = screen
		self.backgroundColour = (0,0,0)
		self.lineColour = (15,15,15)
		self.textColour = (0,50,0)

		self.xDivisionNo = 20  # the number of cells along the top of the screen
		self.divisionWidth = self.screenWidth / self.xDivisionNo
		self.yDivisionNo = self.screenHeight / self.divisionWidth

		self.lines = []
		for x in range(self.screenWidth):
			if x%self.divisionWidth == 0:
				self.lines.append(((x,0),(x,self.screenHeight)))
		for y in range(self.screenHeight):
			if y%self.divisionWidth == 0:
				self.lines.append(((0,y),(self.screenWidth,y)))

		self.gameOver = False

		self.twoPlayer = twoPlayer
		self.snakeList = [Snake((self.divisionWidth*3,self.divisionWidth*3),
								self.divisionWidth, self.screenWidth, self.screenHeight,
								K_w,K_s,K_a,K_d,(255,255,255),(0,75,0))]
		if self.twoPlayer:
			self.snakeList.append(Snake((self.screenWidth-self.divisionWidth*3,self.screenHeight-self.divisionWidth*3),
										self.divisionWidth, self.screenWidth, self.screenHeight,
										K_UP,K_DOWN,K_LEFT,K_RIGHT,(100,100,255),(0,0,75)))
			self.snakeList[1].direction = (0,-1)
			self.snakeList[0].colour = (255,100,100)
			self.snakeList[0].foodColour = (75,0,0)
		Gameplay.score = len(self.snakeList)
		self.font = pygame.font.Font(None, 40)
		self.text = self.font.render("{}".format(Gameplay.score), False, self.textColour)
		self.textRect = self.text.get_rect(center=(int(self.screenWidth/2),20))

	def drawLines(self):
		for line in self.lines:
			pygame.draw.line(self.screen, self.lineColour, line[0],line[1])

	def drawScore(self):
		self.screen.blit(self.text,self.textRect)

	def updateScore(self):
		score = 0
		for snake in self.snakeList:
			score += len(snake.segments)
		Gameplay.score = score
		self.text = self.font.render("{}".format(Gameplay.score), False, self.textColour)
		self.textRect = self.text.get_rect(center=(int(self.screenWidth / 2), 20))

	def update(self):
		for snake in self.snakeList:
			snake.move()
			if snake.killed:
				self.gameOver = True
				self.nextState = "gameover"
		self.updateScore()

	def draw(self):
		self.screen.fill(self.backgroundColour)
		self.drawLines()
		for snake in self.snakeList:
			snake.draw(self.screen)
		self.drawScore()

	def getEvent(self,event):
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.nextState = "pause"

		for snake in self.snakeList:
			snake.handleEvent(event)

	def exit(self):
		Snake.cells = []
		if self.gameOver:
			currentPath = os.path.dirname(__file__)
			newPath = os.path.join(currentPath, "..\\High Scores\\highscore{}p.txt".format(len(self.snakeList)))
			with open(newPath,"rb") as f:
				highscore = pickle.load(f)
			if Gameplay.score > highscore:
				with open(newPath,"wb") as f:
					pickle.dump(Gameplay.score,f)
		return self.twoPlayer, False

	def startup(self,persistentVar):
		self.nextState = "gameplay"
		twoPlayer,reset = persistentVar
		if self.gameOver or self.twoPlayer != twoPlayer or reset:
			self.gameOver = False
			self.twoPlayer = twoPlayer
			self.snakeList = [Snake((self.divisionWidth * 3, self.divisionWidth * 3),self.divisionWidth, self.screenWidth, self.screenHeight,K_w, K_s, K_a, K_d)]
			if self.twoPlayer:
				self.snakeList.append(
					Snake((self.screenWidth - self.divisionWidth * 3, self.screenHeight - self.divisionWidth * 3),
						  self.divisionWidth, self.screenWidth, self.screenHeight,
						  K_UP, K_DOWN, K_LEFT, K_RIGHT, (100, 100, 255), (0, 0, 75)))
				self.snakeList[1].direction = (0, -1)
				self.snakeList[0].colour = (255, 100, 100)
				self.snakeList[0].foodColour = (75, 0, 0)
		for snake in self.snakeList:
			snake.generateCells(self.screenWidth,self.screenHeight)


class Snake:
	"""
	This class controls snake behavior.
	It has methods for movement, collision detection and food eating
	"""
	cells = []  # becomes a variable containing a list of points
	#   		  representing all the cells not occupied by any snakes
	foodPos = []  # cells without any points containing food

	def __init__(self, pos, width, screenWidth, screenHeight, upKey, downKey, leftKey, rightKey,
				 colour=(255, 255, 255),foodColour=(0,75,0)):
		self.killed = False

		self.screenWidth = screenWidth
		self.screenHeight = screenHeight

		self.width = width
		self.segments = [pygame.Rect(pos, (width, width))]
		self.colour = colour
		self.foodColour = foodColour

		self.generateCells(screenWidth, screenHeight)

		self.upKey = upKey
		self.downKey = downKey
		self.leftKey = leftKey
		self.rightKey = rightKey
		self.direction = (0, 1)
		self.lastMove = (0, 1)

	def generateCells(self, screenWidth, screenHeight):
		if not Snake.cells:
			Snake.foodPos = []
			for x in range(screenWidth):
				if (x % self.width) == 0:
					for y in range(screenHeight):
						if (y % self.width) == 0:
							Snake.cells.append((x, y))

		for segment in self.segments:
			try:
				Snake.cells.remove((segment.x, segment.y))
			except ValueError:
				pass
		self.food = random.choice(list(set(Snake.cells)-set(Snake.foodPos)))
		Snake.foodPos.append(self.food)
		#Snake.cells.remove(self.food)

	def eaten(self,newHeadPos):
		if self.food == newHeadPos:
			Snake.foodPos.remove(self.food)
			#Snake.cells.append(self.food)
			self.food = random.choice(list(set(Snake.cells)-set(Snake.foodPos)))
			#Snake.cells.remove(self.food)
			Snake.foodPos.append(self.food)
			return True

	def move(self):
		self.lastMove = self.direction
		newHeadPos = (int(self.segments[0].x + (self.direction[0]*self.width)),
					  int(self.segments[0].y + (self.direction[1]*self.width)))
		newHead = pygame.Rect(newHeadPos, (self.width, self.width))
		if newHeadPos in Snake.cells or newHeadPos in Snake.foodPos:
			if not self.eaten(newHeadPos):
				Snake.cells.append((self.segments[-1].x, self.segments[-1].y))
				self.segments.pop()
			Snake.cells.remove(newHeadPos)
			self.segments.insert(0, newHead)
		else:
			self.killed = True

	def draw(self, screen):
		#for cell in Snake.cells:
		#	pygame.draw.rect(screen,(0,255,0),pygame.Rect(cell,(int(self.width/2),int(self.width/2))))
		#for food in Snake.foodPos:
		#	pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food, (int(self.width / 2), int(self.width / 2))))
		pygame.draw.rect(screen,self.foodColour,pygame.Rect(self.food,(self.width,self.width)))
		for segment in self.segments:
			pygame.draw.rect(screen, self.colour, segment)

	def handleEvent(self,event):
		if event.type == KEYDOWN:
			if event.key == self.upKey and self.lastMove != (0,1):
				self.direction = (0,-1)
			elif event.key == self.downKey and self.lastMove != (0,-1):
				self.direction = (0,1)
			elif event.key == self.leftKey and self.lastMove != (1,0):
				self.direction = (-1,0)
			elif event.key == self.rightKey and self.lastMove != (-1,0):
				self.direction = (1,0)


class GameOver(State):

	def __init__(self,screen,isTwoPlayer,):
		self.screen = screen
		self.screenWidth,self.screenHeight = self.screen.get_size()
		self.nextState = "gameover"
		self.isTwoPlayer = isTwoPlayer
		self.score = 0
		self.font = pygame.font.Font(None, 40)
		self.textColour = (0,75,0)
		self.backgroundColour = (0,0,0)


	def startup(self,persistentVar):
		self.nextState = "gameover"
		self.screen.fill((0,0,0))
		self.isTwoPlayer = persistentVar[0]
		self.reset = True
		playerNo = 0
		if self.isTwoPlayer:
			playerNo = 2
		else:
			playerNo = 1

		currentPath = os.path.dirname(__file__)
		newPath = os.path.join(currentPath,"..\\High Scores\\highscore{}p.txt".format(playerNo))
		with open(newPath,"rb") as f:
			self.score = pickle.load(f)

		lineText =[self.font.render("Game Over",True, self.textColour),
				   self.font.render("{} Player".format(playerNo), True, self.textColour),
				   self.font.render("Highscore: {}".format(self.score), True, self.textColour),
				   self.font.render("press 'R' to restart", True, self.textColour),
				   self.font.render("or 'ESC' to go to the main menu", True, self.textColour)]

		lineRects = [lineText[0].get_rect(center=(int(self.screenWidth/2),int(self.screenHeight/2 - 100))),
					 lineText[1].get_rect(center=(int(self.screenWidth / 2), int(self.screenHeight / 2 - 60))),
					 lineText[2].get_rect(center=(int(self.screenWidth / 2), int(self.screenHeight / 2 - 20))),
					 lineText[3].get_rect(center=(int(self.screenWidth / 2), int(self.screenHeight / 2 + 80))),
					 lineText[4].get_rect(center=(int(self.screenWidth / 2), int(self.screenHeight / 2 + 120)))]

		for i in range(len(lineText)):
			self.screen.blit(lineText[i],lineRects[i])

	def exit(self):
		return self.isTwoPlayer,self.reset

	def update(self):
		pass

	def getEvent(self,event):
		if event.type == KEYDOWN:
			if event.key == K_r:
				self.nextState = "gameplay"
			elif event.key == K_ESCAPE:
				self.nextState = "menu"

	def draw(self):
		pass
