import pygame
import os
import random

# SCREEN SETTINGS
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Burger Funnel!")

# LOADING ASSETS
MAN = pygame.image.load(os.path.join("assets", "man.png"))
START = pygame.image.load(os.path.join("assets", "start.png"))
BURGER = pygame.image.load(os.path.join("assets", "burger.png"))
BURGER1 = pygame.image.load(os.path.join("assets", "burger1.png"))
BURGER2 = pygame.image.load(os.path.join("assets", "burger2.png"))
TOP = pygame.image.load(os.path.join("assets", "stick.png"))
LEFT = pygame.image.load(os.path.join("assets", "stick1.png"))
RIGHT = pygame.image.load(os.path.join("assets", "stick2.png"))
BGD = pygame.transform.scale((pygame.image.load(os.path.join("assets", "background.png"))), (WIDTH, HEIGHT))

# FONTS
pygame.font.init()
main_font = pygame.font.SysFont("", 50)
tip_font = pygame.font.SysFont("", 25, italic=True)
go_font = pygame.font.SysFont("", 65, bold=True)


class Main:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = None

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()


class Player(Main):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = MAN
        self.mask = pygame.mask.from_surface(self.image)


class Burger(Main):
    AXIS_MAP = {
        "one": BURGER,
        "two": BURGER1,
        "three": BURGER2
    }

    def __init__(self, x, y, axis):
        super().__init__(x, y)
        self.image = self.AXIS_MAP[axis]
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, burger_vel, obj):
        self.y += burger_vel
        if self.collision(obj):
            return True

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main_menu():
    running = True
    while running:
        WIN.blit(BGD, (0, 0))
        WIN.blit(START, (10, 450))
        start_label = go_font.render("BURGER FUNNEL!", 1, (255, 255, 255))
        begin_label = main_font.render("Press Spacebar to Begin", 1, (255, 255, 255))
        WIN.blit(start_label, (int(WIDTH / 2 - start_label.get_width() / 2), 350))
        WIN.blit(begin_label, (int(WIDTH / 2 - begin_label.get_width() / 2), 450))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            main()
    pygame.quit()


def main():
    running = True
    game_over = False
    clock = pygame.time.Clock()
    fps = 60
    go_count = 0
    score = 0
    left = False
    right = False

    # Generate new player
    velocity = 5
    player = Player(-600, 475)

    # Generate a wave of burgers
    wave_length = 40
    burgers_drop = 0
    burgers = []
    burger_vel = 3

    def redraw_window():
        WIN.blit(BGD, (0, 0))

        # Draw score and burgers dropped
        score_label = main_font.render(f"SCORE: {score}", 1, (255, 255, 255))
        burger_label = main_font.render(f"DROPPED: {burgers_drop}", 1, (255, 255, 255))
        tip_label = tip_font.render("DONT DROP MORE THAN 20 BURGERS!", 1, (255, 255, 255))
        WIN.blit(score_label, (10, 10))
        WIN.blit(burger_label, (WIDTH - burger_label.get_width() - 10, 10))
        WIN.blit(tip_label, (WIDTH - tip_label.get_width() - 10, 50))

        if left:
            WIN.blit(LEFT, (10, 555))
        elif right:
            WIN.blit(RIGHT, (10, 555))
        else:
            WIN.blit(TOP, (10, 555))

        # Draw the player
        player.draw(WIN)

        # draw the burgers
        for b in burgers:
            b.draw(WIN)

        if game_over:
            go_label = go_font.render("GAME OVER!", 1, (255, 255, 255))
            go_label1 = go_font.render(f"YOUR FINAL SCORE IS {score}", 1, (255, 255, 255))
            WIN.blit(go_label, (int(WIDTH/2 - go_label.get_width()/2), 350))
            WIN.blit(go_label1, (int(WIDTH/2 - go_label1.get_width()/2), 450))

        pygame.display.update()

    while running:
        clock.tick(fps)
        redraw_window()

        # Game over screen
        if burgers_drop == 20:
            game_over = True
            go_count += 1
        if game_over:
            if go_count > fps * 5:
                running = False
            else:
                continue

        # Generating random burgers
        if len(burgers) == 0:
            for i in range(wave_length):
                burger = Burger(random.randrange(20, WIDTH - 20), random.randrange(-6000, -100),
                                random.choice(["one", "two", "three"]))
                burgers.append(burger)

        # Quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Pressing keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x + velocity > -950:
            player.x -= velocity
            left = True
            right = False
        if keys[pygame.K_RIGHT] and player.x + velocity < -250:
            player.x += velocity
            left = False
            right = True

        # Appending burger collisions
        for burger in burgers[:]:
            if burger.move(burger_vel, player):
                score += 10
                burgers.remove(burger)
            if burger.y + burger.get_height() > 650:
                burgers_drop += 1
                burgers.remove(burger)


main_menu()
