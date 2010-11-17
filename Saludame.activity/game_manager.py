# -*- coding: utf-8 -*-

CONTROL_INTERVAL = 15 #cantidad de señales hasta que realiza un checkeo de las acciones.

import random

class GameManager:
    """
    Clase gestora del sistema. Se encarga del control de las acciones
    y los eventos del juego.
    """
    
    def __init__(self, character, bars_controller, actions_list, events_list, places_list, moods_list, windows_controller):
        """
        Constructor de la clase
        """
        self.character = character
        self.bars_controller = bars_controller
        self.windows_controller = windows_controller
        self.count = 0 #sirve como 'clock' interno, para mantener un orden de tiempo dentro de la clase.
        
        #evenst, actions, moods
        self.events_list = events_list
        self.actions_list = actions_list
        self.moods_list = moods_list        

        self.background_actions = []
        
        #character states
        self.active_char_action = None #Active character action, Action instance
        self.active_event = None 
        self.active_mood = None
        self.__check_active_mood() # sets active_mood
        
        self.places_list = places_list
        
        #for events handling:
        self.max_rand = self.__calculate_max_rand(self.events_list)
        self.probability_ranges = self.__calculate_ranges(self.events_list)
        

    def set_active_action(self, action_id):
        #place = get_place(self.character.actual_place) 
        #if(place.allowed_action(action_id)): #continúa con la acción, solo si es permitida en el lugar
        if(not self.active_char_action): #Si existe una accion activa no la interrumpe
            if(True): #dont check char's place yet
                action = self.get_action(action_id)
                if(action):
                    action.perform() 
                    self.windows_controller.show_action_animation(action)
                    self.active_char_action = action
    
    def get_active_action(self):
        """
        Return the character active action
        """
        return self.active_char_action
    
    def interrupt_active_action(self, action_id):
        """
        Stops the active action if exist, and set as active the
        action with the 'action_id'. If the action_id is 'None', just
        stops the active action.
        """
        self.active_char_action.reset()
        self.active_char_action = None
        
        if(action_id):
            action = self.get_action(action_id)
            if(action):
                self.active_char_action = action

    def add_background_action(self, action_id):
        """
        Add a background action.
        """
        action = self.get_action(action_id)
        if(action):
            self.background_actions.append(action)

    def signal(self):
        """
        Increment signal, it means that an iteration has been completed 
        """
        self.count += 1
        if(self.count >= CONTROL_INTERVAL):
            self.__control_active_actions() #handle active character actions
            self.bars_controller.calculate_score()  #calculates the score of the score_bar
            self.__control_active_events() #handle active events
            self.__check_active_mood() # check if the active character mood
            
            self.count = 0    
    
    def get_place(self, id_place):
        """
        Returns the place asociated to the id_place
        """
        for place in self.places_list:
            if(place.id == id_place):
                return place
    
    def get_action(self, action_id):
        """
        Returns the action asociated to the id_action
        """
        for action in self.actions_list:
            if(action.id == action_id):
                return action
        
    def __control_active_actions(self):
            
        for action in self.background_actions:
            action.perform()
            action.time_span = 1 #that means background actions never stop
            
        if(self.active_char_action): #if the character is performing an action: 
            if(self.active_char_action.time_left):
                self.active_char_action.perform()
            else: #if the action was completed: 
                self.active_char_action.reset()
                self.active_char_action = None
                self.windows_controller.stop_actual_action_animation()
                
                
## Moods handling

    def __check_active_mood(self):
        """
        Check the active mood, and set it according to the character state.
        """
        mood = None
        event_preferred_mood = 12 # set in highest mood rank (happy 1)
        overall_bar_percent = self.bars_controller.get_overall_percent()
        overall_bar_mood = 9 # set in normal mood
        
        if(overall_bar_percent < 0.33): 
            overall_bar_mood = 5 #set mood in sad grade 1
        elif(overall_bar_percent > 0.66):
            overall_bar_mood = 10 #set mood in happy 3
        
        if(self.active_event):
            event_preferred_mood = self.active_event.preferred_mood
        
        if(event_preferred_mood <= overall_bar_mood): # choose the lowest value
            mood = self.moods_list[event_preferred_mood]
        else:
            mood = self.moods_list[overall_bar_mood]
        
        if(mood <> self.active_mood):
            self.active_mood = mood
            self.windows_controller.set_mood(mood)
            print "cambio estado de animo a: ", self.active_mood.name
        
## Events handling

    def __control_active_events(self):
        """
        Active event handler
        """
        if(self.active_event):
            if(self.active_event.time_left):
                self.active_event.perform()
            else:
                self.windows_controller.remove_personal_event(self.active_event)
                self.active_event.reset()
                self.active_event = self.__get_new_event()
                self.windows_controller.add_personal_event(self.active_event)
                print "se disparó el evento: ", self.active_event.name
                if(self.active_event.kid_message):
                    self.windows_controller.show_kid_message(self.active_event.kid_message, self.active_event.message_time_span)
 
        else:
            self.active_event = self.__get_new_event()
            self.windows_controller.add_personal_event(self.active_event)
            print "se disparó el evento: ", self.active_event.name
            if(self.active_event.kid_message):
                self.windows_controller.show_kid_message(self.active_event.kid_message, self.active_event.message_time_span)
            print "se disparó el evento: ", self.active_event.name
    
    def __get_new_event(self):
        """
        Get a random event
        """
        rand = random.randint(0, self.max_rand)
        for i in range(0, len(self.probability_ranges)):
            if(rand >= self.probability_ranges[i][0] and rand <= self.probability_ranges[i][1]):
                return self.events_list[i]
            
    def __calculate_max_rand(self, events_list):
        """
        Calculates the max random number
        """
        max_rand = 0
        for event in events_list:
            max_rand += event.appereance_probability
        return max_rand
    
    def __calculate_ranges(self, events_list):
        """
        Calculate a probability range for each event and returns
        a list of ranges
        """
        previous = 0
        ranges = []
        for event in events_list:
            ranges += [(previous, previous + event.appereance_probability)]
            previous += event.appereance_probability + 1
        return ranges
    
    
    
    
    
    


