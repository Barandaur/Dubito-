import numpy as np
import random as random
import re
import time
from Cards  import *
from Player import *

class Game:
    def __init__(self, num_players):
        self.Deck = Cards(num_players)
        self.num_players = num_players
        self.players = [Player(self.Deck, id_=i) for i in range(1, num_players+1)] 
        
        # a cosa corrisponde il jolly?
        self.jolly = 100
        
        self.turn = 0       
        self.player = 0
        self.consec_passes = 0
        
        self.need_to_declare = True
        
        self.decl_istr  = "Dichiara il tipo di carta che andrà giocata (il numero, non il seme): "
        self.playc_istr = "Inserire il numero di ogni carta che vuoi buttare, separando ogni carta con spazi o virgole: "
        self.doubt_istr = "Insert the number of the player who wants to doubt, if any. Otherwise just press enter: "
        
        self.play()
     
    def first_draw(self):
        for id_ in range(self.num_players):
            player = self.players[id_]
            player.add_to_hand(self.Deck.draw())
        
    def advance_turn(self):
        self.turn += 1
        if self.turn >= self.num_players:
            self.turn = 0
            
    def reset(self, loser=None):
        """
        Resetta pool, need_to_declare e il num di pass consecutivi.
        Se specificato il loser, egli pescherà il pozzo.

        Parameters
        ----------
        loser: istanza del player perdente

        Returns
        ----------
        """
        
        # reset all relevant variables
        self.need_to_declare = True
        self.consecutive_passes = 0
        
        # eventually add pool to hand of loser and reset pool 
        if loser:
            loser.add_to_hand(self.Deck.pool)
        self.Deck.reset_pool()
        
        return
    
    def take_input(self, istrz, min_=0, max_=13, type_=int, none = False, no_self_doubt = False):
        """ Take an input, while controlling that it is
            within a numerical range or that it is of the
            right type, if the relative arguments are specified """
        
        while True:
            ui = input(istrz)
            
# se None è una risposta ammissibile e viene data, restituisci None
            if none == True and not ui:
                return ui
            
# here start checks about type, and min < ui < max, and self doubting
            if type_ is not None:
                try:
                    ui = type_(ui)
                except ValueError:
                    print("Input type must be {0}.".format(type_.__name__))
                    continue
            
            if no_self_doubt == True and ui == self.player.id_:
                print("One can't doubt his own play! :/")                
            elif max_ is not None and ui > max_:
                print("Input must be less than or equal to {0}.".format(max_))
            elif min_ is not None and ui < min_:
                print("Input must be greater than or equal to {0}.".format(min_))
            else:
                return ui
    
    
    def play_cards(self):
        """ ask the user for the cards he wants to play,
            take only those which he actually has in hand,
            use the Player class method to play the cards """
        
# request input cards to play from player x 
        self.player.show_hand()    
        # take input, split based on comma or whitespace, clean resulting empty strings
        #in the thus formed list (e.g. if one uses two whitespaces), convert to int, 
        cards_played = [int(carta) if int(carta) != self.jolly else self.card_declared \
                        for carta in \
                         list(filter(None, re.split(" |,|;", input(self.playc_istr)))) \
                         ]
        #cards_played = list(filter(lambda x:x in \
        #                            cards_to_play, \
        #                            self.player.hand))
        
# actually play the cards
        cards_played = self.player.play_cards(cards_played)

# informative prints
        if cards_played:
            print(f"player {self.player.id_} has played {len(cards_played)} {self.card_declared[0]}")
        else:
            print(f"player {self.player.id_} has passed its turn")  
        
        return cards_played
         
        
    def doubt(self, cards_played, who_doubted):
        
# if the player was honest, reset and give the pool to the doubter
        if cards_played == self.card_declared*len(cards_played):
            print("E invece il giocatore {} aveva effettivamente giocato {} {}!" \
                  .format(self.player.id_, len(cards_played), self.card_declared[0]))
            loser = self.players[who_doubted -1]
            self.reset(loser)
            #self.players[who_doubted -1].add_to_hand(self.Deck.pool)
            #self.Deck.reset_pool()
            return False

# if the player got correctly doubted, give him the first turn and the bluffer takes the cards
        else:
            print(f"Il giocatore {who_doubted} ha correttamente dubitato del giocatore {self.player.id_}!")
            loser = self.player
            self.reset(loser)
            #self.player.add_to_hand(self.Deck.pool)
            #self.Deck.reset_pool()
            return True

    def play(self):
        
        self.first_draw()
                
        while True:
            
            """---------------- define player ----------------"""
            
            self.player = self.players[self.turn]
            print("\n----------------------------------------")
            print(f"è il turno del giocatore {self.player.id_}")
            
            
            """---------------- play card ----------------"""
            
            if self.need_to_declare:
                print("Inizia un nuovo giro! Tagadà!")
                time.sleep(1)
                self.player.show_hand()
                # declare the card which will need to be played
                self.card_declared = [self.take_input(istrz=self.decl_istr)]
                self.need_to_declare = False
                
            print(f"La carta da giocare è il {self.card_declared[0]}")
            
            time.sleep(0.5)
            # play cards
            cards_played = self.play_cards()         
            
            """---------------- doubt ----------------"""
            
            time.sleep(1)
            who_doubted = None
            # se non è stato passato il turno, apri la fase di dubbio
            if cards_played:
                # if someone wants to doubt, insert his player number in this input
                who_doubted = self.take_input(self.doubt_istr, 
                                              min_= 0,
                                              max_=self.num_players,
                                              type_=int,
                                              none = True,
                                              no_self_doubt = True)
                if who_doubted:
                    correctness_doubt = self.doubt(cards_played, who_doubted)   
                    time.sleep(2.5)
            
            else: 
                self.consec_passes += 1
                if self.consec_passes >= self.num_players:
                    time.sleep(0.5)
                    print("Tutti i giocatori hanno passato!")
                    
                    self.reset()
                    self.consec_passes = 0
            
            """---------------- check victory ----------------"""
            
            if not self.player.hand:
                print(f"\n Player {self.player._id} has won the game, ggs! \n")
                return
            
            """---------------- manage turns ----------------"""
            
            # if there was a doubt, give the turn to the winner of the outcome
            if who_doubted and correctness_doubt == True:
                self.turn = who_doubted-1
                
            # else regularly advance the turn
            elif not who_doubted:
                self.advance_turn()
        
        return