from Pos import Pos
from utils import log
import random


def put_strategy(game):
    if game.get_cycle() > 2:
        log()
    log('Cycle #', game.get_cycle())
    log('Started put strategy')

    # Check if there is a dooz opportunity
    my_opps = game.dooz_opportunities(game.get_my_positions(), by_putting=True)
    if my_opps:
        log('Dooz opportunities found:', my_opps)
        log('Putting on', my_opps[0])
        return game.put(Pos(my_opps[0][0], my_opps[0][1]))  # TODO choose the best dooz opportunity

    # No dooz opportunity found
    # Check if the enemy can dooz and we can surely prevent it
    enemy_opps = game.dooz_opportunities(game.get_opp_positions(), by_putting=True)
    if len(enemy_opps) == 1:
        log('Enemy has only 1 dooz opportunity:', enemy_opps[0], 'preventing it.')
        return game.put(Pos(enemy_opps[0][0], enemy_opps[0][1]))

    # Enemy has more than 1 dooz opportunity or has none
    # Try to find a two-way
    for empty_pos in game.get_empty_positions():
        my_opps = game.dooz_opportunities(game.get_my_positions() + [empty_pos], by_putting=True)
        if len(my_opps) > 1:
            # We've created a two-way
            log('Can create a two-way by putting on', empty_pos)
            log('These opportunities will be created:', my_opps)
            return game.put(Pos(empty_pos[0], empty_pos[1]))  # TODO choose the best two-way

    # Couldn't find a two-way
    # create a simple dooz opportunity
    for empty_pos in game.get_empty_positions():
        my_opps = game.dooz_opportunities(game.get_my_positions() + [empty_pos], by_putting=True)
        if len(my_opps) > 0:
            # We've created a opportunity
            log('Can create a simple opportunity by putting on', empty_pos)
            log('These opportunities will be created:', my_opps)
            return game.put(Pos(empty_pos[0], empty_pos[1]))  # TODO choose the best opportunity

    # TODO combine finding one-ways and two-ways

    # Put randomly
    if game.get_board().get_emptycells():
        the_random = random.choice(game.get_board().get_emptycells())
        log('Put randomly on', the_random.get_pos().getx(), the_random.get_pos().gety())
        return game.put(the_random.get_pos())
