# -*- coding: utf-8 -*-

import gtk
from gettext import gettext as _

class StartupWindow(gtk.VBox):
    
    def __init__(self, start_cb):
        gtk.VBox.__init__(self, False)
        
        self.start_cb = start_cb
        self.set_welcome()

    def set_welcome(self):
        for child in self.get_children():
            self.remove(child)
        
        self.add(Welcome(self.start_cb, self._new_game, self._load_last_game, self._load_game))
        self.show_all()
        
    def _new_game(self, button):
        for child in self.get_children():
            self.remove(child)
        
        self.add(SelectGenderAndName(self._gender_selected))
    
    def _load_last_game(self, button):
        pass
    
    def _load_game(self, button):
        pass
    
    def _gender_selected(self, name, gender, grade = 3):
        for child in self.get_children():
            self.remove(child)
        
        self.add(Introduction(self.start_cb))

class Welcome(gtk.Fixed):
    
    def __init__(self, start_cb, new_game_cb, load_last_game_cb, load_game_cb):
        gtk.Fixed.__init__(self)

        self.start_cb = start_cb
        
        image = gtk.Image()
        image.set_from_file("assets/slides/screen_mainmenu.jpg")
        self.put(image, 0, 0)
        
        btn_new = gtk.Button(_("New game"))
        btn_new.connect("clicked", new_game_cb)
        self.put(btn_new, 490, 386)
        
        btn_last_game = gtk.Button(_("Load last game"))
        btn_last_game.connect("clicked", load_last_game_cb)
        self.put(btn_last_game, 490, 500)
        
        btn_load_game = gtk.Button(_("Load game from journal"))
        btn_load_game.connect("clicked", load_game_cb)
        self.put(btn_load_game, 490, 620)

        self.show_all()

class SelectGenderAndName(gtk.Fixed):
    
    def __init__(self, callback):
        gtk.Fixed.__init__(self)
        
        self.callback = callback
        
        image = gtk.Image()
        image.set_from_file("assets/slides/screen_name_and_gender.jpg")
        self.put(image, 0, 0)

        self.kid_name = gtk.Entry()
        self.put(self.kid_name, 225, 150)
        
        btn_boy = gtk.Button(_("Boy"))
        btn_boy.connect("clicked", self._boy)
        btn_boy.set_size_request(-1, 24)
        self.put(btn_boy, 220, 285)
        
        btn_girl = gtk.Button(_("Girl"))
        btn_girl.connect("clicked", self._girl)
        btn_girl.set_size_request(-1, 24)
        self.put(btn_girl, 750, 285)
        
        self.show_all()
        
    def _boy(self, button):
        self.callback(self.kid_name.get_text(), "boy")

    def _girl(self, button):
        self.callback(self.kid_name.get_text(), "girl")


story = [
    
    #Slide1
    {
        "image": "assets/slides/history1.jpg",
        "text": None
    },
    
    #Slide2
    {
        "image": "assets/slides/history2.jpg",
        "text": None
    },

    #Slide3
    {
        "image": "assets/slides/help.png",
        "text": None
    },
    
]

class Introduction(gtk.Fixed):
    
    def __init__(self, callback):
        gtk.Fixed.__init__(self)
        
        self.callback = callback
        
        self.index = 0
        
        self.show_slide()
        
    
    def show_slide(self):
        
        for child in self.get_children():
            self.remove(child)
            
        slide = story[self.index]
        
        # Image
        image = gtk.Image()
        image.set_from_file(slide["image"])
        self.put(image, 0, 0)
        
        # Text
        if slide["text"]:
            text_view = gtk.TextView()
            text_buffer = text_view.get_buffer()
            text_buffer.set_text(slide["text"])
            text_view.set_wrap_mode(gtk.WRAP_WORD)
            self.pack_start(text_view, False, False)
        
        # HBox with buttons
        hbox = gtk.HBox(False)
        btn_back = gtk.Button(_("< Back"))
        btn_back.connect("clicked", self._back)
        btn_back.set_size_request(-1, 24)
        hbox.pack_start(btn_back)
        if self.index == 0:
            btn_back.set_sensitive(False)
        
        btn_next = gtk.Button(_("Next >"))
        btn_next.connect("clicked", self._next)
        btn_next.set_size_request(-1, 24)
        hbox.pack_start(btn_next)
        self.put(hbox, 0, 0)
        
        self.show_all()
        
    def _next(self, button):
        if self.index + 1 < len(story):
            self.index += 1
            self.show_slide()
        else:
            self.callback()
        
    def _back(self, button):
        if self.index > 0:
            self.index -= 1
            self.show_slide()
        