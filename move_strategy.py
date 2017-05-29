from Pos import Pos
from Checker import Checker


def move_strategy(game):
    print('\nCycle #', game.get_cycle())
    print('Move strategy')

    # Check if there is a dooz opportunity
    for line in game.get_lines():
        my_cells_in_line = [game.get_board().get_cell(i[0], i[1]) for i in line if
                            game.get_board().get_cell(i[0], i[1]) in game.get_board().get_mycells()]
        empty_cells_in_line = [game.get_board().get_cell(i[0], i[1]) for i in line if
                               game.get_board().get_cell(i[0], i[1]) in game.get_board().get_emptycells()]

        if len(my_cells_in_line) == 2 and len(empty_cells_in_line) == 1:
            empty_cell_neighbors = game.get_neighbors()[(empty_cells_in_line[0].get_pos().getx(),
                                                         empty_cells_in_line[0].get_pos().gety())]
            my_cells_in_line = [(i.get_pos().getx(), i.get_pos().gety()) for i in my_cells_in_line]
            empty_cell_neighbors = [i for i in empty_cell_neighbors if i not in my_cells_in_line]
            print('Dooz opportunity found:')
            print('(%d, %d)' % (empty_cells_in_line[0].get_pos().getx(),
                                empty_cells_in_line[0].get_pos().gety()))
            print('Neighbors:', empty_cell_neighbors)
            for cell in empty_cell_neighbors:
                if cell in [(i.get_pos().getx(), i.get_pos().gety()) for i in game.get_board().get_mycells()]:
                    print('Moving ', cell)
                    return game.move(game.get_board().get_cell(cell[0], cell[1]).get_checker(),
                                     empty_cells_in_line[0].get_pos())
            print('No neighbor found')

    print('No dooz opportunity found')
