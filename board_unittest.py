import board

b = board.Board()

# case 1
b.figs['white']['p5'] = 'a3'
b.figs['white']['n1'] = 'c3'
b.figs['white']['b2'] = 'f3'
b.figs['white']['n2'] = 'h3'
b.figs['white']['q'] = 'd4'
b.figs['black']['q'] = 'a6'

for fig in b.figs['white']:
	print(fig, ':', b.get_moves('white', fig))
