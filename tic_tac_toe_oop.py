

from os import system, name 
import random


class board:

	def __init__(self):

		# Define board
		self.placeholder_text = " "
		self.board = []
		self.reset_board()

	def reset_board(self):
		self.board = [self.placeholder_text for i in range(9)]


	def print_board(self):

		str = """

| {} | {} | {} |
 --- --- --- 
| {} | {} | {} |
 --- --- --- 
| {} | {} | {} |


		""".format(*self.board)

		print(str)


	def place_symbol(self, index, symbol, verbose = True):
		if self.board[index] == self.placeholder_text:
			self.board[index] = symbol
			return True
		else:
			if verbose:
				print("This space is taken. Please enter another number. ")
			return False



class game:

	def __init__(self, p1, p2, board, visible = True):

		self.visible = visible
		self.game_over = False
		self.is_winner = False
		self.winner = None
		self.board = board
		self.p1 = p1
		self.p2 = p2
		self.current_player = self.p1
		self.games_played = 0

		# Welcome message
		if self.visible:
			print("Welcome to a game of Tic Tac Toe! Press 'q' to quit or 'h' for help.")
			self.board.print_board()


	def restart_game(self):
		self.game_over = False
		self.is_winner = False
		self.winner = None
		self.board.reset_board()
		self.current_player = self.p1
		self.games_played += 1

		print("Restarting game")
		self.play()


	def clear(self):
		# for windows
		if name == 'nt':
			_ = system('cls')

		# for mac and linux(here, os.name is 'posix')
		else:
			_ = system('clear')

	def print_help(self):

		help_txt = """
You are now playing a game of Tic Tac Toe.
The 3x3 grid is numerated like the numpad at a phone: 1 is at the top left and 9 is at the bottom right, like this: \n 

| 1 | 2 | 3 |
 --- --- --- 
| 4 | 5 | 6 |
 --- --- --- 
| 7 | 8 | 9 | \n

Choose a number to place your symbol. 
The first player to get three in a row - either horizontally, vertically or diagonally - wins.
If the board is full and nobody won yet, then it's a tie. 
		"""

		self.clear()
		print(help_txt)
		input("Press 'enter' to go back to the game.")
		self.clear()
		self.board.print_board()
		#self.play()

	def check_winner(self):

		current_board = self.board.board

		row1 = (current_board[0] == current_board[1] == current_board[2]) and self.board.placeholder_text not in current_board[0:2]
		row2 = (current_board[3] == current_board[4] == current_board[5]) and self.board.placeholder_text not in current_board[3:5]
		row3 = (current_board[6] == current_board[7] == current_board[8]) and self.board.placeholder_text not in current_board[6:8]
		col1 = (current_board[0] == current_board[3] == current_board[6]) and self.board.placeholder_text not in current_board[0:9:3]
		col2 = (current_board[1] == current_board[4] == current_board[7]) and self.board.placeholder_text not in current_board[1:9:3]
		col3 = (current_board[2] == current_board[5] == current_board[8]) and self.board.placeholder_text not in current_board[2:9:3]
		diagonal1 = (current_board[0] == current_board[4] == current_board[8]) and current_board[4] != self.board.placeholder_text
		diagonal2 = (current_board[2] == current_board[4] == current_board[6]) and current_board[4] != self.board.placeholder_text

		# Check if there's a winner
		self.is_winner = row1 or row2 or row3 or col1 or col2 or col3 or diagonal1 or diagonal2
		self.winner = self.current_player
	
		if self.is_winner:
			
			self.game_over = True

			if self.visible:
				print(self.current_player.symbol + " won! Congratulations!")
				print()
			

		elif self.board.placeholder_text not in current_board:

			self.game_over = True
			
			if self.visible:
				print("Board is full. It's a tie.")
				print()

		else:
			# Change player's turn
			if self.current_player == self.p1:
				self.current_player = self.p2
			else:
				self.current_player = self.p1

		if self.game_over:
			self.give_reward()
			#self.restart_game()



	def give_reward(self):

		if self.winner == self.p1:
			self.p1.feed_reward(10)
			self.p2.feed_reward(-10) 

		elif self.winner == self.p2:
			self.p1.feed_reward(-10)
			self.p2.feed_reward(10)
		else:
			# Draw is better for p2, as p1 has a higher prob of winning
			self.p1.feed_reward(0)
			self.p2.feed_reward(5)

			
	def quit_game(self):
		print("Goodbye!")
		self.game_over = True
		quit()


	def play(self):

		while not self.game_over:

			if self.visible:
				print(self.current_player.symbol + "'s turn!")

			move_finished = False

			while not move_finished:

				choice = self.current_player.choose_move(board = self.board.board, free_pos_txt = self.board.placeholder_text)

				# Quit if input is "q"
				if choice == "q":
					self.quit_game()

				# Provide help if input is "h"
				elif choice == "h":
					self.print_help()
					continue

				# Check that input is valid
				elif choice not in [str(i) for i in range(1,10)]:
					print("'" + choice + "'" + " is invalid. Please enter a number between 1 and 9.")
					continue

				# Input is a valid move, continue with game logic
				else:
					# Set the choice to the same indexing as the board
					choice_board_index = int(choice) -1

					move_finished = self.board.place_symbol(choice_board_index, self.current_player.symbol, verbose = self.current_player.type == "human")


			if self.visible:
				self.clear()
				self.board.print_board()
			self.check_winner()



class human_player:

	def __init__(self, symbol = "x"):
		self.symbol = symbol
		self.type = "human"

	def choose_move(self, board = None, free_pos_txt = None):
		# board and free_pos_txt are inputs for the AI player, but is not used for the human
		choice = input("Enter your move (1-9): ").strip().lower()
		return choice

	def feed_reward(self, reward):
		pass




class ai_player:

	def __init__(self, symbol = "y", er = 0.1, lr = 0.8, discount_factor = 0.95):
		self.symbol = symbol
		self.type = "machine"
		self.explore_rate = er
		self.states = []
		self.states_value = {}
		self.lr = lr # Learning rate
		self.discount_factor = discount_factor


	def get_possible_moves(self, board, free_pos_txt):
		return [i+1 for i, x in enumerate(board) if x == free_pos_txt]

	def choose_move(self, board, free_pos_txt):

		current_board = board.copy()
		possible_moves = self.get_possible_moves(current_board, free_pos_txt)

		if random.uniform(0, 1) < self.explore_rate:
			
			choice = random.choice(possible_moves) # random choice from possible_moves
		
		else:
			
			value_max = -999

			for move in possible_moves:

				next_board = current_board.copy()
				next_board[move-1] = self.symbol
				hash_next_board = "".join(next_board)
				value = 0 if self.states_value.get(hash_next_board) is None else self.states_value.get(hash_next_board)
			if value > value_max:
				value_max = value
				choice = move			
		
		# Hash next board
		next_board = current_board.copy()
		next_board[choice -1] = self.symbol
		hash_next_board = "".join(next_board)
		self.states.append(hash_next_board)

		choice = str(choice)
		return choice

	def feed_reward(self, reward):
		for state in reversed(self.states):
			if self.states_value.get(state) is None:
				self.states_value[state] = 0

			self.states_value[state] += self.lr * (self.discount_factor * reward - self.states_value[state])

			reward = self.states_value[state]








# Start game! 	

iterations = 10000

p1 = ai_player(symbol = "x", er = 1)
p2 = ai_player(er = 1) 

print("Training the AI:")

for i in range(iterations):

	if i % 100 == 0:
		print(str(i).rjust(len(str(iterations))) + "/" + str(iterations))


	er = 1 - (i / iterations)
	if er > 0.9:
		er = 1

	if er < 0.1:
		er = 0.1

	p1.explore_rate = er
	p2.explore_rate = er

	tic_tac_toe = game(p1, p2, board(), visible = False)

	tic_tac_toe.play()


tic_tac_toe.clear()

print("Player 1's states:")

for key in p1.states_value:
	print(key, '->', p1.states_value[key])


print("Player 2's states:")
for key in p2.states_value:
	print(key, '->', p2.states_value[key])



play_again = True

while play_again:
	tic_tac_toe = game(human_player(), p2, board())
	tic_tac_toe.play()
	play_again = input("Play again [y/n]: ") == "y"




