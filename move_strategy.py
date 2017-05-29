from log import log
from Pos import Pos


def move_strategy(game):
    log()
    log('Cycle #', game.get_cycle())
    log('Starting move strategy...')

    # Check if there is a dooz opportunity
    my_opps = game.dooz_opportunities(game.get_my_positions())
    if my_opps:
        log('Dooz opportunities found')
        log('Checking if we can dooz by moving')
        for pos in my_opps:
            my_neis = [i for i in game.get_neighbors()[pos] if i in game.get_my_positions()]
            if my_neis:
                log('Doozing by moving', my_neis[0], 'to', pos)  # TODO choose the best instead of the first
                return game.move(game.get_board().get_cell(*my_neis[0]).get_checker(), Pos(*pos))

    # Check if we can prevent the enemy from doozing
    enemy_opps = game.dooz_opportunities(game.get_opp_positions())
    if len(enemy_opps) == 1:
        log('Enemy has only one opportunity to dooz. Trying to prevent...')
        for pos in enemy_opps:
            my_neis = [i for i in game.get_neighbors()[pos] if i in game.get_my_positions()]
            if my_neis:
                log('Can prevent the dooz by moving', my_neis[0], 'to', pos)
                return game.move(game.get_board().get_cell(*my_neis[0]).get_checker(), Pos(*pos))

    # Get out of current dooz and get back to it in the next cycle
    for line in game.get_lines():
        if len([i for i in line if i in game.get_my_positions()]) == 3:
            log('Checking if we can move a checker out from dooz', line)
            for pos in line:
                empty_neis = [i for i in game.get_neighbors()[pos] if i in game.get_empty_positions()]
                if empty_neis:
                    log('Moving', pos, 'to', empty_neis[0])
                    return game.move(game.get_board().get_cell(*pos).get_checker(), Pos(*empty_neis[0]))
