#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os
import sys


window_size = window_width, window_height = 450, 350
FPS = 10
levels_dir = "levels"
tile_size = 50

class Sokoban:

    def __init__(self, filename, free_tiles, finish_tile):
        self.mapz = []
        self.image1 = self.load_image(r'images\free_tile0.png')
        self.image1 = pygame.transform.scale(self.image1, (tile_size, tile_size))
        self.image2 = self.load_image(r'images\wall1.png')
        self.image2 = pygame.transform.scale(self.image2, (tile_size, tile_size))
        self.image3 = self.load_image(r'images\finish_tile2.png')
        self.image3 = pygame.transform.scale(self.image3, (tile_size, tile_size))
        self.image4 = self.load_image(r"images\nothing.png")
        self.image4 = pygame.transform.scale(self.image4, (tile_size, tile_size))
        with open(f"{levels_dir}/{filename}") as input_file:
            for line in input_file:
                self.mapz.append(list(map(int, line.split())))
        self.height = len(self.mapz)
        self.width = len(self.mapz[0])
        self.tile_size = tile_size
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def load_image(self, name, colorkey=None):
        fullname = os.path.join(os.path.dirname(__file__), name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            pass
        return image

    def render(self, screen):
        colors = {0: self.image2, 1: self.image1, 2: self.image3, 3: self.image4}
        for y in range(self.height):
            for x in range(self.width):
                screen.blit(colors[self.get_tile_id((x, y))], (x * tile_size, y * tile_size))

    def get_tile_id(self, position):
        return self.mapz[position[1]][position[0]]

    def is_free(self, position):
        return str(self.get_tile_id(position)) in str(self.free_tiles)


class Hero:

    def __init__(self, position):
        self.x, self.y = position
        self.image5 = self.load_image(r"images\hero.png")
        self.image5 = pygame.transform.scale(self.image5, (tile_size, tile_size))

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
        screen.blit(self.image5, (self.x * tile_size, self.y * tile_size))
        
    def load_image(self, name, colorkey=None):
        fullname = os.path.join(os.path.dirname(__file__), name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        colorkey = -1
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            pass
        return image    

class Game:

    def __init__(self, sokoban, hero, box1, box2, box3, n):
        self.sokoban = sokoban
        self.hero = hero
        self.box1 = box1
        self.box2 = box2
        self.box3 = box3
        self.n = n

    def load_image(self, name, colorkey=None):
        fullname = os.path.join(os.path.dirname(__file__), name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            pass
        return image      

    def render(self, screen):
        self.sokoban.render(screen)
        self.hero.render(screen)
        self.box1.render(screen)
        self.box2.render(screen)
        self.box3.render(screen)
        rn = button((window_width - 35, 20), (85, 30), (220, 220, 220), (255, 0, 0), None, 'restart')
        button_list = [rn]
        for b in button_list:
            b.draw(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        previous_x, previous_y = next_x, next_y
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1

        if self.sokoban.is_free((next_x, next_y)) and self.box1.check_box1((next_x, next_y)) and self.box2.check_box2((next_x, next_y)) and self.box3.check_box3((next_x, next_y)):  #
            self.hero.set_position((next_x, next_y))
# 1 to 2
        next_pos = next_x + 1, next_y
        if previous_x == next_x - 1 and previous_y == next_y and self.box1.check_box1((next_x, next_y)) is False and self.sokoban.is_free((next_x + 1, next_y)) and next_pos != self.box3.get_position():  # +x
            next_pos = next_x + 1, next_y
            if next_pos != self.box2.get_position():
                self.box1.set_position((next_x + 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x - 1, next_y
        if previous_x == next_x + 1 and previous_y == next_y and self.box1.check_box1((next_x, next_y)) is False and self.sokoban.is_free((next_x - 1, next_y)) and next_pos != self.box3.get_position() and next_pos != self.box2.get_position():  # -x
            next_pos = next_x - 1, next_y
            if next_pos != self.box2.get_position():
                self.box1.set_position((next_x - 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y + 1
        if previous_x == next_x and previous_y == next_y - 1 and self.box1.check_box1((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y + 1)) and next_pos != self.box3.get_position():  # +y
            next_pos = next_x, next_y + 1
            if next_pos != self.box2.get_position():
                self.box1.set_position((next_x, next_y + 1))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y - 1
        if previous_x == next_x and previous_y == next_y + 1 and self.box1.check_box1((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y - 1)) and next_pos != self.box3.get_position():  # -y
            next_pos = next_x, next_y - 1
            if next_pos != self.box2.get_position():
                self.box1.set_position((next_x, next_y - 1))
                self.hero.set_position((next_x, next_y))
# 1 to 3
        next_pos = next_x + 1, next_y
        if previous_x == next_x - 1 and previous_y == next_y and self.box1.check_box1((next_x, next_y)) is False and self.sokoban.is_free((next_x + 1, next_y)) and next_pos != self.box2.get_position() and next_pos != self.box3.get_position():  # +x
            next_pos = next_x + 1, next_y
            if next_pos != self.box3.get_position():
                self.box1.set_position((next_x + 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x - 1, next_y
        if previous_x == next_x + 1 and previous_y == next_y and self.box1.check_box1((next_x, next_y)) is False and self.sokoban.is_free((next_x - 1, next_y)) and next_pos != self.box2.get_position():  # -x
            next_pos = next_x - 1, next_y
            if next_pos != self.box3.get_position():
                self.box1.set_position((next_x - 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y + 1
        if previous_x == next_x and previous_y == next_y - 1 and self.box1.check_box1((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y + 1)) and next_pos != self.box2.get_position():  # +y
            next_pos = next_x, next_y + 1
            if next_pos != self.box3.get_position():
                self.box1.set_position((next_x, next_y + 1))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y - 1
        if previous_x == next_x and previous_y == next_y + 1 and self.box1.check_box1((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y - 1)) and next_pos != self.box2.get_position():  # -y
            next_pos = next_x, next_y - 1
            if next_pos != self.box3.get_position():
                self.box1.set_position((next_x, next_y - 1))
                self.hero.set_position((next_x, next_y))
# 2 to 1
        next_pos = next_x + 1, next_y
        if previous_x == next_x - 1 and previous_y == next_y and self.box2.check_box2((next_x, next_y)) is False and self.sokoban.is_free((next_x + 1, next_y)) and next_pos != self.box3.get_position():  # +x
            next_pos = next_x + 1, next_y
            if next_pos != self.box1.get_position():
                self.box2.set_position((next_x + 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x - 1, next_y
        if previous_x == next_x + 1 and previous_y == next_y and self.box2.check_box2((next_x, next_y)) is False and self.sokoban.is_free((next_x - 1, next_y)) and next_pos != self.box3.get_position():  # -x
            next_pos = next_x - 1, next_y
            if next_pos != self.box1.get_position():
                self.box2.set_position((next_x - 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y + 1
        if previous_x == next_x and previous_y == next_y - 1 and self.box2.check_box2((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y + 1)) and next_pos != self.box3.get_position():  # +y
            next_pos = next_x, next_y + 1
            if next_pos != self.box1.get_position():
                self.box2.set_position((next_x, next_y + 1))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y - 1
        if previous_x == next_x and previous_y == next_y + 1 and self.box2.check_box2((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y - 1)) and next_pos != self.box3.get_position():  # -y
            next_pos = next_x, next_y - 1
            if next_pos != self.box1.get_position():
                self.box2.set_position((next_x, next_y - 1))
                self.hero.set_position((next_x, next_y))
# 3 to 1
        next_pos = next_x + 1, next_y
        if previous_x == next_x - 1 and previous_y == next_y and self.box3.check_box3((next_x, next_y)) is False and self.sokoban.is_free((next_x + 1, next_y)) and next_pos != self.box2.get_position() and next_pos != self.box1.get_position():  # +x
            next_pos = next_x + 1, next_y
            if next_pos != self.box1.get_position():
                self.box3.set_position((next_x + 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x - 1, next_y
        if previous_x == next_x + 1 and previous_y == next_y and self.box3.check_box3((next_x, next_y)) is False and self.sokoban.is_free((next_x - 1, next_y)) and next_pos != self.box2.get_position() and next_pos != self.box1.get_position():  # -x
            next_pos = next_x - 1, next_y
            if next_pos != self.box1.get_position():
                self.box3.set_position((next_x - 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y + 1
        if previous_x == next_x and previous_y == next_y - 1 and self.box3.check_box3((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y + 1)) and next_pos != self.box2.get_position() and next_pos != self.box1.get_position():  # +y
            next_pos = next_x, next_y + 1
            if next_pos != self.box1.get_position():
                self.box3.set_position((next_x, next_y + 1))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y - 1
        if previous_x == next_x and previous_y == next_y + 1 and self.box3.check_box3((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y - 1)) and next_pos != self.box2.get_position() and next_pos != self.box1.get_position():  # -y
            next_pos = next_x, next_y - 1
            if next_pos != self.box1.get_position():
                    self.box3.set_position((next_x, next_y - 1))
                    self.hero.set_position((next_x, next_y))
# 2 to 3
        next_pos = next_x + 1, next_y
        if previous_x == next_x - 1 and previous_y == next_y and self.box2.check_box2((next_x, next_y)) is False and self.sokoban.is_free((next_x + 1, next_y)) and next_pos != self.box1.get_position():  # +x
            next_pos = next_x + 1, next_y
            if next_pos != self.box3.get_position():
                self.box2.set_position((next_x + 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x - 1, next_y
        if previous_x == next_x + 1 and previous_y == next_y and self.box2.check_box2((next_x, next_y)) is False and self.sokoban.is_free((next_x - 1, next_y)) and next_pos != self.box1.get_position():  # -x
            next_pos = next_x - 1, next_y
            if next_pos != self.box3.get_position():
                self.box2.set_position((next_x - 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y + 1
        if previous_x == next_x and previous_y == next_y - 1 and self.box2.check_box2((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y + 1)) and next_pos != self.box1.get_position():  # +y
            next_pos = next_x, next_y + 1
            if next_pos != self.box3.get_position():
                self.box2.set_position((next_x, next_y + 1))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y - 1
        if previous_x == next_x and previous_y == next_y + 1 and self.box2.check_box2((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y - 1)) and next_pos != self.box1.get_position():  # -y
            next_pos = next_x, next_y - 1
            if next_pos != self.box3.get_position():
                self.box2.set_position((next_x, next_y - 1))
                self.hero.set_position((next_x, next_y))
# 3 to 2
        next_pos = next_x + 1, next_y
        if previous_x == next_x - 1 and previous_y == next_y and self.box3.check_box3((next_x, next_y)) is False and self.sokoban.is_free((next_x + 1, next_y)) and next_pos != self.box1.get_position():  # +x
            next_pos = next_x + 1, next_y
            if next_pos != self.box2.get_position():
                self.box3.set_position((next_x + 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x - 1, next_y
        if previous_x == next_x + 1 and previous_y == next_y and self.box3.check_box3((next_x, next_y)) is False and self.sokoban.is_free((next_x - 1, next_y)) and next_pos != self.box1.get_position():  # -x
            next_pos = next_x - 1, next_y
            if next_pos != self.box2.get_position():
                self.box3.set_position((next_x - 1, next_y))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y + 1
        if previous_x == next_x and previous_y == next_y - 1 and self.box3.check_box3((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y + 1)) and next_pos != self.box1.get_position():  # +y
            next_pos = next_x, next_y + 1
            if next_pos != self.box2.get_position():
                self.box3.set_position((next_x, next_y + 1))
                self.hero.set_position((next_x, next_y))
        next_pos = next_x, next_y - 1
        if previous_x == next_x and previous_y == next_y + 1 and self.box3.check_box3((next_x, next_y)) is False and self.sokoban.is_free((next_x, next_y - 1)) and next_pos != self.box1.get_position():  # -y
            next_pos = next_x, next_y - 1
            if next_pos != self.box2.get_position():
                self.box3.set_position((next_x, next_y - 1))
                self.hero.set_position((next_x, next_y))
        if self.box1.green1() and self.box2.green2() and self.box3.green3():
            knopka()
    def nomer(self, n):
        return n

class Box1:

    def __init__(self, position):
        self.image6 = self.load_image(r"images\box0.png")
        self.image6 = pygame.transform.scale(self.image6, (tile_size, tile_size))
        self.image7 = self.load_image(r"images\box1.png")
        self.image7 = pygame.transform.scale(self.image7, (tile_size, tile_size))
        self.image_main = self.image6        
        self.x1, self.y1 = position

    def get_position(self):
        return self.x1, self.y1

    def set_position(self, position):
        self.x1, self.y1 = position

    def check_box1(self, position):
        return position != self.get_position()
    
    def green1(self):
        position = self.get_position()
        aaa = position
        return sokoban.mapz[aaa[1]][aaa[0]] == 2    

    def load_image(self, name, colorkey=None):
        fullname = os.path.join(os.path.dirname(__file__), name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            pass
        return image      

    def render(self, screen):
        if self.green1():
            self.image_main = self.image7
        else:
            self.image_main = self.image6        
        screen.blit(self.image_main, (self.x1 * tile_size, self.y1 * tile_size))


class Box2:

    def __init__(self, position):
        self.image6 = self.load_image(r"images\box0.png")
        self.image6 = pygame.transform.scale(self.image6, (tile_size, tile_size))
        self.image7 = self.load_image(r"images\box1.png")
        self.image7 = pygame.transform.scale(self.image7, (tile_size, tile_size))
        self.image_main = self.image6
        self.x2, self.y2 = position

    def get_position(self):
        return self.x2, self.y2

    def set_position(self, position):
        self.x2, self.y2 = position
        
    def check_box2(self, position):
        return position != self.get_position()

    def green2(self):
        position = self.get_position()
        aaa = position
        return sokoban.mapz[aaa[1]][aaa[0]] == 2

    def load_image(self, name, colorkey=None):
        fullname = os.path.join(os.path.dirname(__file__), name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            pass
        return image      

    def render(self, screen):
        if self.green2():
            self.image_main = self.image7
        else:
            self.image_main = self.image6
        screen.blit(self.image_main, (self.x2 * tile_size, self.y2 * tile_size))

class Box3:

    def __init__(self, position):
        self.image6 = self.load_image(r"images\box0.png")
        self.image6 = pygame.transform.scale(self.image6, (tile_size, tile_size))
        self.image7 = self.load_image(r"images\box1.png")
        self.image7 = pygame.transform.scale(self.image7, (tile_size, tile_size))
        self.image_main = self.image6        
        self.x3, self.y3 = position

    def get_position(self):
        return self.x3, self.y3

    def set_position(self, position):
        self.x3, self.y3 = position
        
    def check_box3(self, position):
        return position != self.get_position()

    def green3(self):
        position = self.get_position()
        aaa = position
        return sokoban.mapz[aaa[1]][aaa[0]] == 2      

    def load_image(self, name, colorkey=None):
        fullname = os.path.join(os.path.dirname(__file__), name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            pass
        return image      

    def render(self, screen):
        if self.green3():
            self.image_main = self.image7
        else:
            self.image_main = self.image6
        screen.blit(self.image_main, (self.x3 * tile_size, self.y3 * tile_size))


class button:
    def __init__(self, position, size, clr=[100, 100, 100], cngclr=None, func=None, text='', font="Segoe Print", font_size=16, font_clr=[0, 0, 0]):
        self.clr = clr
        self.size = size
        self.func = func
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=position)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])


        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh // 2 for wh in self.size])

    def draw(self, screen):
        self.mouseover()

        self.surf.fill(self.curclr)
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.func:
            return self.func(*args)

class text:
    def __init__(self, msg, position, clr=[100, 100, 100], font="Segoe Print", font_size=15, mid=False):
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.txt_surf = self.font.render(msg, 1, clr)
        if len(clr) == 4:
            self.txt_surf.set_alpha(clr[3])
        if mid:
            self.position = self.txt_surf.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.txt_surf, self.position)

def load_image(name, colorkey=None):
    fullname = os.path.join(os.path.dirname(__file__), name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        pass
    return image

def main(n):
    global sokoban
    pygame.init()
    pygame.display.set_caption('Сокобан')
    screen = pygame.display.set_mode(window_size)
    if n == 1:
        sokoban = Sokoban("1level.txt", [0, 2], 2)
        hero = Hero((5, 5))
        box1 = Box1((3, 2))
        box2 = Box2((3, 3))
        box3 = Box3((4, 4))
    if n == 2:
        sokoban = Sokoban("2level.txt", [0, 2], 2)
        hero = Hero((6, 3))
        box1 = Box1((3, 3))
        box2 = Box2((4, 3))
        box3 = Box3((5, 3))
    if n == 3:
        sokoban = Sokoban("3level.txt", [0, 2], 2)
        hero = Hero((7, 2))
        box1 = Box1((6, 2))
        box2 = Box2((6, 4))
        box3 = Box3((3, 4))
    if n == 4:
        sokoban = Sokoban("4level.txt", [0, 2], 2)
        hero = Hero((2, 1))
        box1 = Box1((3, 1))
        box2 = Box2((3, 2))
        box3 = Box3((3, 3))
    if n == 5:
        sokoban = Sokoban("5level.txt", [0, 2], 2)
        hero = Hero((5, 4))
        box1 = Box1((4, 3))
        box2 = Box2((5, 3))
        box3 = Box3((6, 3))
    rect = pygame.Rect((window_width - 80, 5, window_width - 80, 30))
    game = Game(sokoban, hero, box1, box2, box3, n)
    clock = pygame.time.Clock()
    running = True
    restart = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    restart = True
        screen.fill((0, 0, 0))
        game.render(screen)
        game.update_hero()
        pygame.display.flip()
        clock.tick(FPS)
    if restart:
        main(n)
    return False

def terminate():
    pygame.quit()
    sys.exit()

def fn1():
    Game.nomer(1, 1)
    main(1)

def fn2():
    main(2)

def fn3():
    main(3)

def fn4():
    main(4)

def fn5():
    main(5)

def fn6():
    start_screen()

def knopka():
    pygame.init()
    pygame.display.set_caption('Сокобан')
    end = pygame.transform.scale(load_image(r'images\win.png'), window_size)
    screen = pygame.display.set_mode(window_size)
    screen.blit(end, (0, 0))
    kn = button((225, 175), (100, 50), (220, 220, 220), (255, 0, 0), fn6, 'Menu')
    button_list = [kn]
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for b in button_list:
                        if b.rect.collidepoint(pos):
                            b.call_back()
                            screen.blit(end, (0, 0))
                            running = False
            for b in button_list:
                b.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    
def start_screen():
    pygame.init()
    pygame.display.set_caption('Сокобан')
    fon = pygame.transform.scale(load_image(r'images\nach.png'), window_size)
    screen = pygame.display.set_mode(window_size)
    screen.blit(fon, (0, 0))
    button1 = button((80, 100), (100, 50),(220, 220, 220), (255, 0, 0), fn1, 'level 1')
    button2 = button((220, 100), (100, 50), (220, 220, 220), (255, 0, 0), fn2, 'level 2')
    button3 = button((380, 100), (100, 50), (220, 220, 220), (255, 0, 0), fn3, 'level 3')
    button4 = button((150, 200), (100, 50), (220, 220, 220), (255, 0, 0), fn4, 'level 4')
    button5 = button((300, 200), (100, 50), (220, 220, 220), (255, 0, 0), fn5, 'level 5')
    button_list = [button1, button2, button3, button4, button5]
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for b in button_list:
                        if b.rect.collidepoint(pos):
                            b.call_back()
                            screen.blit(fon, (0, 0))
                            running = False
            for b in button_list:
                b.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
start_screen()
