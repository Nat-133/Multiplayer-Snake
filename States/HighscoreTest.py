import os
import pickle
playerNo = 1
currentPath = os.path.dirname(__file__)

newPath = os.path.relpath("\\High Scores\\highscore{}p.txt".format(playerNo),currentPath)
with open("..\\High Scores\\highscore{}p.txt".format(playerNo),"wb") as f:
    highscore = pickle.dump(f)
print(highscore)


#print(os.path.relpath("..\\High Scores"),os.path.dirname(__file__))
#print(os.path.relpath("..\\High Scores\\highscore{}p.txt".format(playerNo),currentPath))
#>>>..\High Scores\highscore1p.txt
print(os.pardir)
print(currentPath)
print(newPath)
