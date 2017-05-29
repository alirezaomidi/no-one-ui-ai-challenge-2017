from Pos import Pos
from log import log


def pop_strategy(game):
    log()
    log('Cycle #', game.get_cycle())
    log('Starting pop strategy...')

    # Check if by popping any of the enemy checkers, we can prevent enemy from doozing
    log('Checking if we can prevent enemy from doozing')
    for enemy_pos in game.get_opp_positions():
        cur_opps = game.dooz_opportunities([i for i in game.get_opp_positions() if i != enemy_pos])
        if not cur_opps:
            # pop the enemy_pos
            log('Popping', enemy_pos)
            return game.pop(game.get_board().get_cell(*enemy_pos).get_checker())

