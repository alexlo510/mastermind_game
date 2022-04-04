# Alex Lo
# CS325 Homework 6

import random


class MasterMind:
    """Represents a mastermind game."""

    def __init__(self):
        self._game_state = "UNFINISHED"
        self._game_board = Board()
        self._round = 0
        self._piece_colors = ["blue", "green", "orange", "red", "yellow", "white"]
        self._code = []
        for i in range(0, 4):
            self._code.append(random.choice(self._piece_colors))

    def get_game_state(self):
        """Returns the game state"""
        return self._game_state

    def print_board(self):
        """Prints the board."""
        self._game_board.display_board()

    def make_guess(self, guess):
        """Takes in a guess as a list."""
        if self._game_state != "UNFINISHED":
            print("Game is finished.")
            return

        if type(guess) is not list:
            print("Please enter your guess as a list of four colors.")

        if len(guess) != 4:
            print("Please enter four colors")

        if len(guess) == 4:
            for color in guess:
                if color.lower() not in self._piece_colors:
                    print("Please enter four valid colors. Either blue, green, orange, red, yellow, or white")
                    return
            self._game_board.set_board(self._round, guess)
            win = self.check_win(self._round)
            self._round += 1
            if win is True:
                self._game_state = "WON"
                self._game_board.display_board()
                print("You guess it!. The code was", self._code)
            else:
                self._game_board.display_board()
                print("Incorrect. You have", 8 - self._round, "guesses left.")
                if self._round > 7:
                    self._game_state = "LOSS"
                    print("You loss. The code was", self._code)
            return self._game_board.get_keypeg_index(self._round - 1)

    def check_win(self, index):
        # first check if the colors are in the correct spot:
        copy_of_code = self._code.copy()
        copy_of_guess = self._game_board.get_board_index(index).copy()
        for i in range(0, 4):
            if self._code[i] == self._game_board.get_board_index(index)[i]:
                self._game_board.set_keypeg(index, "B")
                copy_of_code.remove(self._game_board.get_board_index(index)[i])
                copy_of_guess.remove(self._game_board.get_board_index(index)[i])

        # next check to see if the colors in the code are in the guess
        for i in range(len(copy_of_code)):
            if copy_of_code[i] in copy_of_guess:
                self._game_board.set_keypeg(index, "W")
                copy_of_guess.remove(copy_of_code[i])

        # check keypegs for win
        if len(self._game_board.get_keypeg_index(index)[3]) != 0:
            if self._game_board.get_keypeg_index(index)[0] == "B" and \
                    self._game_board.get_keypeg_index(index)[1] == "B" and \
                    self._game_board.get_keypeg_index(index)[2] == "B" and \
                    self._game_board.get_keypeg_index(index)[3] == "B":
                return True
        else:
            return False


class Board:
    """Represents the game board."""

    def __init__(self):
        self._board = [[[], [], [], []] for columns in range(0, 8)]
        self._keypeg = [[[], [], [], []] for columns in range(0, 8)]

    def display_board(self):
        """Prints the board."""
        for i in range(7, -1, -1):
            if i == 7:
                print("Board:" + "                 " + "Keypegs:")
            print(self._board[i], end="     ")
            print(self._keypeg[i])

    def set_board(self, index, guess):
        for i in range(0, 4):
            self._board[index][i] = guess[i].lower()

    def set_keypeg(self, index, key_peg_color):
        for i in range(0, 4):
            if len(self._keypeg[index][i]) == 0:
                self._keypeg[index][i] = key_peg_color
                break

    def get_board_index(self, index):
        return self._board[index]

    def get_keypeg_index(self, index):
        return self._keypeg[index]


if __name__ == "__main__":
    game = MasterMind()
    print("Game Rules: Guess the colors of the four pegs in 8 guesses. The colors to choose from are: blue, green, \n" 
          "orange, red, yellow, or white. There will be four keypegs that indicate how correct your guess is. \n"
          "A black keypeg denotes a correct color and position, a white keypeg denotes a correct color but a wrong \n"
          "position You can have multiples of the same color in the pegs. Enter your four color guesses in the \n"
          "prompt with a comma and space between each color guess. Example of a guess: blue, yellow, white, red.")
    game.print_board()
    while game.get_game_state() == "UNFINISHED":
        user_guess_list = []
        user_guess = input("Enter your guess: ")
        if user_guess.lower() == "end":
            print("Ending Game")
            break
        user_guess = user_guess.split(", ")
        print("Your guess was", user_guess)
        game.make_guess(user_guess)
