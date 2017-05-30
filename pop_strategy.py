from Pos import Pos
from utils import log


def pop_strategy(game):
    log()
    log('Cycle #', game.get_cycle())
    log('Starting pop strategy...')

    # Check if the enemy has any dooz opportunities
    enemy_opps = game.dooz_opportunities(game.get_opp_positions(),
                                         by_putting=True if game.get_cycle() <= 24 else False)

    if enemy_opps:
        log('Enemy has dooz opportunities:', enemy_opps)
        # Check if by popping any of the enemy checkers, we can prevent enemy from doozing
        log('Checking if we can prevent enemy from doozing')
        for enemy_pos in game.get_opp_positions():
            cur_opps = game.dooz_opportunities([i for i in game.get_opp_positions() if i != enemy_pos],
                                               by_putting=True if game.get_cycle() <= 24 else False)
            if not cur_opps:
                # pop the enemy_pos
                log('Popping', enemy_pos)
                return game.pop(game.get_board().get_cell(*enemy_pos).get_checker())
        log('Couldn\'t prevent enemy from doozing.')

    # Enemy has no dooz opportunity or has more than 1
    # Try to make opportunities
    log('Trying to make opportunities by popping')
    my_opps = game.dooz_opportunities(game.get_my_positions(),
                                      by_putting=True if game.get_cycle() <= 24 else False)
    enemy_poses_score = []
    for enemy_pos in game.get_opp_positions():
        my_new_opps = game.dooz_opportunities(game.get_my_positions(),
                                              empty_positions=game.get_empty_positions() + [enemy_pos],
                                              by_putting=True if game.get_cycle() <= 24 else False)
        enemy_poses_score.append((enemy_pos, len(set(my_new_opps)) - len(set(my_opps))))
    enemy_poses_score.sort(key=lambda i: i[1], reverse=True)
    log('Could make', enemy_poses_score[0][1], 'opportunities by popping', enemy_poses_score[0][0], 'Popping...')
    return game.pop(game.get_board().get_cell(*enemy_poses_score[0][0]).get_checker())
