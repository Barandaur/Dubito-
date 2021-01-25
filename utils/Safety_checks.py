# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 12:10:52 2021

@author: Eugenio
"""
import numpy as np
import random as random
import re

import sys, os
#import degli altri script
path_to_classes =  os.getcwd() +  r"\Classi"  # os.getcwd() + 
sys.path.append(path_to_classes)

from Cards  import *
from Player import *
from Game   import *


def safety_checks_Deck():
    """ Some (not thourough) checks that cards are correctly
        distributed among players, and that the pool gets correctly
        expanded and reset """

    c = Cards(3)  

    hand1 = c.draw()
    hand2 = c.draw()
    hand3 = c.draw()
    assert len(hand1) == len(hand2) == len(hand3)

    len_hand = len(hand1)
    c.add_to_pool(hand1)
    assert len(c.pool) == len_hand, "Error in adding cards to the pool"

    c.reset_pool()
    assert not c.pool
    
    return


def safety_checks_Player():
    """ Checks that, when invalid cards are passed as argument to
        'play_cards', no card actually gets played.
        Checks that all cards correctly get played """
    
    c = Cards(2)
    p1 = Player(c, 0)
    p2 = Player(c, 1)
    
    p1.add_to_hand(c.draw())
    p2.add_to_hand(c.draw())

    len_p1_hand = len(p1.hand)
    len_p2_hand = len(p2.hand)
    assert len_p1_hand == len_p1_hand, "Errore in fase di pesca"

    p1.play_cards([22222, 23313, 34414])
    assert len_p1_hand == len(p1.hand), "Some cards were played despite none should have been played"

    p1.play_cards([i for i in p1.hand])
    assert len(p1.hand) == 0, "Non sono state giocate tutte le carte che avrebbero dovuto essere giocate"

    p2.play_cards([i for i in p2.hand][:1] + [32313231])
    assert len(p2.hand) == len_p2_hand-1, "Sono state sbagliate le carte giocate"