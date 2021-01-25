# -*- coding: utf-8 -*-
"""
Contiene la classe Cards, per gestire il mazzo,
e la funzione safety_checks_Deck, per effettuare
alcuni controlli base sulla classe

@author: Eugenio
"""
import numpy as np
import random as random
import re
import time


class Cards:
    def __init__(self, num_players, jolly = 100):
        self.num_players = num_players
        self.to_draw = 0 
        self.deck = []
        self.pool = [] 
        self.jolly = jolly
        
        assert isinstance(jolly, int), "Il Jolly deve essere un numero"
        assert isinstance(num_players, int), "num_players non è un numero"
        
        self.create_deck()
    
    def create_deck(self):
        """ Crea un deck con 4 copie di ogni carta (una per seme)
            e 4 jolly, indicati per convenzione col numero 100 """
        
        self.deck = np.array([i for i in range(1,14)]*4 +[self.jolly]*4, dtype=int)
        if self.num_players > 5:
            self.deck = np.array[list(self.deck) + list(self.deck)]
        
        self.to_draw = len(self.deck)//self.num_players
        self.shuffle()
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def add_to_pool(self, cards):
        self.pool += list(cards)
        
    def reset_pool(self):
        self.pool = []
        print("Le carte sono state prese o rimosse dal pozzo")
        
                
    def draw(self):
        """ draw an equal amount of cards from the deck for each player.
            Return the cards extracted for one player, while removing
            them from the Deck.
            Note: requires that the Deck remains shuffled"""
        
        # safety check
        assert len(self.deck) >= self.to_draw, "There are not enough cards to draw!"
        
        # extracted cards
        #extracted = np.random.choice(self.deck, self.to_draw, replace = False)
        extracted = self.deck[:self.to_draw]
        
        # remove them from deck
        #self.deck = np.array([i for i in self.deck if i not in extracted])
        self.deck = self.deck[self.to_draw:]
        
        return extracted
    
    
  