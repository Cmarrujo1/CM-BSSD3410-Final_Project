# https://github.com/HarmoniaLeo/Mancala


import pygame
import sys
from mancala_game import MancalaGame
from algorithms import minimax, greedy_move

#screen dimensions
WIDTH, HEIGHT = 800, 400

def main():
    pygame.init()  #initialize pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  #create the game window
    pygame.display.set_caption("Mancala Game")  #set the title of the game window
    clock = pygame.time.Clock()  #create a clock to control the frame rate

    game = MancalaGame(use_minimax=True)  #initialize the Mancala game with Minimax enabled

    while True:  #main game loop
        for event in pygame.event.get():  #process events
            if event.type == pygame.QUIT:  #quit the game if the window is closed
                pygame.quit()  #quit pygame
                sys.exit()  #exit the program

            if event.type == pygame.MOUSEBUTTONDOWN:  #mouse click events
                x, y = event.pos  #position of the mouse click
                game.handle_click(x, y)  #pass click to the game logic

        if game.game_over:  #if the game ends
            print(f"Game over. Winner: {game.winner}") #prints game over and who's the winner
            game.display_winner(screen)
            game.reset()  #reset the game state to start over

        if not game.game_over:  #game is still ongoing
            if game.current_player == 1:
                if game.use_minimax:
                    _, move = minimax(game, 4, True)
                else:
                    move = greedy_move(game)

                if move is not None:
                    game.make_move(move)

        game.render(screen)  #render the game
        clock.tick(30)  #limit the frame


if __name__ == "__main__":
    main()  #run the main function
