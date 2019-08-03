"""
This is the documentation for the controls module.

Controls supports easy updating and setup for controls.

Controls objects have 2 attributes:
    current
    previous

Those are both dictionaries:

{"mouse": {"pressed": (bool, bool, bool),
           "position": (int, int) or None},
 "keyboard": dict}

"mouse" branch is self-descriptive,
where "pressed" represents all 3 mouse buttons, whether they are pressed or not,
and where "position" represents the cursor's (x, y) position on the surface.

"keyboard" is a dictionary, where each used key is put as key-index:bool pair.

Let's start thinking about the usage of the Controls.

Initialization:
    In the initialization, Controls.__init__ wants an iterable, an iterable of integers or characters.
    Each character must either represent the key index, or the key character.
    You need to put the key index of each character, that is going to be used in the program.
    Controls("wasd") => {"mouse": {...},
                         "keyboard": {97: bool, 100: bool, 115: bool, 119: bool}}
    Controls((97, 100, 115, 119)) would have the same result.

    Those key positions would be checked each time the Controls object is updated.

    c = Controls(...)

Loop:
    In each iteration of the loop, you might want to update the controls.
    This is done with:
    c.update()
    This will test the mouse and keyboard poses and update those to the c.current dictionary.
    c.previous dictionary would always be a copy of c.current dictionary of the previous iteration.

Working with controls:
    When you want to check keyboard or mouse current or previous pose, you can use the dictionary:
    c.current["mouse"]["position"] -> (int, int) or None
    But there is a bit shorter way:
    c.get_short("cmpos") -> (int, int) or None
    Where:
    "c" "mou" "pos"
    are shorts of:
    "c": current
    "m": mouse
    "pos" position

    If you want to check whether B key is pressed, you should use this:
    c.get_short("ck")[98]

    Not this:
    c.get_short("ck98")

    get_short only works for: and equals:
    "c" + "k"             | c.current["keyboard"]
    "c" + "m" + "pos"     | c.current["mouse"]["position"]
    "c" + "m" + "pre"     | c.current["mouse"]["pressed"]
    "p" + "k"             | c.previous["keyboard"]
    "p" + "m" + "pos"     | c.previous["mouse"]["position"]
    "p" + "m" + "pre"     | c.previous["mouse"]["pressed"]
"""


class __Testings:
    def __init__(self, cls):
        global pygame
        import pygame
        pygame.init()
        self.surface = pygame.display.set_mode((500, 500))
        
        if cls == "Controls":
            c = Controls("adsw")
            
            while not any(e.type == 12 for e in c.current["events"]):
                time1 = pygame.time.get_ticks()
                c.update()
                time2 = pygame.time.get_ticks()
                self.surface.fill((0, 0, 0))

                self.print("control testing mode")
                self.print("mouse", 1)
                self.print("pressed: {0}".format(c.get_short("cmpre")), 2, 1)
                self.print("position: {0}".format(c.get_short("cmpos")), 3, 1)
                self.print("keyboard: {0}".format(c.get_short("ck")), 4, 0)
                self.print("Time per frame: {0} ms".format(time2-time1), 5, 0)
                pygame.display.flip()
                pygame.time.delay(100)

        pygame.quit()

    def print(self, text, line=0, column=0):
        font = pygame.font.Font(None, 25)
        text_surface = font.render(text, 1, (255, 255, 255))
        rect = text_surface.get_rect()
        rect.move_ip(column*25, line*25)
        self.surface.blit(text_surface, rect)

class Controls:
    def __init__(self, pygame, keyboard_indices=()):
        self.pygame = pygame
        
        self.keyboard_indices = tuple(map(lambda x: ord(x) if isinstance(x, str) else x, keyboard_indices))
        raw_dict = {"mouse": {"pressed": (0, 0, 0),
                         "position": None},
               "keyboard": {},
               "events": []}
        
        self.min = 0
        self.max = 0
        
        for i in self.keyboard_indices:
            if i > self.max:
                self.max = i
            elif i < self.min:
                self.min = i
            
            raw_dict["keyboard"][i] = 0

        self.max += 1

        self.current = raw_dict.copy()
        self.previous = raw_dict.copy()

    def update(self):
        self.previous = self.current.copy()

        self.current["events"] = self.pygame.event.get()

        if self.pygame.mouse.get_focused():
            self.current["mouse"]["pressed"] = self.pygame.mouse.get_pressed()
            self.current["mouse"]["position"] = self.pygame.mouse.get_pos()
        else:
            self.current["mouse"]["pressed"] = (0, 0, 0)
            self.current["mouse"]["position"] = None

        raw_keyboard = tuple(self.pygame.key.get_pressed())

        for i in range(self.min, self.max):
            if i in self.keyboard_indices:
                self.current["keyboard"][i] = raw_keyboard[i]

    def get_short(self, short):
        if short[0] == "c":
            if short[1] == "m":
                if short[2:5] == "pre":
                    return self.current["mouse"]["pressed"]
                elif short[2:5] == "pos":
                    return self.current["mouse"]["position"]
            elif short[1] == "k":
                return self.current["keyboard"]
        elif short[0] == "p":
            if short[1] == "m":
                if short[2:5] == "pre":
                    return self.previous["mouse"]["pressed"]
                elif short[2:5]:
                    return self.previous["mouse"]["position"]
            elif short[1] == "k":
                return self.previous["keyboard"]

if __name__=="__main__":
    __Testings("Controls")

