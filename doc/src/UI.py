import pygame


class Main_manager:
    """Manages all pictures in right section not knowing what they really are!"""
    def __init__(self, screen, x, y, spacing):
        self.screen = screen
        self.x = x
        self.y = y
        self.spacing = spacing
        self.images = []
        self.sizes = []
        self.counter = -1

    def add(self, image):
        self.images.append(image)
        self.sizes.append(image.get_height())
        self.counter += 1
        return self.counter

    def add_empty(self):
        self.images.append(None)
        self.sizes.append(0)
        self.counter += 1
        return self.counter

    def change(self, num, new_image):
        self.images[num] = new_image
        self.sizes[num] = new_image.get_height()

    def set_empty(self, num):
        self.images[num] = None
        self.sizes[num] = 0

    def blit(self):
        y = self.y
        for image, size in zip(self.images, self.sizes):
            if image is not None:
                self.screen.blit(image, (self.x, y))
                y += self.spacing
                y += size

    def click(self, pos):
        x, y = pos
        i_y = self.y  # current image y
        if x < self.x:
            return None
        for n, (image, size) in enumerate(zip(self.images, self.sizes)):
            if i_y > y:
                return None
            elif i_y + size > y:
                if x < self.x + image.get_width():
                    return n
                return None
            i_y += size
            if image is not None:
                i_y += self.spacing
        return None


class Text_manager:
    """Adds and changes text in main manager."""
    def __init__(self, main, colour, font):
        self.main = main
        self.colour = colour
        self.font = font
        self.table = {}  # contains positions of images in main manager
        self.name_text = {}

    def add(self, name, text):
        if text:
            image = self.font.render(text, True, self.colour)
            self.table[name] = self.main.add(image)
        else:
            self.table[name] = self.main.add_empty()
        self.name_text[name] = text

    def change(self, name, text):
        if text:
            image = self.font.render(text, True, self.colour)
            self.main.change(self.table[name], image)
        else:
            self.main.set_empty(self.table[name])
        self.name_text[name] = text


class Option_manager(Text_manager):
    """Manages options (only one can be chosed) in main manager."""
    def __init__(self, main, colour, font, bold_colour):
        super().__init__(main, colour, font)
        self.normal_colour = colour
        self.bold_colour = bold_colour
        self.options = {}
        self.chosen = None

    def add(self, name, text, default=False):
        if default:
            self.colour = self.bold_colour
            self.chosen = name
        super().add(name, text)
        self.colour = self.normal_colour
        self.options[self.table[name]] = name

    def deactivate(self):
        if self.chosen is not None:
            self.change(self.chosen, self.name_text[self.chosen])
            self.chosen = None

    def chose(self, num):
        if num in self.options:
            if self.chosen == self.options[num]:
                self.deactivate()
            else:
                self.deactivate()
                self.colour = self.bold_colour
                name = self.options[num]
                self.change(name, self.name_text[name])
                self.colour = self.normal_colour
                self.chosen = self.options[num]

            return True
        return False


class Button_manager(Text_manager):
    """Manages buttons."""
    def __init__(self, main, colour, font):
        super().__init__(main, colour, font)
        self.commands = {}

    def add(self, name, text, command):
        super().add(name, text)
        self.commands[self.table[name]] = command

    def chose(self, num):
        if num in self.commands:
            return self.commands[num]()
        return False

class Game_menu:
    def __init__(self, screen, x):
        self.screen = screen
        self.x = x
        self.width = self.screen.get_width() - self.x

        self.main_manager = Main_manager(self.screen, self.x + self.width *
                                         0.1, 20, 20)

        self.font = pygame.font.Font("doc/art/sanitechtro.regular.ttf", 26)
        self.text_manager = Text_manager(self.main_manager, (0, 0, 0),
                                         self.font)
        self.text_manager.add("board", "MAIN BOARD")
        self.text_manager.add("turn", "Red player's turn!")
        self.text_manager.add("left", "3 turns left")
        self.text_manager.add("position", "")
        self.text_manager.add("ship", "")

        self.option_manager = Option_manager(self.main_manager, (0, 0, 0),
                                             self.font, (255, 255, 255))
        self.option_manager.add("move", "")
        self.option_manager.add("attack", "")

        self.text_manager.add("new position", "")
        self.text_manager.add("new ship", "")
        self.text_manager.add("available", "")

        self.button_manager = Button_manager(self.main_manager, (0, 0, 0),
                                             self.font)
        self.button_manager.add("confirm", "", self.confirm)

    def blit(self):
        self.main_manager.blit()

    def click(self, pos):
        n = self.main_manager.click(pos)
        if self.option_manager.chose(n):
            self.deselect()
            if self.option_manager.chosen:
                return self.option_manager.chosen
            return "empty"
        ret = self.button_manager.chose(n)
        if ret:
            return ret

    def confirm(self):
        self.deselect()
        self.text_manager.change("position", "")
        self.text_manager.change("ship", "")
        self.option_manager.change("move", "")
        self.option_manager.change("attack", "")
        self.option_manager.chosen = None
        return "confirm"

    def deselect(self):
        self.text_manager.change("new position", "")
        self.text_manager.change("new ship", "")
        self.text_manager.change("available", "")
        self.button_manager.change("confirm", "")        

    def set_tile(self, info):
        x, y, tile, possible = info
        if self.option_manager.chosen in ("move", "attack"):
            self.text_manager.change("new position", "{}, {}".format(x, y))
            if tile is None:
                self.text_manager.change("new ship", "Empty")
            else:
                self.text_manager.change("new ship", " ".join((tile.colour,
                                                           tile.name)))
            if possible:
                self.button_manager.change("confirm", "Confirm!")
            else:
                self.text_manager.change("available", "Tile not available!")
        else:
            self.text_manager.change("position", "{}, {}".format(x, y))
            if tile is None:
                self.text_manager.change("ship", "Empty")
                self.option_manager.change("move", "")
                self.option_manager.change("attack", "")
            else:
                self.text_manager.change("ship", " ".join((tile.colour,
                                                           tile.name)))
                if tile.is_on_turn():
                    self.option_manager.change("move", "Move")
                    self.option_manager.change("attack", "Attack")

    def set_turn(self, colour, turns):
        self.text_manager.change("turn", "{} player's turn!".format(colour))
        self.text_manager.change("left", "{} turn{} left".format(turns,
                                                                 "s" *
                                                                 (turns >
                                                                  1)))
