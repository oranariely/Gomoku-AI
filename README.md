Gomoku AI 
Created by Kfir Davda , Rotem Dvir, Oran Ariely and Yochai Cohen

Main Modules:

main.py :
The modules which Responsible for running the program

board_gui.py :
The main gui for the Gomoku game, prints the board
Responsible for the logic of the running flow (switching turns and adding moves)
runs the main loop


board_searcher,py :
Contains the AI agent for the game - the next_move method and the alpha beta function.
The heuristic function included at this module and uses the sequence_counter for evaluating.

game_board.py :
An object representing the Gomoku board, each object contains the current sequences count for black and white players,
the positions of the stones, last move and current turn.

sequence_counter:
The purpose of the class is to count the current sequences in the board using efficient methods and evaluating
the values of those sequences. 
It does that by holding a value for each sequence length and type in a matrix form.



Instruction for running the game:
1. go to board_gui.py module
2. in the start of the file (line 9) you'll see values you can edit
    go a head and change them as you like
3. run the main.py module and wait for the results to appear
4. you can add prints of possible moves values by changing PRINT_MOVES_VALUES constant
    to True in board_searcher.py in line 6
*python 3 is required 


Credit:
 We used the gui of the next code: https://github.com/TongTongX/Gomoku/blob/master/README.md


