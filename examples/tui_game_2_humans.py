from pylgrum.tui.tui_game import TUIGame
from pylgrum.tui.tui_player import TUIPlayer

print("""
This is a two-player console-mode game of Gin Rummy. It can be used for
testing, or if the screen can be exchanged privately between two players
for a real game.
""")

p1_name = input("Enter a name for player 1: ")
p2_name = input("Enter a name for player 2: ")

p1 = TUIPlayer(p1_name)
p2 = TUIPlayer(p2_name)

game = TUIGame(p1, p2)

game.play()
