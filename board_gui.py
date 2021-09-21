import os
import tkinter as tk

from game_board import GameBoard
from board_searcher import AlphaBetaAgent

SYM = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E']

'''Section for edit the game'''
ATTACK_VALUE = 1.5
DEFENCE_VALUE = 1.5
DEPTH_AGENT_1 = 1
DEPTH_AGENT_2 = 1
NUMBER_OF_GAMES = 1



class BoardCanvas:
	"""Apply the tkinter Canvas Widget to plot the game board and stones."""
	
	def __init__(self):
		

		self.gameBoard = GameBoard()
		self.boardSearcher = AlphaBetaAgent()
		self.boardSearcher.board = self.gameBoard.board
		self.turn = 2
		self.undo = False
		self.depth = 1
		self.prev_exist = False
		self.prev_row = 0
		self.prev_col = 0
		self.winner =False
		self.winner_1_2 = -1


	def gameLoop(self):
		"""The main loop of the game. 
		Note: The game is played on a tkinter window. However, there is some quite useful information 
			printed onto the terminal such as the simple visualizaiton of the board after each turn,
			messages indicating which step the user reaches at, and the game over message. The user
			does not need to look at what shows up on the terminal. 
		
		self.gameBoard.board()[row][col] == 1(black stone) / 2(white stone)
		self.gameBoard.check() == 1(black wins) / 2(white wins)
		
		Args:
			event (the position the user clicks on using a mouse)
		"""

		agent1 = AlphaBetaAgent(depth=DEPTH_AGENT_1)
		agent2 = AlphaBetaAgent(depth=DEPTH_AGENT_2)
		self.winner = False

		while True:
			# START START START START START START START START START START START START
			# Change the turn to the program now

			self.turn = 1
			print('Program is thinking for black now...')

			# Determine the position the program will place a white stone on.
			# Place a white stone after determining the position.

			row, col = agent1.get_action(self.gameBoard, self.turn)
			if row == -1:
				self.winner_1_2 = 0
				print('TIE')

				return 0

			print('Program has moved to ', SYM[row] + SYM[col])  # {}\n'.format(coord))
			self.gameBoard.apply_action((row, col), 1)
			if self.prev_exist == False:
				self.prev_exist = True

			self.prev_row, self.prev_col = row, col
			self.gameBoard.show()
			print('\n')


			# If the program wins the game, end the game and unbind.
			if self.gameBoard.check(row, col) == 1:
				print('BLACK WINS.')
				self.winner_1_2 = 1

				self.winner = True

				return 0

			# END END END END END END END END END END END END END END END END END

			# Change the turn to the program now
			self.turn = 2
			print('Program is thinking for white now...')

			# Determine the position the program will place a white stone on.
			# Place a white stone after determining the position.
			row, col = agent2.get_action(self.gameBoard, self.turn)
			if row == -1:
				print('TIE')
				self.winner_1_2 = 0

				self.winner = True

				return 0

			print('Program has moved to ', SYM[row] + ',' + SYM[col])

			self.gameBoard.apply_action((row, col), 2)
			if self.prev_exist == False:
				self.prev_exist = True

			self.prev_row, self.prev_col = row, col
			self.gameBoard.show()
			print('\n')


			if self.gameBoard.check(row, col) == 2:
				print('WHITE WINS.')
				self.winner_1_2 = 2

				self.winner = True
				return 0



class BoardFrame():
	"""The Frame Widget is mainly used as a geometry master for other widgets, or to
	provide padding between other widgets.
	"""
	
	def __init__(self):
		self.create_widgets()

	def create_widgets(self):
		attack = [ATTACK_VALUE]
		defence = [DEFENCE_VALUE]


		for a in attack:
			for d in defence:
				if a == d:

					GameBoard.ATTACK_WEIGHTS = a
					GameBoard.DEFENCE_WEIGHTS = d

					self.boardCanvas = BoardCanvas()

					games = dict()
					black_wins = 0
					white_wins = 0
					ties = 0

					num_games = NUMBER_OF_GAMES

					for i in range(num_games):
						self.boardCanvas = BoardCanvas()

						while not self.boardCanvas.winner:
							self.boardCanvas.gameLoop()
							if self.boardCanvas.winner_1_2 == 0:
								ties += 1
								games[i] = ("tie", self.boardCanvas.gameBoard.move_counter)
							elif self.boardCanvas.winner_1_2 == 1:
								black_wins += 1
								games[i] = ("black", self.boardCanvas.gameBoard.move_counter)
							elif self.boardCanvas.winner_1_2 == 2:
								white_wins += 1
								games[i] = ("white", self.boardCanvas.gameBoard.move_counter)

					print("there where " + str(black_wins) + " wins for black, " + str(white_wins) + " wins for white and " + str(ties) +  " ties" + os.linesep)
