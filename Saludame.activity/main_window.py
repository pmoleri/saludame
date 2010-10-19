# -*- coding: utf-8 -*-

import pygame
from gettext import gettext as _

import menu_creator

from window import *
import status_bars

class MainWindow(Window):
    
    def __init__(self, container, rect, frame_rate, clock, windows_controller, cha_loader, bg_color=(0, 0, 0)):
        Window.__init__(self, container, rect, frame_rate, windows_controller, bg_color)
        
        self.name = "main"
        self.clock = clock
        self.cha_loader = cha_loader
        
        self.windows = []   # Lista de ventanas que 'componen' la ventana principal
        
        #temporal para probar ActionWindow (se cargará el diccionario en un módulo aparte).
        self.animations_dic = {'eat_apple': (animation.Apple(pygame.Rect((210, 20), (150, 172)), 10), "Eating an apple!") }
        self.action_win = ActionWindow(container, pygame.Rect((185, 609), (1015, 200)), 10, windows_controller, self.animations_dic, pygame.Color("blue"))
        
        self.kidW = KidWindow(container, pygame.Rect((227, 0), (973, 609)), 1, windows_controller)
        self.windows.append(self.kidW)
        #self.windows.append(animation.Apple(pygame.Rect((700, 90), (150, 172)), 10))
        
        self.windows.append(animation.FPS(container, pygame.Rect((1100, 550), (50, 20)), 15, self.clock))
        self.windows.append(self.action_win)
        self.windows.append(status_bars.BarsWindow(container, pygame.Rect(0, 0, 227, 590), 1, windows_controller))
        
        character = " "
        self.windows.append(menu_creator.load_menu(character, (200, 200), self.kidW.kid_rect, windows_controller))
        
        self.add_child(Clock(container, pygame.Rect(0, 528, 1, 1), 1))
        
        challengesButton = ImageButton(self.rect, pygame.Rect((1000, 400), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_challenges)
        challengesButton.set_tooltip("Challenges module")
        customizationButton = ImageButton(self.rect, pygame.Rect((1000, 530), (50, 50)), 1, "customization/palette.png", self._cb_button_click_customization)
        customizationButton.set_tooltip("Customization module")
        
        self.buttons.append(challengesButton)
        self.buttons.append(customizationButton) 
        
        for b in self.buttons:
            self.add_child(b) 
        
    def _cb_button_click_challenges(self, button):
        challenges_window = self.cha_loader.get_challenge()
        self.windows_controller.add_new_window(challenges_window, "challenges")
        self.windows_controller.set_active_window("challenges")
        
    def _cb_button_click_customization(self, button):
        self.windows_controller.set_active_window("customization")

class Clock(Widget):
    
    def __init__(self, container, rect_in_container, frame_rate):
        surface = pygame.image.load("assets/layout/clock_background.png").convert_alpha()
        rect_in_container.size = surface.get_size()
        Widget.__init__(self, container, rect_in_container, frame_rate, surface)
    


