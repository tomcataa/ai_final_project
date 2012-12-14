import GameBoard
import SmartAgent2
import SmartAgent
import GeniusAgent

g = GameBoard.GameBoard()
s1 = SmartAgent2.Agent('smart1', g)
s2 = SmartAgent2.Agent('smart2', g)
s3 = SmartAgent2.Agent('smart3', g)
genius = GeniusAgent.Agent('genius', g)
g.play()

