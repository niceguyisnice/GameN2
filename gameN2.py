import pygame as p; import ctypes; from PIL import Image; import unittest


class Player(object):
    player_flip = False

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left_speed = -5
        self.right_speed = 5
        self.up_speed = 5
        self.down_speed = 5
        self.movement = [0, 0]
        self.jumping = False
        self.jumpcnt = 10
        self.moving_right = False
        self.moving_left = False
        self.rect = p.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.update_rect = p.Rect(rectangle.x, rectangle.y, rectangle.width, rectangle.height)
        self.update_movement = [0, 0]

        if tick % 5 == 0:
            if self.movement[0] > 0: self.movement[0] -= 1
            if self.movement[0] < 0: self.movement[0] += 1
            if self.movement[1] > 0: self.movement[1] -= 1
            if self.movement[1] < 0: self.movement[1] += 1

        if self.moving_right == True:
            self.update_movement[0] = self.right_speed
        if self.moving_left == True:
            self.update_movement[0] = self.left_speed

        # self.x += self.update_movement[0]
        # self.y += self.update_movement[1]


    def events(self):
        global keys, player_y_momentum
        keys = p.key.get_pressed()

        for event in p.event.get():
            if event.type == p.QUIT:
                Game.run = False
            if keys[p.K_ESCAPE]:
                Game.run = False

            if event.type == p.KEYDOWN:
                if event.key == p.K_d:
                    self.moving_right = True
                if event.key == p.K_a:
                    self.moving_left = True
                if event.key == p.K_SPACE:
                    player_y_momentum = -5

            if event.type == p.KEYUP:
                if event.key == p.K_d:
                    self.moving_right = False
                if event.key == p.K_a:
                    self.moving_left = False

    @staticmethod
    def collision_detection(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    @staticmethod
    def move(rect, movement, tiles):
        collision_sides = {"top" : False, "bottom" : False, "left" : False, "right" : False}
        rectangle.x += movement[0]
        hit_list = Player.collision_detection(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                # rectangle.x = tile.x + rectangle.width
                rect.right = tile.left
                collision_sides[ "right" ] = True 
            elif movement[0] < 0:
                #rectangle.x = tile.x - rectangle.width
                rect.left = tile.right
                collision_sides[ "left" ] = True 
        rectangle.y += movement[1]
        hit_list = Player.collision_detection(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                #rectangle.y = tile.y - rectangle.height
                rect.bottom = tile.top
                collision_sides[ "bottom" ] = True 
            elif movement[1] < 0:
                #rectangle.y = tile.y + rectangle.height
                rect.top = tile.bottom
                collision_sides[ "right" ] = True 

        print(rect)

        return rect, collision_sides

class Tiles():
    pass

class Game():
    p.init()
    p.display.set_caption("عائلتك مثلي الجنس")
    ctypes.windll.user32.SetProcessDPIAware()

    run = True
    scr_width, scr_height = 720, 1280
    MINTGREEN, BROWN = (122, 252, 200), (164, 131, 100)
    win = p.display.set_mode((scr_height, scr_width))
    clock = p.time.Clock()

    @staticmethod
    def load_game_map():
        global game_map
        map_txt = open("game_map.txt", "r")
        game_map = map_txt.readlines()

        for i in range(0, len(game_map)):
            game_map[i] = game_map[i].replace("\n", "")

        map_txt.close()

    @staticmethod
    def main():

        global tick, player_y_momentum
        tick = 0

        obstacle = p.image.load("platform_metroidvania asset pack v1.0/tiles and background_foreground/tileset.png").convert_alpha()
        sprite = p.image.load("platform_metroidvania asset pack v1.0/herochar sprites(new)/herochar_run_anim.gif").convert_alpha()
        sprite = p.transform.scale(sprite, (50, 50))

        sprite_mask = p.mask.from_surface(sprite)
        obstacle_mask = p.mask.from_surface(obstacle)
        Game.load_game_map()
        player_y_momentum = 0

        while Game.run:
            Game.clock.tick(60)
            Game.win.fill(0)

            tile_rects = []
            y = 0
            for row in game_map:
               x = 0
               for tile in row:
                   if tile == '1':
                       p.draw.rect(Game.win, Game.BROWN, (x * 50, y * 50, 50, 50))
                #    if tile == '2':
                #        p.draw.rect(Game.win, Game.BROWN,(x * 50, y * 50, 50, 50))
                   if tile != '0':
                       tile_rects.append(p.Rect(x * 50, y * 50, 50, 50))
                   x += 1
               y += 1

            #rectangle.movement = [0, 0]

            rectangle.update()

            rectangle.update_movement[1] += player_y_momentum
            player_y_momentum += 0.2
            if player_y_momentum > 10:
                player_y_momentum = 10

            rectangle.events()

            rectangle.update_rect, collision_sides = Player.move(rectangle.update_rect, rectangle.update_movement, tile_rects)




            if collision_sides[ "bottom" ]:
                player_y_momentum = -0.6

            

            Game.win.blit(sprite, (rectangle.x, rectangle.y))
            p.display.flip()

            tick += 1

rectangle = Player(100, 180, 50, 50)
obstacle1 = Player(300, 300, 50, 50)

Game.main()
p.quit()
