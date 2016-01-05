import Tkinter as tk
from Tkinter import *
import math
import random
import itertools

TOTAL_COLUMNS=15
TOTAL_ROWS=15
TILE_HEIGHT=60
TILE_WIDTH=60
RACK_TILE_HEIGHT=4
RACK_TILE_WIDTH=7

letters_available =[['A',9] , ['B',2] , ['C',2] , ['D',4] , ['E',12] , ['F',2] , ['G',3] , ['H',2] , ['I',9] , ['J',1] , ['K',1] , 
					['L',4] , ['M',2] , ['N',6] , ['O',8] , ['P',2] , ['Q',1] , ['R',6] , ['S',4] , ['T',6] , ['U',4] , ['V',2] , 
					['W',2] , ['X',1] , ['Y',2] , ['Z',1]]

p1_tiles=[]
selected='a'		#'a' for not selected, CAPS letters otherwise
rack_index=-1

board_tiles=[[-1 for x in range(TOTAL_COLUMNS)] for x in range(TOTAL_ROWS)]		#board_tiles[row][column]
board_letters=[[' ' for x in range(TOTAL_COLUMNS)] for x in range(TOTAL_ROWS)]	#'a' for not selected, CAPS letters otherwise

def findRackTile(widget):				#from Click
	for x in range(len(p1_tiles)):
		if(widget==p1_tiles[x]):
			return x
	return -1

def findBoardTile(widget):				#from Click
	for x in range(TOTAL_COLUMNS):
		for y in range(TOTAL_ROWS):
			if(widget==board_tiles[y][x]):
				return y,x
	return -1,-1

def removeFromArray(i):					#when Rack tile is used
	global p1_tiles
	for x in range(i,len(p1_tiles)-1):
		p1_tiles[x]=p1_tiles[x+1]
	del p1_tiles[-1]

def makeWords():
	rows = (''.join(row) for row in board_letters)
	columns = (''.join(column) for column in zip(*board_letters))
	words = [word for line in itertools.chain(rows,columns) for word in line.split() if len(word) > 1]
	print words

def rack_callback(event):
	global rack_index
	rack_index=findRackTile(event.widget)
	global selected
	if(rack_index==-1):
		print "Tile not in rack! Shouldn't happen"
	else:
		if(p1_tiles[rack_index]["bg"]=="yellow"):
			p1_tiles[rack_index]["bg"]="white"
			selected='a'
		else:
			p1_tiles[rack_index]["bg"]="yellow"
			selected=p1_tiles[rack_index]["text"]

def board_callback(event):
	global board_tiles,board_letters,selected,rack_index,p1_tiles
	r,c=findBoardTile(event.widget)
	if(r==-1 and c==-1):
		print "Tile not in board! How did that happen"
	else:
		if(selected!='a' and board_letters[r][c]==' '):
			board_tiles[r][c]["text"]=selected
			board_tiles[r][c]["bg"]="yellow"
			board_letters[r][c]=selected
			selected='a'
			removeFromArray(rack_index)
			fillPlayerTiles()
			showPlayerTiles()
			makeWords()

def initialiseBoard():
	global board_tiles
	for i in range(TOTAL_COLUMNS):
		for j in range(TOTAL_ROWS):
			board_tiles[j][i]=Label(board_frame,text=" ",relief="raised")			#STANDARD TILE
			board_tiles[j][i].pack()
			board_tiles[j][i].place(x=i*TILE_WIDTH , y=j*TILE_HEIGHT,height=TILE_HEIGHT,width=TILE_WIDTH)
			board_tiles[j][i].bind("<Button-1>",board_callback)

def drawRandomTile():
	temp=[]
	for x in range(len(letters_available)):
		for y in range(letters_available[x][1]):
			temp.append(letters_available[x][0])
	num=random.randrange(0,len(temp),1)
	for x in range(len(letters_available)):
		if(letters_available[x][0]==temp[num]):
			letters_available[x][1]-=1
	return temp[num]

def fillPlayerTiles():
	global p1_tiles
	no_of_total_letters_remaining = 0
	for x in range(len(letters_available)):
		no_of_total_letters_remaining+=letters_available[x][1]
	if(no_of_total_letters_remaining >= 7-len(p1_tiles)):
		while(len(p1_tiles)<7):
			try:
				p1_tiles.append(Label(rack_frame,text=drawRandomTile(),relief="raised",height=RACK_TILE_HEIGHT,width=RACK_TILE_WIDTH,bg="white"))
			except:
				print len(p1_tiles)
	else:
		while(len(p1_tiles)<no_of_total_letters_remaining):
			try:
				p1_tiles.append(Label(rack_frame,text=drawRandomTile(),relief="raised",height=RACK_TILE_HEIGHT,width=RACK_TILE_WIDTH,bg="white"))
			except:
				print len(p1_tiles)

def showPlayerTiles():
	for widget in rack_frame.winfo_children():
		widget.pack_forget()
	for x in range(len(p1_tiles)):
		p1_tiles[x].pack(side="left",padx=5)
		p1_tiles[x].bind("<Button-1>",rack_callback)

if __name__=="__main__":
	window = Tk()
	window.title("SCRABBLE")

	board_frame = Frame(window,height=TOTAL_ROWS*TILE_HEIGHT,width=TOTAL_COLUMNS*TILE_WIDTH)
	board_frame.pack()

	rack_frame = Frame(window,height=TILE_HEIGHT,width=7*TILE_WIDTH)
	rack_frame.pack(pady=10)
	fillPlayerTiles()
	showPlayerTiles()

	initialiseBoard()

	window.mainloop()