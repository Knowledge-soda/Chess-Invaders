import pygame

from doc.src import board, logic, UI

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.init()

        self.board = board.Board(self.screen)
        self.board_size = self.board.size

        self.game_menu = UI.Game_menu(self.screen, self.board_size)

        self.blue_player = board.Player(self.board, False)
        self.red_player = board.Player(self.board, True)
        self.red_player.start()
        self.turn = "Red"
        self.players = {"Blue": self.blue_player, "Red": self.red_player}

        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[0] < self.board_size:
                            info = self.board.click(event.pos)
                            self.game_menu.set_tile(info)
                        else:
                            action = self.game_menu.click(event.pos)
                            self.board.do(action)
                            if action == "confirm":
                                if not self.players[self.turn].turn:
                                    self.turn = "Blue" if self.turn ==\
                                                "Red" else "Red"
                                    self.players[self.turn].start()
                                self.game_menu.set_turn(self.turn,
                                                        self.players[self.turn].turn)

            self.screen.fill((128, 128, 128))

            self.board.blit()
            self.game_menu.blit()
            self.blue_player.blit()
            self.red_player.blit()

            pygame.display.flip()

game = Game()
game.run()
pygame.quit()
