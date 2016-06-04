import pygame

from . import logic


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.screen_size = self.screen_w, self.screen_h = screen.get_size()
        self.size = min(self.screen_w - 100, self.screen_h)
        self.tile_size = self.size / 16

        self.image = pygame.Surface((self.size, self.size))
        self.tiles = [pygame.Surface((self.tile_size, self.tile_size))
                      for x in range(3)]
        self.tiles[0].fill((0, 0, 0))
        self.tiles[1].fill((255, 255, 255))
        self.tiles[2].fill((0, 255, 0))
        self.tiles[2].set_alpha(100)
        for y in range(16):
            for x in range(16):
                self.draw(x, y)

        self._tiles = [[None for x in range(16)] for x in range(16)]
        self.chosen_tile = None
        self.chosen_tile2 = None  # used for chosing where to move
        self.bolded = []
        self.action = ""

    def draw(self, x, y):
        self.image.blit(self.tiles[(x + y) % 2], (x * self.tile_size,
                                                  y * self.tile_size))

    def bold(self, n):
        for x, y in self.bolded:
            self.image.blit(self.tiles[n], (x * self.tile_size, y *
                                            self.tile_size))

    def un_bold(self):
        for x, y in self.bolded:
            self.draw(x, y)

    def blit(self):
        self.screen.blit(self.image, (0, 0))

    def click(self, pos):
        x, y = pos
        tile_x = int(x // self.tile_size)
        tile_y = int(y // self.tile_size)
        if self.action in ("move", "attack"):
            self.chosen_tile2 = (tile_x, tile_y)
        else:
            self.chosen_tile = (tile_x, tile_y)
        return (tile_x, tile_y, self[tile_x, tile_y],
                (tile_x, tile_y) in self.bolded)

    def do(self, action):
        if action == "move":
            self.action = action
            figure = self[self.chosen_tile]
            self.bolded = figure.get_move()
            self.bold(2)
        elif self.action == "move":
            self.un_bold()
            self.bolded = []

        if action == "confirm":
            figure = self[self.chosen_tile]
            if self.action == "move":
                figure.move(self.chosen_tile2)
            self.action = ""
            self.chosen_tile = None
            self.chosen_tile2 = None
            self.bolded = []

    def __getitem__(self, pos):
        x, y = pos
        return self._tiles[y][x]

    def __setitem__(self, pos, item):
        x, y = pos
        self._tiles[y][x] = item


class Player:
    SETTINGS = {
        logic.King: [(8, 0), (9, 0)],
        logic.Pawn: [(8, 1), (9, 1)]
        }
    def __init__(self, board, red):
        self.board = board
        self.screen = self.board.screen
        self.red = red
        self.figures = []
        self.images = {
            "King": (pygame.image.load("doc/art/blue_king.png"),
                     pygame.image.load("doc/art/red_king.png")),
            "Pawn": (pygame.image.load("doc/art/blue_pawn.png"),
                     pygame.image.load("doc/art/red_pawn.png"))
            }
        for figure in self.SETTINGS:
            for x, y in self.SETTINGS[figure]:
                if self.red:
                    y = ~y & 0b1111
                self.figures.append(figure(x, y, self))
        self.turn = 0

    def blit(self):
        for figure in self.figures:
            figure.blit()

    def start(self):
        self.turn = 3
