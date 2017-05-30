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
        return game.put(Pos(*my_opps[0]))  # TODO choose the best dooz opportunity

    # No dooz opportunity found
    # Check if the enemy can dooz and we can surely prevent it
    enemy_opps = game.dooz_opportunities(game.get_opp_positions(), by_putting=True)
    if len(enemy_opps) == 1:
        log('Enemy has only 1 dooz opportunity:', enemy_opps[0], 'preventing it.')
        return game.put(Pos(*enemy_opps[0]))

    # Enemy has more than 1 dooz opportunity or has none
    # Try to find a two-way
    log('Trying to find a two-way by 1 move')
    for empty_pos in game.get_empty_positions():
        my_opps = game.dooz_opportunities(game.get_my_positions() + [empty_pos], by_putting=True)
        if len(my_opps) > 1:
            # We've created a two-way
            log('Can create a two-way by putting on', empty_pos)
            log('These opportunities will be created:', my_opps)
            return game.put(Pos(*empty_pos))  # TODO choose the best two-way

    # Couldn't find a two-way
    # Try to put where it will make two-way in the future
    log('Trying to find a two-way by 2 moves')
    for empty_pos1 in game.get_empty_positions():
        for empty_pos2 in game.get_empty_positions():
            if empty_pos1 == empty_pos2:
                continue
            my_opps = game.dooz_opportunities(game.get_my_positions() + [empty_pos1, empty_pos2],
                                              by_putting=True)
            if len(my_opps) > 1:
                # We've created a two-way
                log('Can create a two-way by putting on', empty_pos1, '&', empty_pos2)
                log('These opportunities will be created:', my_opps)
                opps_with_pos1 = game.dooz_opportunities(game.get_my_positions() + [empty_pos1],
                                                         by_putting=True)
                opps_with_pos2 = game.dooz_opportunities(game.get_my_positions() + [empty_pos2],
                                                         by_putting=True)
                the_empty_pos_to_put = empty_pos1 if len(opps_with_pos1) < len(opps_with_pos2) else empty_pos2
                return game.put(Pos(*the_empty_pos_to_put))  # TODO choose the best two-way

    log('Trying to find a two-way by 3 moves')
    for empty_pos1 in game.get_empty_positions():
        for empty_pos2 in game.get_empty_positions():
            for empty_pos3 in game.get_empty_positions():
                if len({empty_pos1, empty_pos2, empty_pos3}) < 3:
                    continue
                my_opps = game.dooz_opportunities(game.get_my_positions() + [empty_pos1, empty_pos2, empty_pos3],
                                                  by_putting=True)
                if len(my_opps) > 1:
                    # We've created a two-way
                    log('Can create a two-way by putting on', empty_pos1, '&', empty_pos2, '&', empty_pos3)
                    log('These opportunities will be created:', my_opps)
                    opps_with_pos1_2 = game.dooz_opportunities(game.get_my_positions() + [empty_pos1, empty_pos2],
                                                             by_putting=True)
                    opps_with_pos2_3 = game.dooz_opportunities(game.get_my_positions() + [empty_pos2, empty_pos3],
                                                             by_putting=True)
                    opps_with_pos1_3 = game.dooz_opportunities(game.get_my_positions() + [empty_pos1, empty_pos3],
                                                             by_putting=True)
                    min_opps = min(len(opps_with_pos1_2), len(opps_with_pos2_3), len(opps_with_pos1_3))
                    the_empty_pos_to_put = empty_pos1
                    if len(opps_with_pos2_3) == min_opps:
                        the_empty_pos_to_put = empty_pos2
                    return game.put(Pos(*the_empty_pos_to_put))  # TODO choose the best two-way

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
