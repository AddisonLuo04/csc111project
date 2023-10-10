<a name="br1"></a> 

CSC111 Project: Creating a Simple Chess AI

Erika Liang and Addison Luo

April 3, 2023

Introduction

Chess is a strategic board game with countless strategies and move choices. Chess is played between 2

players on a checkered board with black and white pieces, where they alternate making moves, which can

include moving pieces and capturing pieces. It can either end in a checkmate, where a king is in a position

to be captured with no escape or alternative moves, a stalemate, or a draw. On their ﬁrst moves alone, the

players have 10 diﬀerent moves they can possibly make. After each move, the number of possible moves

increases exponentially. Thus, for a long time, it was believed that the complexities of the game could

never be summarized or understood by chess-playing computer AIs, much less that chess-playing computer

AIs could beat the top human chess players. However, in 1997, in an astounding feat, the chess engine,

”Deep Blue,” beat world champion Garry Kasparov under normal tournament regulations. This was the

ﬁrst time ever that a chess AI had ever achieved this (Wikipedia). Today, the best chess engines in the

world are able to ﬁnd optimal moves, analyze entire move sequences instantaneously, and play with close

to 100% accuracy. Thus, our research question wishes to delve into this complex AI and analyze its inner

workings: How can we create an simple AI for playing chess and evaluate how well it plays?

Libraries and Datasets

The new libraries we will be importing and installing are chess and pygame. chess has several useful

built-in functions that help translate our code into chess moves. It has functions that deal with move

generation, move validation, and extraneous support of for other comparable formats (”Chess”). It also

has the ability to detect wins, stalemates, draws from general repetition. It can also show a simple ASCII

board in order to better visualize game states (”Chess”). We will use also pygame, which is a Python

module that excels in coding and writing games. This library will allow us to create an interactive GUI

that a user can play against the AI with. There is no preexisting data set that we must use as our tree

will be solely generated from moves and move sequences.

Computational Overview

The data used in our project consist of:

• A board representation of an 8x8 black and white matrix

• A piece representation where each piece is represented by a unique code or identiﬁer that indicates

its type (pawn, bishop, knight, rook, queen, or king) and color (white or black).

• Evaluation metrics in terms of scores which determine the strength of a particular board. How these

are computed will be described later under our chess tree functions.

1



<a name="br2"></a> 

In order to create a way to visualize the project, we used display helpers as well pygame in order

to display the game on a traditional chess board. Speciﬁcs of how we did it will be further elaborated

upon under our display helper, main and runner functions. For our project, we have multiple py ﬁles:

display helpers, main, runner, chess engine, and chess tree.

display helpers has 3 functions which help load the display of the chess board through pygame:

• initialize image() initializes the .png images for each piece and is called one time in main

• initialize pygame window() returns a new pygame window of a pre determined size (in our case,

400x400 pixels)

• display board() displays the board and pieces given a speciﬁc position on the board

main has one function and serves as the main ﬁle in our project.

• main() handles user input to create chess engine objects. It then calls other the functions in the

runner to run game(s).

runner has two functions and will be used to run the game.

• run game() takes in white player and black player which correspond to chess engines. This function

runs a chess game between the two engines, or user input depending on what the user decides to run.

• run games() also takes in a white player and black player which are two chess engines. n number

of games are computed and the results are stored in a dictionary and returned. It also prints each

outcome of each individual game.

• run example() runs a single game and is defaulted into using a RandomChessEngine

chess engines is our py ﬁle of all of are diﬀerent engine implementations. We have created 3 classes

of diﬀerent engines.

• ChessEngine is an abstract class that represents a general chess engine. It has one function,

make move() that returns a move to make given the current position of the chess board, though

it isn’t implemented.

• RandomChessEngine is a subclass of ChessEngine and its make move() function make random valid

moves given a board in chess.

• UserInput is a subclass of ChessEngine and its make move() function returns a move given the

current board as well as an user inputted move.

• TreeChessEngine is a subclass of ChessEngine and its make move() function returns a move based

on its associated ChessTree. We will go further into what this class represents, but in short, the

move that is selected is the one that leads to the best eval position, an evaluation of the position.

• GreedyChessEngine is a subclass of ChessEngine and its make move() function returns a move based

the search algorithm in find move by search(). Not utilized as TreeChessEngine is more eﬃcient.

2



<a name="br3"></a> 

Finally, chess tree has one class and eight functions.

• ChessTree is a decision tree for chess moves. It has instance attributes board, eval position, and

subtrees. board is the root board of the tree. eval position is the evaluated score of this board

using piece values and piece tables. subtrees is a dictionary of that maps a fen to a chess tree.

This class has eight functions:

–

init () initializes a new ChessTree with a board and eval position.

– get subtrees is a helper function that returns a dict containing all subtrees of self.

– find subtree by board() is a helper function that returns a subtree based on a given board.

– add subtree() is a helper function that adds a subtree to the current chess tree.

– size() is a helper function that returns the size of the subtree. This was mostly used for testing

how large were the trees we were creating.

– str indented and str () are functions that return string representations of the tree.

• evaluate piece() evaluates a given piece and returns a score indicating the how big of an advantage

this given piece has and has parameters piece and square. A positive score indicates that the piece

is in favour of white while a negative score indicates that the piece is in favour of black. This

implementation uses Michniewski’s piece values in order to evaluate individual piece scores and then

piece tables to evaluate bonus scores for each piece relative to their position. This is because in chess,

the pieces have diﬀerent relative values. The type of piece matters as the queen, for example, is very

valuable because it can control many spaces while the pawn is less valuable. Additionally, position

also plays an important role, as a piece like the knight is more valuable if near the centre of the

board, as it controls more spaces that way. The returned value is the score that the piece generates

using these parameters.

• evaluate board() takes a board and evaluates the given board, returning a score that indicates how

big of an advantage that board provides. First, it checks whether or not the board is checkmated and

returns positive or negative inﬁnity based on the winner. It also checks if the board is a stalemate or

if there is insuﬃcient material for either side to win. In those cases, the score is returned as 0. Then,

using a for loop, we cycle through all of the squares on the board. If there is a piece on the square,

then we call the helper function evaluate piece() and sum it to our total. Finally, we return this

total if the turn is white and the negative total is the turn is black.

• generate chess tree() generates and returns a complete chess tree of depth d for all valid moves

from the current board. As we pointed out in the problem description, generating a complete tree

for chess is computationally infeasible. Thus, we will only generate our trees to a certain depth d. If

the depth is not 0 and the board’s outcome is not None (the base case), depending on whose turn it

is, this function recurses through all legal moves and generates new chess trees to add onto the chess

tree. It also updates the chess trees instance attribute eval position based on whose turn it is. If

it is white, the eval position is maximized and if it is black, the eval position is minimized.

• generate pruned chess tree() is very similar to generate chess tree() and also returns a com-

plete chess tree of depth d for all valid moves from the current board. However, this function takes

in extra parameters alpha and beta which allows the function to prune unwanted subtrees by using

the alpha-beta pruning algorithm. In short, this algorithm works by storing the evaluations of the

”best” subtrees in the alpha and beta variable. It then checks if a subtree can be pruned if there

already exists a ”better” option in a previously explored subtree. This returns a chess tree that is

much smaller and more manageable which allows for greater depths and faster running times. For

the purposes of our chess engines, we will only be using generate pruned chess tree() to compute

trees.

3



<a name="br4"></a> 

• search() is a recursive implementation of the minimax algorithm with alpha-beta pruning for ﬁnding

the best move for a given chess position on the given board. It takes 4 parameters, board, d, alpha,

and beta. d is the depth of the search tree in order to limit the depth of the search and avoid

an inﬁnite recursion. Alpha is a ﬂoat representing the lower bound of the search window for the

alpha-beta pruning while beta represents the upper bound. If the d parameter is 0 or the board

has a result (i.e. checkmate, stalemate, or draw), then the function returns the result of calling

search all captures() to search for all possible captures that follow and see if the true value of the

position after all the captures are made. This is a way to avoid ending the horizon eﬀect, more on

this in the next point. If neither are the case, this function generates all legal moves and evaluates

them recursively using the minimax algorithm while pruning the tree depending on the alpha beta

bounds.

• search all captures() is a helper function used to evaluate all possible captures in a given board.

It takes the parameters board, alpha, and beta which have the same meaning as in search. The

function generates a list of all possible capture moves in the current position and evaluates each of

them recursively. It is used for search as well as generate pruned chess tree() in their base cases

where we want to compute all the possible captures and evaluate the board after all the trades. This

is so we can avoid the horizon eﬀect, where potential captures that are out of range of the search

because they were out of the depth range may happen right after. However, the search would not

know that it was a bad move because it could not see over the ”horizon”. Thus, we compute all

possible captures that can happen after reaching a depth of 0 to see the true value of the board.

• find move by search() ﬁnds the best move for a given board. It takes the parameters board and d

which indicate the given board and depth of the tree. First, it initializes the variable best move eval

to be equal to negative inﬁnity if the turn is white and inﬁnity if the turn is black. This way, the ﬁrst

evaluation will always be better than the original evaluation. Then, it creates a list of legal moves

which it cycles through in order to evaluate each move using search.

• get ordered moves() returns a list of moves, sorted by best to worst move. This is not a compre-

hensive ordering based on what move will lead to the best position but instead, just a sorting based

on the move in a vacuum. Generally, a pawn promoting and a piece of low value capturing a piece

with higher value are good moves. A move that sacriﬁces a piece with high value for something of low

value is generally a bad move. This is useful for the alpha-beta pruning algorithm because generally,

moves that are good will lead to positions that are better. Thus, if we sort the moves from best to

worst, we are more likely to ﬁnd good positions and we are able to prune more subtrees.

In this implementation, trees are extremely important as it provides a way to explore all possible moves

and outcomes in a game of chess. Our AI chess engines use game trees to analyze diﬀerent positions and

evaluate the best moves based on various factors such as the strength of the pieces and the number of

pieces on the board. By using trees to explore all possible moves and outcomes, our AI chess engines

can make informed decisions and choose the best move to play. They also can compute a search up to

a depth of d, and they will not have to create a new search every time the opponent makes a move.

We noticed this in our testing of our implementations of TreeChessEngine and GreedyChessEngine, we

observed that it was TreeChessEngine that was more computationally and time eﬃcient. This is because

GreedyChessEngine uses the search() function and it computed a search every time make move is called.

However, TreeChessEngine has an tree as an instance attribute which means it does not have to recompute

the next moves all the time and instead only needs to regenerate a tree when it reaches the end of the

range of its chess tree.

Discussion

Throughout testing our code, we came across many interesting results from our program.

4



<a name="br5"></a> 

For example, when we run a game between two RandomChessEngines, most of the time, the game ends

in a draw. Very rarely does the RandomChessEngine produce moves that lead to a checkmate, but this is

as expected. Since there are just so many diﬀerent possible moves, choosing very speciﬁc moves to lead to

a checkmate is often too small of a chance. Indeed, if we use the run games() function in runner.py, we

can see that between two RandomChessEngines, the percentage of times that RandomChessEngine found a

checkmate was 7-10%. It turns out that getting a checkmate can happen accidentally at not an absurdly

small chance. However, what barely does happen is a draw by repetition of moves, only occurring in 4/10

000 games that we simulated. This was much lower because of the chance that both the engines randomly

choose the same moves 5 times in a row. Thus, the results of this test align with what we expected, that

the random chess AI would not succeed in winning because of its inability to look ahead into what moves

would give the better position.

Next, we looked at developing a smarter AI that uses a tree of chess moves to search for and select its

move. We ﬁrst made the generate chess tree() function, which made a full tree of all possible moves

in chess up to a certain depth. By using the size() method on the tree, we found out that just after 3

moves, the tree had 8902 nodes. After 4, 197,742 diﬀerent positions. And at this point, we knew that

if we wanted to make an engine which uses a fully generated tree, it would take lots of computational

power just to compute the ﬁrst tree and once we traversed to the depth of where the tree ended, we would

have to create another tree to continue. Thus, to make the computation easier, we needed to be able to

shrink the tree to a more manageable size. This is where we used alpha-beta pruning and minimaxing.

We used many diﬀerent resources to learn about and understand alpha-beta pruning and minimaxing

because it was a crucial step in making the computations easier. In summary, minimaxing is the process

of determining which child node to go into. In this speciﬁc case of chess, White is trying to maximize the

evaluation score of the position while black is trying to minimize the evaluation score. So as we traverse

down the tree, the node that will be chosen will either be the min or max of its sibling nodes (Lague,

2018). Alpha-beta pruning is the process of storing the max/min evaluation score of the subtrees as we

go through each child node (Lague, 2018). If the program ever encounters an evaluation score that is, at

best, still ”worse” than the ”best” subtree, that subtree can be pruned as the program knows it already

has a better option so it doesn’t need to spend computational resources on computing those. However, if

the subtrees are ordered in ”best” to ”worse”, more pruning can occur because the evaluation of subtrees

that are computed earlier would be better and therefore, there can be more pruning of later trees. This

motivated the get ordered moves() function, where we attempt to order the legal moves from best to

worst in a vacuum where we don’t compute any further moves. Indeed, some moves that are ”bad” will

lead to positions that are actually ”good”, so we cannot just use this function to choose the next move.

Thus, after these optimizations, generate pruned chess tree() produced a tree that after 3 moves, had

81 subtrees and after 4, 1277.

We discovered our next problem, for example, let the depth of our ChessTree be 3. Sometimes, the

tree would evaluate the last move in the depth (the third move) as a ”good” move let’s say queen takes

knight, but then the very next turn, (on move 4), the knight was actually defended, so we lost the queen.

This problem is called the horizon eﬀect (Chess Programming Wiki). A way to combat this is to instead

of just returning a static evaluation of the position when depth is 0 in our tree generation, we can return

a value from a diﬀerent function, search all captures(), which as it sounds, gives an evaluation of the

board after all captures are made.

Thus, we completed TreeChessEngine and tested it against a RandomChessEngine. We noticed many

things right away. If we ever set the depth to above 3, TreeChessEngine would take lots of time to

compute its next moves because it had to generate a larger tree. This was to be expected. However,

what we did not expect was that after a depth of around 5, the TreeChessEngine seems to select moves

that repeat themselves, like moving the rook one square to the left and then back one square to the right.

We ﬁgured that the reason for this was because it did not ﬁnd a good move within that depth and just

decided to shuﬄe between 2 decent moves. However, if we set the depth to 3, we did not have this problem.

Another interesting case was in the endgames between the two engines. For many test games between the

5



<a name="br6"></a> 

two, TreeChessEngine would always overwhelming beat RandomChessEngine in the early game, leaving

the RandomChessEngine’s king all by itself. However, because the depth was still at 3, TreeChessEngine

could never ﬁnd a winning sequence of moves that lead to checkmate. Almost all the games resulted in

a draw by repetition of moves. A reason why this might be the case is because we did not implement

a diﬀerent way the engine should behave if the game was in the endgame. If we were to implement an

endgame change, it would be to develop a function that would detect if the game was in the endgame

(check if the king is by itself/with less than n pieces) and a way to force the king to the corner. We decided

that was out of the scope of this project.

Project Modiﬁcations

Our TA had extremely insightful comments, as they have had experience with a chess GUI in the past.

One of their comments was to use matplotlib from the library. In addition, one thing that we were not able

to add were opening and ending tables. These would be tables that include popular chess openings and

endgames that our AI could use. Given the complexity of the code if we were to do that, we ultimately

did not include that function in our project. Something we added to our project that we didn’t plan on

adding but did in the end was an additional tree generator that used alpha-beta pruning to eliminate

certain subtrees (Healey, Building my own chess engine). Though we did not plan to add it, it made sense

to look into it due to the overwhelming size of the trees that we were dealing with.

References

Wikipedia. “Deep Blue versus Garry Kasparov.” Wikipedia, Wikimedia Foundation, 1 Mar. 2023,

https://en.wikipedia.org/wiki/Deep Blue versus Garry Kasparov.

“Chess: A Chess Library for Python.” Python, pythonchess.readthedocs.io/en/latest/.

Dennis, William Wu. “Simple Interactive Chess Gui in Python.” Medium, Dev Genius, 30 Dec. 2022,

blog.devgenius.iosimpleinteractivechessguiinpythonc6d6569f7b6c.

“Getting Started.” Getting Started Chessprogramming Wiki, 18 Dec. 2018,

www.chessprogramming.orgGetting Started.

St¨ockl, Andreas. “Writing a Chess Program in One Day.” Medium, Medium, 24 Apr. 2019,

andreasstckl.medium.comwritingachessprograminoneday30daﬀ4610ec.

Lague, Sebastian. “Algorithms Explained – Minimax and Alpha-Beta Pruning.” YouTube, YouTube,

20 Apr. 2018, https://www.youtube.com/watch?v=l-hh51ncgDI.

Chess Programming Wiki. “Horizon Eﬀect.” Horizon Eﬀect - Chessprogramming Wiki,

https://www.chessprogramming.org/Horizon Eﬀect.

6

