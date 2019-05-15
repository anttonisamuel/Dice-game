# Game rules

This game is a very simplified version of poker. It uses dices and it has less 
possible win scenarios than poker.

Player has to score 4 different outcomes to win:

1. One pair 
2. Three of a kind
3. Four a kind/two pairs
4. Five of a kind/full house

Two pairs counts as four of a kind and full house counts as five of a kind,
for sake of not having to play the game for an hour just to get a win scenario
(or the lad who programmed it is lazy, you decide).

You can also lock dices after your first throw, like in poker; you first get
dealt with something, then you can keep of the card and swap some of them.

# How does it work?

The first object is just a simple entry window. It asks how many players are 
playing and returns it to the main function. Then it asks the user to to close
the entry window (it doesn't open the game automatically after pressing enter
because of my stupidity) and then starts the actual game. 

The game scales depending on how many players are playing. The game is
played until one on the players completes all "goals". After that, the 
program declares the winner and disables the throw button. 

# What I learned?

- Design and implements simple GUI's with Python
- Object oriented programming
