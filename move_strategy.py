from utils import log
from Pos import Pos
import random


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
            for line in game.get_lines():
                dooz_partners = [i for i in line if i in game.get_my_positions()]
                if pos in line and len(dooz_partners) == 2:
                    my_neis = [i for i in game.get_neighbors()[pos]
                               if i in game.get_my_positions() and i not in dooz_partners]
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
                return game.move(game.get_board().get_cell(*my_neis[0]).get_checker(), Pos(*pos))  # TODO choose the best instead of the first

    # Do the best move
    log('Searching for the best move...')
    my_prev_opps = game.dooz_opportunities(game.get_my_positions())
    moves = []
    for my_pos in game.get_my_positions():
        for empty_nei in [i for i in game.get_neighbors()[my_pos] if i in game.get_empty_positions()]:
            new_my_poses = [i for i in game.get_my_positions() if i != my_pos] + [empty_nei]
            new_empty_poses = [i for i in game.get_empty_positions() if i != empty_nei] + [my_pos]
            my_new_opps = game.dooz_opportunities(new_my_poses, empty_positions=new_empty_poses)
            moves.append((my_pos, empty_nei, len(set(my_new_opps)) - len(set(my_prev_opps))))
    moves.sort(key=lambda i: i[2], reverse=True)
    if moves:
        log('Moving from', moves[0][0], 'to', moves[0][1], 'which makes', moves[0][2], 'opportunities')
        return game.move(game.get_board().get_cell(*moves[0][0]).get_checker(), Pos(*moves[0][1]))
