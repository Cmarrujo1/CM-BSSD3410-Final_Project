import pygame
import math

#constants
WIDTH, HEIGHT = 800, 400
PIT_RADIUS = 40
BIG_PIT_RADIUS = 60
BOARD_MARGIN = 80
CENTER_START = BIG_PIT_RADIUS * 2 + 40

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREY = (169, 169, 169)
GREEN = (0, 200, 0)

class MancalaGame:
    def __init__(self, stones_per_pit=4, use_minimax=True):
        self.stones_per_pit = stones_per_pit  #number of stones in each pit at the start
        self.pits = [self.stones_per_pit] * 6 + [0] + [self.stones_per_pit] * 6 + [0]  #initial state of the board
        self.current_player = 0  #player 0 starts first
        self.game_over = False  #flag to check if the game is over
        self.use_minimax = use_minimax  #determines if Minimax is used

    def render(self, screen):
        screen.fill(WHITE)  #background

        for i in range(6):  #draw player 1's & player 2's pits
            pit_x = CENTER_START + i * (PIT_RADIUS * 2 + 20)  #x-position
            pit_y = HEIGHT - BOARD_MARGIN - PIT_RADIUS * 2  #y-position
            pygame.draw.circle(screen, BROWN, (pit_x, pit_y), PIT_RADIUS)  #draw the pit
            self.draw_stones(screen, pit_x, pit_y, self.pits[i])  #draw stones in the pit

            pit_y = BOARD_MARGIN + PIT_RADIUS * 2  #update y-position
            pygame.draw.circle(screen, BROWN, (pit_x, pit_y), PIT_RADIUS)  #draw the pit
            self.draw_stones(screen, pit_x, pit_y, self.pits[i + 7])  #draw stones in the pit

        pygame.draw.circle(screen, GREY, (BOARD_MARGIN, HEIGHT // 2), BIG_PIT_RADIUS)
        self.draw_stones(screen, BOARD_MARGIN, HEIGHT // 2, self.pits[6])

        pygame.draw.circle(screen, GREY, (WIDTH - BOARD_MARGIN + 20, HEIGHT // 2), BIG_PIT_RADIUS)
        self.draw_stones(screen, WIDTH - BOARD_MARGIN + 20, HEIGHT // 2, self.pits[13])

        #display the scores
        font = pygame.font.SysFont("Arial", 24)
        player1_score = self.pits[6]  #score for player 1
        player2_score = self.pits[13]  #score for player 2
        score_text = font.render(f"Player 1: {player1_score} | Player 2: {player2_score}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT - 70))

        #draw the restart button
        restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 30)  #position the button
        pygame.draw.rect(screen, GREEN, restart_button)  #draw the button
        restart_text = font.render("Restart", True, WHITE)  #text for the button
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 35))  #render button text

        #display winner if game is over
        if self.game_over:
            font = pygame.font.SysFont("Arial", 32)
            player1_score = self.pits[6]  #final score for player 1
            player2_score = self.pits[13]  #final score for player 2
            if player1_score > player2_score:
                winner_text = f"Game Over! Winner: Player 1 with {player1_score} stones"
            elif player2_score > player1_score:
                winner_text = f"Game Over! Winner: Player 2 with {player2_score} stones"
            else:
                winner_text = f"Game Over! It's a Tie! Player 1: {player1_score}, Player 2: {player2_score}"
            winner_message = font.render(winner_text, True, BLACK)  #render winner message
            screen.blit(winner_message, (WIDTH // 2 - winner_message.get_width() // 2, 20))  #display the message

        pygame.display.flip()  #update the display

    def draw_stones(self, screen, x, y, count):
        angle_step = 360 // max(1, count)  #determine spacing for stones
        for i in range(count):  #draw each stone
            angle = math.radians(i * angle_step)  #calculate angle
            offset_x = int(PIT_RADIUS * 0.6 * math.cos(angle))
            offset_y = int(PIT_RADIUS * 0.6 * math.sin(angle))
            pygame.draw.circle(screen, BLACK, (x + offset_x, y + offset_y), 5)  #draw the stone

    def make_move(self, pit_index):
        stones = self.pits[pit_index]  #number of stones in selected pit
        if stones == 0 or (self.current_player == 0 and pit_index > 5) or (self.current_player == 1 and pit_index < 7):
            return False  #invalid move if the pit is empty

        self.pits[pit_index] = 0  #remove stones from the selected pit
        index = pit_index
        while stones > 0:  #distribute stones to other pits
            index = (index - 1) % 14
            if (self.current_player == 0 and index == 13) or (self.current_player == 1 and index == 6):
                continue  #skip opponent's
            self.pits[index] += 1  #add a stone to the current pit
            stones -= 1

        if (self.current_player == 0 and index == 6) or (self.current_player == 1 and index == 13):
            return True  #extra turn if the last stone lands in the player's

        if self.pits[index] == 1:  #capture rule
            if self.current_player == 0 and 0 <= index <= 5:
                opposite_index = 12 - index  #opposite pit for player 1
                self.pits[6] += self.pits[index] + self.pits[opposite_index]  #capture stones
                self.pits[index] = 0  #empty the pit
                self.pits[opposite_index] = 0  #empty the opposite pit
            elif self.current_player == 1 and 7 <= index <= 12:
                opposite_index = 12 - index  #opposite pit for Player 2
                self.pits[13] += self.pits[index] + self.pits[opposite_index]  #capture stones
                self.pits[index] = 0  #empty the pit
                self.pits[opposite_index] = 0  #empty the opposite pit

        self.current_player = 1 - self.current_player  #switch turns
        self.check_game_over()  #check if the game is over
        return True  #move successful

    def handle_click(self, x, y):
        print(f"Mouse clicked at: ({x}, {y})")

        restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 30)
        if restart_button.collidepoint(x, y):
           print("Restart button clicked. Resetting game.")
           self.reset()  #reset the game
           return

        if self.game_over:
            print("Game is over. Click ignored.")
            return

        for i in range(6):
            pit_x = CENTER_START + i * (PIT_RADIUS * 2 + 20)  #x-position of the pit
            pit_y = HEIGHT - BOARD_MARGIN - PIT_RADIUS * 2  #y-position of the pit
            if (x - pit_x) ** 2 + (y - pit_y) ** 2 <= PIT_RADIUS ** 2:  #check if click is inside the pit
                print(f"Player clicked on pit {i}.")
                if self.current_player == 0:  #ensure it's player 1's turn
                    if not self.make_move(i):  #attempt to make the move
                        print(f"Invalid move on pit {i}.")
                return

    def check_game_over(self):
        if sum(self.pits[:6]) == 0 or sum(self.pits[7:13]) == 0:  #one side is empty
            self.game_over = True  #mark the game as over
            self.pits[6] += sum(self.pits[:6])  #add remaining stones to player 1's
            self.pits[13] += sum(self.pits[7:13])  #add remaining stones to player 2's
            for i in range(6):  #empty all pits
                self.pits[i] = 0
                self.pits[i + 7] = 0

            #determine the winner
            if self.pits[6] > self.pits[13]:
                self.winner = "Player 1"
            elif self.pits[6] < self.pits[13]:
                self.winner = "Player 2"
            else:
                self.winner = None  # Tie

    def display_winner(self, screen):
        font = pygame.font.SysFont("Arial", 32)
        winner_text = f"Winner: {self.winner}" if self.winner else "It's a Tie!"  #determine the winner
        winner_message = font.render(winner_text, True, BLACK)  #render the winner message

        screen.fill(WHITE)  #clear the screen
        screen.blit(winner_message,
                    (WIDTH // 2 - winner_message.get_width() // 2, HEIGHT // 2 - 20))  #center the message
        pygame.display.flip()  #update the display

        pygame.time.wait(3000)  #wait for 3 seconds

    def reset(self):
        self.__init__()