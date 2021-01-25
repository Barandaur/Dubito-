# -*- coding: utf-8 -*-
"""
Contiene la classe Player, per gestire il mazzo,
e la funzione safety_checks_Deck, per effettuare
alcuni controlli base sulla classe

@author: Eugenio
"""

import numpy as np
import random as random
import re
import time


class Player:
    def __init__(self, deck, id_):
        self.hand = []
        self.deck = deck
        self.id_ = id_
        
    def add_to_hand(self, cards):       
        # volendo puoi sovrascrivere __iadd__ per poter operare comodamente con np arrays
        self.hand += list(cards)
    
    def show_hand(self):
        print("Le tue carte sono: ", sorted(self.hand))
    
    def reset_hand(self):
        self.hand = []
        
    def play_cards(self, cards):
        """ Input: cards -> list.
            Purpose: remove from hand the cards played, 
            and add them to the pool. 
            Controls that each card played is actually in hand,
            otherwise disregards them"""
        
        # remove each played card from the hand, if present, and keep in cards the cards actually played
        cards = [(self.hand.remove(num),num)[1] for _i, num in enumerate(cards) if num in self.hand ]
        add_to_pool = self.deck.add_to_pool(cards)
        
        return cards
    
    
    
