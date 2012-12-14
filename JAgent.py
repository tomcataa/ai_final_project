#-*- coding: utf-8 -*-
from GameBoard import *

class JAgent(Agent):
    #def __init__(self, name, gb):
    #    super(JAgent, self).__init__(name, gb) # 呼叫父類別
    
    
    def draw(self, keep=False):
        card = self.gb.drawCard()
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win_by_draw+=1
            print("\t[Test] Agent({0}) 自摸 {1}!".format(self.name, card))
            return

        prewin_tiles = GameBoard.PreWinTiles(self)
        if len(prewin_tiles) > 0:
            return card

        print("\t[Test] {0} draw {1}...".format(self.name, card))
        ctype = GameBoard.CardType(card)
        if ctype==1:
            self.wang_list.append(card)
            self.wang_list.sort()
            self.card_count+=1
        elif ctype==2:
            self.tube_list.append(card)
            self.tube_list.sort()
            self.card_count+=1
        elif ctype==3:
            self.bamb_list.append(card)
            self.bamb_list.sort()
            self.card_count+=1
        elif ctype==4:
            self.word_list.append(card)
            self.word_list.sort()
            self.card_count+=1
        elif ctype==5:
            self.wind_list.append(card)
            self.wind_list.sort()
            self.card_count+=1
        else:
            self.flow_list.append(card)
            self.flow_list.sort()
            return self.draw()

        dcard = None
        if not keep:
            dcard = self.drop()
            print("\t[Test] {0} drop {1}...".format(self.name, dcard))
            #self.gb.disCard(self, dcard)
        return dcard
    
    def __str__(self):
        self_str = "{0}({1}/{2}/{3}): [".format(self.name, self.win_by_draw, self.win, self.lose)
        for card in self.wang_list:
            self_str+="{0} ".format(card)
        self_str+="|"
        for card in self.tube_list:
            self_str+="{0} ".format(card)
        self_str+="|"
        for card in self.bamb_list:
            self_str+="{0} ".format(card)
        self_str+="|"
        for card in self.word_list:
            self_str+="{0} ".format(card)
        self_str+="|"
        for card in self.wind_list:
            self_str+="{0} ".format(card)    
        self_str = "{0}]".format(self_str)
        if len(self.flow_list) > 0:
            self_str+=" / [ "
            for card in self.flow_list:
                self_str+="{0} ".format(card)
            self_str+="]"
        else:
            self_str+=" / []"
        if len(self.pong_list) > 0:
            self_str+=" / [ "
            for card in self.pong_list:
                self_str+="{0} ".format(card)
            self_str+="]"
        else:
            self_str+=" / []"
            
        if self.win_card:
            self_str+=" -> {0}".format(self.win_card)
        else:
            prewin_tiles = GameBoard.PreWinTiles(self)
            if len(prewin_tiles) > 0:
                self_str+=" / 聽 {0}".format(toCListStr(prewin_tiles))    
        return self_str
        

    
