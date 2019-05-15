# TIE-02100 Johdatus ohjelmointiin
# Task: Graphical user interface
# Anttoni Tukia, student number: 267137

from tkinter import *
import random


DICEPICS = ["1.gif", "2.gif", "3.gif", "4.gif", "5.gif", "6.gif"]


class Entrywindow:
    """""
    Class asks how many players are playing, and returns the number.
    ......
    """""

    def __init__(self):
        self.__window = Tk()
        self.__window.title("Dice poker for dum dums")

        self.__how_many_text = Label(self.__window,
                                     text="How many players? (max 4)")\
            .grid(row=0, columnspan=3)
        self.__how_many = Entry(self.__window)
        self.__how_many.grid(row=1, columnspan=3)
        self.__go_button = Button(self.__window, text="Enter",
                                  command=self.lets_have_fun)\
            .grid(row=2, columnspan=3)

        self.__in_case_of_error = Label(self.__window)
        self.__in_case_of_error.grid(row=3, columnspan=3)

        self.__players = 0

    def lets_have_fun(self):
        """""
        This method checks if given number is correct or a number at all.
        ....
        """""
        try:

            players = int(self.__how_many.get())

            if 1 <= players <= 4:
                self.__players += players
                self.__in_case_of_error.configure(
                    text="Close current window to have fun :)")

            else:
                self.__in_case_of_error\
                    .configure(text="1-4 players darling :)")
                self.__how_many.delete(0, END)

        except ValueError:
            self.__in_case_of_error.\
                configure(text="U TRYING 2 BREAK MY PROGRAM??!!! >:(")
            self.__how_many.delete(0, END)

    def return_players(self):
        """
        :return: self.__players
        """
        return self.__players

    def start(self):
        self.__window.mainloop()


class Game:
    """""
    The actual game. Some of the code is copied from earlier assignments for 
    practical reasons.
    .....
    """""

    def __init__(self, number_of_players):
        """""
        Object's builder method takes the number of players returned from 
        entry window class and constructs the game based on that.
        ....
        """""
        self.__number_of_players = number_of_players
        self.__mainwindow = Tk()
        self.__mainwindow.title("Dice poker for dum dums")

        # This lis is used to determine which dices are locked.
        # If the equivalent list index is 1, the dice is locked.
        self.__locked_dices = [0, 0, 0, 0, 0]

        # Counters that keeps track whose turn is it and how many attempts
        # players has left.
        self.__turn = 0
        self.__attempts = 1

        # This dict is used to determine the winner, and it's used later in
        # method "check_winner".
        self.__goals_completed = {}

        for i in range(self.__number_of_players):
            are_goals_completed = [False, False, False, False]
            self.__goals_completed[i] = are_goals_completed

        # The list that contains all of the the dice pictures.
        self.__dicepics = []
        for picfile in DICEPICS:
            pic = PhotoImage(file=picfile)
            self.__dicepics.append(pic)

        for i in range(self.__number_of_players):
            Label(self.__mainwindow, text="Player " + str(i + 1) + " score:") \
                .grid(row=i + 5, column=0, sticky=E)

        # This dict contains lists of goal labels. The amount of keys and lists
        # is determined bt the number of players.
        self.__goal_labels = {}
        for i in range(self.__number_of_players):

            # Every players individual "goals completed" list.
            inner_list = []

            for j in range(1, 5):
                goal_label = Label(self.__mainwindow, text="{} same"
                                   .format(1 + j),
                                   background="red", foreground="white")
                goal_label.grid(row=i+5, column=0+j)
                inner_list.append(goal_label)

            self.__goal_labels[i] = inner_list

        # Instead of making separate buttons for locking the dices, dice
        # pictures are buttons.
        self.__dicepicbuttons = []
        for i in range(1, 6):
            new_label = Button(self.__mainwindow,
                               command=lambda number=i - 1:
                               self.change_dice_status(number))
            new_label.grid(row=0, column=0 + i)
            self.__dicepicbuttons.append(new_label)

        # Labels to indicate which dices are locked
        self.__locklabels = []
        for i in range(1, 6):
            new_button = Label(self.__mainwindow)
            new_button.grid(row=1, column=0 + i)
            self.__locklabels.append(new_button)

        # Tells whose turn is it.
        self.__infolabel = Label(self.__mainwindow)
        self.__infolabel. \
            grid(row=self.__number_of_players + 5, column=0, columnspan=2)

        self.__throwButton = Button(self.__mainwindow, text="throw",
                                    command=self.throw)
        self.__throwButton.grid(row=0, column=0, sticky=W + E)

        self.__winner_label = Label(self.__mainwindow)
        self.__winner_label.grid(row=10, column=2, columnspan=3)

        self.__roast_label = Label(self.__mainwindow)
        self.__roast_label.grid(row=11, column=1, columnspan=5)

        self.__gamesituationtext = ""
        self.__dices_in_use = None
        self.__current_dice_score = None

        self.initialize_game()

    def initialize_game(self):
        """
        Method is used for setting the inital state of the game.
        ....
        """
        self.__turn = 0
        self.__gamesituationtext = "Player " + str(self.__turn + 1) + " turn"
        self.__dices_in_use = [True] * 5
        self.__current_dice_score = [1] * 6

        for label in self.__dicepicbuttons:
            label.configure(image=self.__dicepics[0])
        self.set_lockbuttons()
        self.update_ui_texts()

    def update_ui_texts(self):
        """""
        Updates the label that tells whose turns is it.
        ....
        """""
        self.__infolabel.configure(text=self.__gamesituationtext)

    def throw(self):
        """""
        Throws all dices, used when user presses throw button.
        ....
        """""
        first_dice = 0
        second_dice = 0
        third_dice = 0
        fourth_dice = 0
        fifth_dice = 0
        if self.__locked_dices[0] == 0:
            first_dice += random.randint(1, 6)
        if self.__locked_dices[1] == 0:
            second_dice += random.randint(1, 6)
        if self.__locked_dices[2] == 0:
            third_dice += random.randint(1, 6)
        if self.__locked_dices[3] == 0:
            fourth_dice += random.randint(1, 6)
        if self.__locked_dices[4] == 0:
            fifth_dice += random.randint(1, 6)

        # This loop is used for updating dice pictures depending on what
        # numbers "random number generators" giv
        for i in range(1, 7):
            if first_dice == i:
                self.__current_dice_score[0] = first_dice
                self.__dicepicbuttons[0] \
                    .configure(image=self.__dicepics[i - 1])
            if second_dice == i:
                self.__current_dice_score[1] = second_dice
                self.__dicepicbuttons[1] \
                    .configure(image=self.__dicepics[i - 1])
            if third_dice == i:
                self.__current_dice_score[2] = third_dice
                self.__dicepicbuttons[2] \
                    .configure(image=self.__dicepics[i - 1])
            if fourth_dice == i:
                self.__current_dice_score[3] = fourth_dice
                self.__dicepicbuttons[3] \
                    .configure(image=self.__dicepics[i - 1])
            if fifth_dice == i:
                self.__current_dice_score[4] = fifth_dice
                self.__dicepicbuttons[4] \
                    .configure(image=self.__dicepics[i - 1])

        # Resets attempts when the turn changes.
        if self.__attempts == 2:
            self.__attempts -= 1

            # Resets turns when round is finished.
            if self.__turn == self.__number_of_players - 1:
                self.__turn -= self.__number_of_players - 1

            else:
                self.__turn += 1

            # Check goal if player has used his/hers both attempts.
            self.check_goals()
        else:
            self.__attempts += 1
        self.__gamesituationtext = "Player " + str(
            self.__turn + 1) + " turn"

        # Update whose turn is it.
        self.update_ui_texts()

        # Reset all locked buttons to unlocked,
        # after player has used both of his/hers attempts.
        self.set_lockbuttons()

    def check_goals(self):
        """""
        Checks if player has completed a goal after his/hers second attempt and 
        changes correct goal label to green.
        ....
        """""
        same = 0
        # Creates a list, where current dice scores are kept temporarily,
        # current_dice_score[i] excluded.
        for i in range(0, 5):
            temp_dice_score_list = []

            for j in range(0, 5):
                temp_dice_score_list.append(self.__current_dice_score[j])

            temp_dice_score_list.remove(self.__current_dice_score[i])

            if self.__current_dice_score[i] in temp_dice_score_list:
                same += 1

            # The list needs to be cleared before the next time.
            temp_dice_score_list.clear()

        # If a goal was completed.
        if same > 0:

            # This if-statement is used for fixing the error that occurs if
            # it's players 1:s turn.
            if self.__turn == 0:
                self.__goal_labels[self.__number_of_players - 1][same - 2]\
                    .configure(text="GOLANZO", background="green")
                self.__goals_completed[self.__number_of_players - 1][same - 2]\
                    = True

            else:
                self.__goal_labels[self.__turn - 1][same - 2]\
                    .configure(text="GOLANZO", background="green")
                self.__goals_completed[self.__turn - 1][same - 2] = True
            self.check_winner()

    def check_winner(self):
        """
        Checks if someone has completed all of the goals.
        ....
        """
        for i in self.__goals_completed:

            # If all list indexes are true, meaning all goal are completed,
            # declare winner.
            if False not in self.__goals_completed[i]:

                # This if-statement is used for fixing the error that occurs if
                # it's players 1:s turn.
                if self.__turn == 0:
                    self.__winner_label\
                        .configure(text="Player {} is the winner!"
                                   .format(self.__number_of_players))
                else:
                    self.__winner_label\
                        .configure(text="Player {} is the winner!"
                                   .format(self.__turn))

                self.__roast_label\
                    .configure(text="You wankers actually"
                         + " wasted your time playing this?")
                self.__throwButton.configure(state=DISABLED)

    def set_lockbuttons(self):
        """
        Resets lock labels after the turn changes and disables lock buttons
        before one's first throw or sets the state of lock buttons to normal
        before one's second throw.
        ....
        """
        if self.__attempts == 1:

            for button in self.__dicepicbuttons:
                button.configure(state=DISABLED)

            for i in range(0, 5):

                if self.__locked_dices[i] == 1:
                    self.__locked_dices[i] -= 1

                self.__locklabels[i].configure(text="")

        if self.__attempts == 2:

            for button in self.__dicepicbuttons:
                button.configure(state=NORMAL)

    def change_dice_status(self, number):
        """
        Changes the text under the chosen dice.
        :param number:
        ....
        """
        if self.__locked_dices[number] == 0:
            self.__locklabels[number]\
                .configure(text="locked", foreground="red")
            self.__locked_dices[number] += 1

        else:
            self.__locklabels[number].configure(text="")
            self.__locked_dices[number] -= 1

    def start_game(self):
        self.__mainwindow.mainloop()


def main():
    players = 0
    ui_1 = Entrywindow()
    ui_1.start()
    players += ui_1.return_players()
    if players > 0:
        ui = Game(players)
        ui.start_game()


main()

