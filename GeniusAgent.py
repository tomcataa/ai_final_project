#-*- coding: utf-8 -*-
from GameBoard import GameBoard
from GameBoard import toCListStr

class Agent:
	def __init__(self, name, gb):
		self.win = 0                # 記錄胡場數
		self.win_by_draw = 0        # 紀錄自摸場數
		self.lose = 0               # 紀錄放槍場數
		self.name = name            # Agent 的名字
		self.gb = gb                # GameBoard 實例.
		self.bamb_list = []         # 條子
		self.wang_list = []         # 萬子
		self.tube_list = []         # 筒子
		self.flow_list = []         # 花牌
		self.word_list = []         # 中發白
		self.wind_list = []         # 風牌       
		self.pong_list = []         # 吃/碰 的排組
		self.card_count = 0         # 手上剩餘牌數
		self.win_card = None        # 贏的時候的那張牌
		gb.appendAgent(self)        # 將 Agent 加入 GameBoard
		self.wrong = False          # Wrong flag
		self.pwin_flag = False      # Enter pre-win state
	
	# Drop all cards in hand
	def clean(self):
		del self.bamb_list[:]
		del self.wang_list[:]
		del self.tube_list[:]
		del self.flow_list[:]
		del self.word_list[:]
		del self.wind_list[:]
		#del self.aget_list[:]
		del self.pong_list[:]
		self.card_count = 0
		self.pwin_flag = False

	def _isPrewin(self):
		prewin_tiles = GameBoard.PreWinTiles(self)
		if len(prewin_tiles) > 0:
			for tile in prewin_tiles:
				ctype = GameBoard.CardType(tile)
				if ctype == 1:
					if tile in self.gb.wang_list:
						return True
				elif ctype == 2:
					if tile in self.gb.tube_list:
						return True
				elif ctype == 3:
					if tile in self.gb.bamb_list:
						return True
				elif ctype == 4:
					if tile in self.gb.word_list:
						return True
				elif ctype == 5:
					if tile in self.gb.wind_list:
						return True

	# 抽牌
	# 1. 使用 self.gb.drawCard() 從牌桌抽一張牌.
	# 2. 檢查是否滿足 Goal State (自摸).
	#    2.1 如果已經聽牌, 則打出抽到的牌.
	# 3. 檢查是否可以槓
	#    3.1 如果槓, 可以再抽一張.
	# 4. 選擇要放棄的牌.
	def draw(self, keep=False):
		card = self.gb.drawCard()
		print "\tdraw: {0}".format(card)
		prewin_tiles = GameBoard.PreWinTiles(self)
		if card in prewin_tiles:
		#if GameBoard.GoalState(self, card): # Check goal state
			self.gb.win_agent = self
			self.win_card = card
			self.win_by_draw+=1
			#print("\t[Test] Agent({0}) 自摸 {1}!".format(self.name, card))
			return       
		elif len(prewin_tiles) > 0:
			self.pwin_flag = True
			for tile in prewin_tiles:
				ctype = GameBoard.CardType(tile)
				if ctype == 1:
					if tile in self.gb.wang_list:
						return card 
				elif ctype == 2:
					if tile in self.gb.tube_list:
						return card
				elif ctype == 3:
					if tile in self.gb.bamb_list:
						return card
				elif ctype == 4:
					if tile in self.gb.word_list:
						return card
				elif ctype == 5:
					if tile in self.gb.wind_list:
						return card
		
		#print("\t[Test] {0} draw {1}...".format(self.name, card))
		ctype = GameBoard.CardType(card)
		if ctype==1:
			if self.wang_list.count(card)==3: # 確認槓牌
				self._kong(ctype, card)
				return self.draw()
			self.wang_list.append(card)            
			self.wang_list.sort()
			self.card_count+=1
		elif ctype==2:
			if self.tube_list.count(card)==3: # 確認槓牌
				self._kong(ctype, card)
				return self.draw()
			self.tube_list.append(card)
			self.tube_list.sort()
			self.card_count+=1
		elif ctype==3:
			if self.bamb_list.count(card)==3: # 確認槓牌
				self._kong(ctype, card)
				return self.draw()
			self.bamb_list.append(card)
			self.bamb_list.sort()
			self.card_count+=1
		elif ctype==4:
			if self.word_list.count(card)==3: # 確認槓牌
				self._kong(ctype, card)
				return self.draw()                
			self.word_list.append(card)
			self.word_list.sort()
			self.card_count+=1
		elif ctype==5:
			if self.wind_list.count(card)==3: # 確認槓牌
				self._kong(ctype, card)
				return self.draw()
			self.wind_list.append(card)
			self.wind_list.sort()
			self.card_count+=1
		else:
			self.flow_list.append(card)
			self.flow_list.sort()
			return self.draw()            

		dcard=None     
		if not keep:
			dcard = self.drop()
			#print("\t[Test] {0} drop {1}...".format(self.name, dcard))
			#self.gb.disCard(self, dcard)
		if (len(self.word_list)%3+len(self.wind_list)%3+len(self.tube_list)%3+len(self.wang_list)%3+len(self.bamb_list)%3) == 0:
			self.wrong = True
		return dcard

	def find_all_combination(self, ctype, cards, comb_str, combination):
		if len(cards) == 0:
			combination.append(comb_str)
			return combination
		card = cards[0]
		ctype = GameBoard.CardType(card)
		if (ctype == 1) or (ctype == 2) or (ctype == 3):
			count = cards.count(card)
			if count == 3:
				copy = list(cards)
				copy.remove(card)
				copy.remove(card)
				copy.remove(card)
				new = "{0} {0} {0}\t".format(card)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			if count == 2:
				copy = list(cards)
				copy.remove(card)
				copy.remove(card)
				new = "{0} {0}\t".format(card)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			n = GameBoard.NextCard(card)
			if n != None: nn = GameBoard.NextCard(n)
			else: nn = ""
			if (n in cards) and (nn in cards):
				copy = list(cards)
				copy.remove(card)
				copy.remove(n)
				copy.remove(nn)
				new = "{0} {1} {2}\t".format(card, n, nn)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			if n in cards:
				copy = list(cards)
				copy.remove(card)
				copy.remove(n)
				new = "{0} {1}\t".format(card, n)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			if nn in cards:
				copy = list(cards)
				copy.remove(card)
				copy.remove(nn)
				new = "{0} {1}\t".format(card, nn)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			cards.remove(card)
			new = "{0}\t".format(card)
			self.find_all_combination(ctype, cards, comb_str + new, combination)

		if (ctype == 4) or (ctype == 5):
			count = cards.count(card)
			if count == 3:
				copy = list(cards)
				copy.remove(card)
				copy.remove(card)
				copy.remove(card)
				new = "{0} {0} {0}\t".format(card)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			if count == 2:
				copy = list(cards)
				copy.remove(card)
				copy.remove(card)
				new = "{0} {0}\t".format(card)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			cards.remove(card)
			new = "{0}\t".format(card)
			self.find_all_combination(ctype, cards, comb_str + new, combination)

		return combination

	def way_to_prewin(self, one):
		"""
		[triple, pair, neighbor, single]
		"""
		kind = [0, 0, 0, 0] 
		useful = set()
		for part in one.split("\t"):
			#print "part: {0}".format(part)
			tmp = part.split()
			length = len(tmp)
			if (length == 3):
				kind[0] += 1
			elif (length == 1):
				kind[3] += 1
			elif (tmp[0] == tmp[1]): # pair
				kind[1] += 1
				useful.add("{0}".format(tmp[0]))
			else:
				kind[2] += 1
				n = GameBoard.NextCard(tmp[0])
				if (n == tmp[1]): # consecutive neighbor
					p = GameBoard.PrevCard(tmp[0])
					if (p != None): useful.add(p)
					nn = GameBoard.NextCard(tmp[1])
					if (nn != None): useful.add(nn)
				else:
					useful.add(n)

		#print "kind: {0}".format(kind)
		#print "useful: {0}".format(" ".join(useful))
		"""
		1. enumerate, because goal state not too much
		2. counting pong_list so that we can focus on 16 cards
		3. chech prewin first	
		"""
		goals = [[4, 1, 1, 0], [5, 0, 0, 1], [4, 2, 0, 0]]
		gpattern = [["***", "***", "***", "***", "##", "$$"],["***", "***", "***", "***", "***", "/"],
					["***", "***", "***", "***", "##", "##"]]
		result = [0, 0, 0]
		size = len(self.pong_list) / 3
		if ((size + kind[0]) > 4): return 0, 0, len(useful)
		for i in range(size): 
			gpattern[0].remove("***")
			gpattern[1].remove("***")
			gpattern[2].remove("***")
		for number in range(3):
			k0 = kind[0]
			k1 = kind[1]
			k2 = kind[2]
			k3 = kind[3]
			p1 = gpattern[number]
			for i in range(k0): p1.remove("***")
			for i in range(min(k1, goals[number][1])): 
				k1 -= 1
				p1.remove("##")
			for i in range(min(k2, goals[number][2])):
				k2 -= 1
				p1.remove("$$")
			#print "p1: {0}, size: {1}".format(p1, (k1+k2)*2+k3)
			step = 0
			two = k1 + k2
			for i in range(len(p1)):
				length = len(p1[i])
				if (length == 3):
					if two:
						two -= 1
						step += 1
					else:
						step += 2
				elif (length == 2):
					step += 1
			result[number] = step
		#print "steps to goal: {0}, useful: {1}".format(result, len(useful))
		
		return min(result), max(result), len(useful)

	def count_steps(self):
		wang_combination = self.find_all_combination(1, list(self.wang_list), "", [])
		tube_combination = self.find_all_combination(2, list(self.tube_list), "", [])
		bamb_combination = self.find_all_combination(3, list(self.bamb_list), "", [])
		word_combination = self.find_all_combination(4, list(self.word_list), "", [])
		wind_combination = self.find_all_combination(5, list(self.wind_list), "", [])
		all_combination = []
		size = 0
		for w in wang_combination:
			for t in tube_combination:
				for b in bamb_combination:
					for wo in word_combination:
						for wi in wind_combination:
							all_combination.append("{0}{1}{2}{3}{4}".format(w, t, b, wo, wi))
							size += 1
		#total_mini = 0
		#total_maxi = 0
		#total_useful = 0
		mini = 99
		maxi = 0
		useful = 0
		for i in range(size):
			one = all_combination[i]
			#print "one: {0}".format(one)
			a, b, c = self.way_to_prewin(one.strip())
			if (a < mini): mini = a
			if (b > maxi): maxi = b
			if (c > useful): useful = c
			#print "min: {0}, max: {1}, useful: {2}".format(a, b, c)
			#exit(1)
			#total_mini += a
			#total_maxi += b
			#total_useful += c
		"""
		average situation
		"""
		#print "total: [{0}, {1}, {2}], size: {3}".format(total_mini, total_maxi, total_useful, size)
		#avg = [(total_mini/size), (total_maxi/size), (total_useful/size)]
		#return avg
		return mini, maxi, useful
			
	def drop(self):
		"""
		try to discard every card to find the best
		"""
		result = []
		all_cards = [self.wang_list, self.tube_list, self.bamb_list, self.word_list, self.wind_list]
		for cards in all_cards:
			for i in range(len(cards)):
				c = cards.pop(i)
				mm, MM, useful = self.count_steps()
				cards.insert(i, c)
				result.append([mm, MM, useful, c])
				#print "min: {0}, max: {1}, useful: {2}, dcard: {3}".format(mm, MM, useful, c)
		sort_result = sorted(result, key=lambda r: r[0])
		# sorting first rule
		flag = False
		m = sort_result[0][0]
		for i in range(len(sort_result)):
			if (sort_result[i][0] != m): 
				flag = True
				break
		# sorting second rule
		if not flag: i += 1
		sub = sort_result[:i]
		sort_sub = sorted(sub, key=lambda r: r[1], reverse=True)
		flag = False
		m = sort_sub[0][1]
		for i in range(len(sort_sub)):
			if (sort_sub[i][1] != m): break
		# sorting third rule
		if not flag: i += 1
		ssub = sort_sub[:i]
		sort_ssub = sorted(ssub, key=lambda r: r[2], reverse=True)
		# choose one
		dcard = sort_ssub[0][3]
		m = sort_ssub[0][2]
		for r in sort_ssub:
			if (r[2] != m): break
			ctype = GameBoard.CardType(r[3])
			if (ctype == 4) and (self.word_list.count(r[3]) == 1): dcard = r[3]
			if (ctype == 5) and (self.wind_list.count(r[3]) == 1): dcard = r[3]
		print "\tdiscard: {0}".format(dcard)
		#exit(1)
		ctype = GameBoard.CardType(dcard)
		all_cards[ctype-1].remove(dcard)
		self.card_count -= 1
		return dcard

	def _pong(self, c_list, count, card):        
		for i in range(count+1):
			self.pong_list.append(card)
			
		for i in range(count):
			c_list.remove(card)
			self.card_count-=1
		
		if count==2:
			dcard = self.drop()
			#print("\t[Test] {0}: Pong '{1}' and drop {2}!".format(self.name, card, dcard))
			#self.gb.disCard(self, dcard)
			return dcard
		else:
			#print("\t[Test] {0}: Gong '{1}'!".format(self.name, card))
			return self.draw()
		
	# 碰! A callback by GameBoard. Return drop card or redraw card if you want.    
	def pong(self, agent, ctype, count, card):
		if GameBoard.GoalState(self, card): # Check goal state
			self.gb.win_agent = self
			self.win_card = card
			self.win+=1
			agent.close+=1
			#print("\t[Test] Agent({0}) 碰胡 {1}!!".format(self.name, card))
			return
		#if self._isPrewin():
	#    return
		# Greedy algorithm: Always pong!
		if ctype==1:
			return self._pong(self.wang_list, count, card)                
		elif ctype==2:
			return self._pong(self.tube_list, count, card)                
		elif ctype==3:
			return self._pong(self.bamb_list, count, card)                
		elif ctype==4:
			return self._pong(self.word_list, count, card)                
		elif ctype==5:
			return self._pong(self.wind_list, count, card)
				

	def _eat(self, olist, dlist, elist):
		self.pong_list.extend(elist)
		for e in dlist:
			olist.remove(e)
			self.card_count-=1
		dcard = self.drop()
		#print("\t[Test] {0}: Eat '{1}' and drop {2}!".format(self.name, toCListStr(elist), dcard))
		#self.gb.disCard(self, dcard)
		return dcard

	# 吃牌. Callback by GameBoard
	def eat(self, agent, card, ctype, eat_list):
		if GameBoard.GoalState(self, card): # Check goal state
			self.gb.win_agent = self
			self.win_card = card
			self.win+=1
			agent.lose+=1
			#print("\t[Test] Agent({0}) 吃胡 {1}!".format(self.name, card))
			return
		if self._isPrewin():
			return
		# Greedy algorithm: Always eat from the first choice
		if ctype==1:
			return self._eat(self.wang_list, eat_list[0][0], eat_list[0][1])
		elif ctype==2:
			return self._eat(self.tube_list, eat_list[0][0], eat_list[0][1])
		elif ctype==3:
			return self._eat(self.bamb_list, eat_list[0][0], eat_list[0][1])

	# 將牌放入
	def _feedCard(self, card):
		ctype = GameBoard.CardType(card)
		if ctype==1:
			self.wang_list.append(card)
			self.wang_list.sort()
			self.card_count+=1
			return True
		elif ctype==2:
			self.tube_list.append(card)
			self.tube_list.sort()
			self.card_count+=1
			return True
		elif ctype==3:
			self.bamb_list.append(card)
			self.bamb_list.sort()
			self.card_count+=1
			return True
		elif ctype==4:
			self.word_list.append(card)
			self.word_list.sort()
			self.card_count+=1
			return True
		elif ctype==5:
			self.wind_list.append(card)
			self.wind_list.sort()
			self.card_count+=1
			return True
		else:
			self.flow_list.append(card)
			self.flow_list.sort()

	def _kong(self, ctype, card):
		#print("\t[Test] Agent({0}) 槓 {1}!".format(self.name, card))
		if ctype==1:
			while card in self.wang_list:
				self.wang_list.remove(card)
				self.pong_list.append(card)
			self.pong_list.append(card)
		elif ctype==2:
			while card in self.tube_list:
				self.tube_list.remove(card)
				self.pong_list.append(card)
			self.pong_list.append(card)
		elif ctype==3:
			while card in self.bamb_list:
				self.bamb_list.remove(card)
				self.pong_list.append(card)
			self.pong_list.append(card)
		elif ctype==4:
			while card in self.word_list:
				self.word_list.remove(card)
				self.pong_list.append(card)
			self.pong_list.append(card)
		elif ctype==5:
			while card in self.wind_list:
				self.wind_list.remove(card)
				self.pong_list.append(card)
			self.pong_list.append(card)
				
	def concealedKong(self):
		drawFlag = False
		if len(self.wang_list)>3:
			for e in set(self.wang_list):
				if self.wang_list.count(e)==4:
					self.pong_list.extend([e]*4)
					while e in self.wang_list:
						self.wang_list.remove(e)
						self.card_count-=1
					while not self._feedCard(self.gb.drawCard()):
						pass # 直到抽到不是花牌
					self.wang_list.sort()
					#self.card_count+=1
					drawFlag=True
					
		if len(self.tube_list)>3:
			for e in set(self.tube_list):
				if self.tube_list.count(e)==4:
					self.pong_list.extend([e]*4)
					while e in self.tube_list:
						self.tube_list.remove(e)
						self.card_count-=1
					while not self._feedCard(self.gb.drawCard()):
						pass # 直到抽到不是花牌                    
					self.tube_list.sort()
					#self.card_count+=1
					drawFlag=True
					
		if len(self.bamb_list)>3:
			for e in set(self.bamb_list):
				if self.bamb_list.count(e)==4:
					self.pong_list.extend([e]*4)
					while e in self.bamb_list:
						self.bamb_list.remove(e)
						self.card_count-=1
					while not self._feedCard(self.gb.drawCard()):
						pass # 直到抽到不是花牌
					self.bamb_list.sort()
					#self.card_count+=1
					drawFlag=True
					
		if len(self.word_list)>3:
			for e in set(self.word_list):
				if self.word_list.count(e)==4:
					self.pong_list.extend([e]*4)
					while e in self.word_list:
						self.word_list.remove(e)
						self.card_count-=1
					while not self._feedCard(self.gb.drawCard()):
						pass # 直到抽到不是花牌
					self.word_list.sort()
					#self.card_count+=1
					drawFlag=True
					
		if len(self.wind_list)>3:
			for e in set(self.wind_list):
				if self.wind_list.count(e)==4:
					self.pong_list.extend([e]*4)
					while e in self.wind_list:
						self.wind_list.remove(e)
						self.card_count-=1
					while not self._feedCard(self.gb.drawCard()):
						pass # 直到抽到不是花牌
					self.wind_list.sort()
					#self.card_count+=1
					drawFlag=True
					
		if drawFlag:
			self.concealedKong()
			
	# 發牌        
	def assignCard(self):
		# 抽滿 16 張牌(扣掉花牌)
		while self.card_count < 16:
			card = self.gb.drawCard()
			self._feedCard(card)
			#print('\t[Test] card={0}, {1}'.format(card, self.card_count))
				
		# 處理槓牌
		self.concealedKong()
		if self.card_count != (16-3*len((set(self.pong_list)))):
			#print('\t[Test] Conceal kong error: {0}'.format(self))
			self.wrong = True
					
			
	def __str__(self):
		self_str = "{0}({1}/{2}/{3}): [".format(self.name, self.win_by_draw, self.win, self.lose)
		for card in self.wang_list:
			self_str+="{0} ".format(card)
		for card in self.tube_list:
			self_str+="{0} ".format(card)
		for card in self.bamb_list:
			self_str+="{0} ".format(card)
		for card in self.word_list:
			self_str+="{0} ".format(card)
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


