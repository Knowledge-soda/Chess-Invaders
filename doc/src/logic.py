#New types should be added (queen, heavy infanty...)

#TO DO: move characteristics here and make it metaclass
class Ship:
    def __init__(self, name, moving):
        pass

#TO DO: add attacking, moves counter and board inside the ship
class King:
    name = "King"
    MOVE = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1),
            (1, 1)]
    IMG_NUM = 0
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.red = player.red
        self.colour = ["Blue", "Red"][self.red]
        self.board = player.board
        self.screen = player.screen
        self.image = player.images[self.name][self.red]
        self.size = self.width, self.height = self.image.get_size()

        self.tile_size = self.board.tile_size
        self.x_off = self.tile_size / 2 - self.width / 2
        self.y_off = self.tile_size / 2 - self.height / 2

        self.rx = self.x * self.tile_size + self.x_off
        self.ry = self.y * self.tile_size + self.y_off

        self.board[self.x, self.y] = self

    def blit(self):
        self.screen.blit(self.image, (self.rx, self.ry))

    def is_on_turn(self):
        return bool(self.player.turn)

    def get_move(self):
        ret = []
        for x, y in self.MOVE:
            if 0 <= self.x + x <= 15 and 0 <= self.y + y <= 15 and \
               self.board[self.x + x, self.y + y] is None:
                ret.append((self.x + x, self.y + y))
        return ret

    def move(self, pos):
        self.board[self.x, self.y] = None  # tile is empty now

        self.x, self.y = pos
        self.rx = self.x * self.tile_size + self.x_off
        self.ry = self.y * self.tile_size + self.y_off

        self.board[self.x, self.y] = self

        self.player.turn -= 1


class Pawn(King):
    name = "Pawn"
    MOVE = [(0, -1), (-1, 0), (1, 0), (0, 1)]

