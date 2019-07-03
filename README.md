# QL_Snake
Q learning snake

'main.py' is game + q learning, that saves best q_table, default generates new one, change q_table = None to filename to use existing one.
'main_playable.py' is game playable for player using arrow keys, only difference between playable and the one that algorithm uses is that playable moves with every frame whereas the one in 'main.py' moves when action is made. It makes to difference for q_learning but had to be changed for playable version.
