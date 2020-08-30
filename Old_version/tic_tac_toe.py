
from os import system, name 

# Define board
placeholder_text = " "
board = [placeholder_text for i in range(9)]


# Define help text
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

# Make function to print the board
def print_board():
	row1 = "| {} | {} | {} |".format(board[0], board[1], board[2])
	row2 = "| {} | {} | {} |".format(board[3], board[4], board[5])
	row3 = "| {} | {} | {} |".format(board[6], board[7], board[8])

	hline = " --- --- --- "

	print()
	print(row1)
	print(hline)
	print(row2)
	print(hline)
	print(row3)
	print()

def check_winner():
	row1 = (board[0] == board[1] == board[2]) and placeholder_text not in board[0:2]
	row2 = (board[3] == board[4] == board[5]) and placeholder_text not in board[3:5]
	row3 = (board[6] == board[7] == board[8]) and placeholder_text not in board[6:8]

	col1 = (board[0] == board[3] == board[6]) and placeholder_text not in board[0:9:3]
	col2 = (board[1] == board[4] == board[7]) and placeholder_text not in board[1:9:3]
	col3 = (board[2] == board[5] == board[8]) and placeholder_text not in board[2:9:3]
	diagonal1 = (board[0] == board[4] == board[8]) and board[4] != placeholder_text
	diagonal2 = (board[2] == board[4] == board[6]) and board[4] != placeholder_text

	return row1 or row2 or row3 or col1 or col2 or col3 or diagonal1 or diagonal2


def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


player = "x"

# Welcome message
print("Welcome to a game of Tic Tac Toe! Press 'q' to quit or 'h' for help.")
print_board()

# The "game loop"
while True:

	print(player + "'s turn!")

	# Ask for move as input
	choice = input("Enter your move (1-9): ").strip().lower()

	# Quit if input is "q"
	if choice == "q":
		print("Goodbye!")
		break

	# Provide help if input is "h"
	elif choice == "h":
		clear()
		print(help_txt)
		input("Press 'enter' to go back to the game.")
		clear()
		print_board()
		continue

	# Check that input is valid
	elif choice not in [str(i) for i in range(1,10)]:
		print("'" + choice + "'" + " is invalid. Please enter a number between 1 and 9.")
		continue
	
	# Input is a valid move, continue with game logic
	else:
		# Set the choice to the same indexing as the board
		choice_board_index = int(choice) -1

		# Check that chosen space is empty
		if board[choice_board_index] == placeholder_text:
			board[choice_board_index] = player
			clear()
			print_board()
		else:
			print("This space is taken. Please enter another number. ")
			continue

	# Roundup game

	# Check if there's a winner
	is_winner = check_winner()

	if is_winner:
		print(player + " won! Congratulations!")
		print()
		break

	if placeholder_text not in board:
		print("Board is full. It's a tie.")
		print()
		break

	# Change player's turn
	if player == "x":
		player = "o"
	else:
		player = "x"






