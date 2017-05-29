from Pos import Pos


def put_strategy(game):
    # Check if there is a dooz opportunity
    for line in game.get_lines():
        my_cells_in_line = [game.get_board().get_cell(i[0], i[1]) for i in line if
                            game.get_board().get_cell(i[0], i[1]) in game.get_board().get_mycells()]
        empty_cells_in_line = [game.get_board().get_cell(i[0], i[1]) for i in line if
                               game.get_board().get_cell(i[0], i[1]) in game.get_board().get_emptycells()]
        if len(my_cells_in_line) == 2 and len(empty_cells_in_line) == 1:
            # We can dooz, so do it
            return game.put(empty_cells_in_line[0].get_pos())

    # No dooz opportunity found
    # Check if the enemy can dooz
    for line in game.get_lines():
        opp_cells_in_line = [game.get_board().get_cell(i[0], i[1]) for i in line if
                               game.get_board().get_cell(i[0], i[1]) in game.get_board().get_oppcells()]
        empty_cells_in_line = [game.get_board().get_cell(i[0], i[1]) for i in line if
                               game.get_board().get_cell(i[0], i[1]) in game.get_board().get_emptycells()]
        if len(opp_cells_in_line) == 2 and len(empty_cells_in_line) == 1:
            # Enemy can dooz, stop him!
            return game.put(empty_cells_in_line[0].get_pos())

    # No opportunity for us & enemy
    # Put randomly
    if game.get_board().get_emptycells():
        return game.put(game.get_board().get_emptycells()[0].get_pos())
