# -*- coding: utf-8 -*-
import asyncio
import time
import sys

sys.path.append("..")

import BattleUtilities
from poke_env.player.random_player import RandomPlayer
from MaxDamagePlayer import MaxDamagePlayer
from poke_env.player.player import Player
from poke_env.player.baselines import SimpleHeuristicsPlayer
from poke_env.environment.move_category import MoveCategory

class SmartDamagePlayer(Player):
    prevDamagePercent = 100 
    currentdamagePercent = 100 
    usedMovePreviously = False 
    currentOpponent = None
    previousOpponent = None

    def choose_move(self, battle):
        self.currentOpponent = battle.opponent_active_pokemon
        if self.currentOpponent != self.previousOpponent: 
            self.currentDamagePercent = 100
            self.previousDamagePercent = 100
            # print(f"New opponent is {self.currentOpponent}")
        else: 
            self.currentDamagePercent = battle.opponent_active_pokemon.current_hp
        #    if self.usedMovePreviously: 
                # print(f'Actual damage % done was {(self.prevDamagePercent - self.currentDamagePercent)}, previous health % was {self.prevDamagePercent}, current health percentage is {self.currentDamagePercent}%')
        self.prevDamagePercent = self.currentDamagePercent
        self.usedMovePreviously = False
        self.previousOpponent = self.currentOpponent
        

        # If Pokemon is out of moves, switch to best option
        if not battle.available_moves: 
            best_switch = self.choose_best_switch(battle)
            if best_switch is None: 
                return self.choose_default_move(battle)
            return self.create_order(best_switch)
        
        # Use info such as type matchup and relative speed to determine who to switch to
        matchup_score = self.get_matchup_score(battle.active_pokemon, battle.opponent_active_pokemon)
        # If negative situation exceeds threshold, switch Pokemon
        if matchup_score >= 1:
            best_switch = self.choose_best_switch(battle)
            if best_switch is not None: 
                return self.create_order(best_switch)
        

        # finds the best move among available ones
        self.usedMovePreviously = True
        best_move = max(battle.available_moves, key=lambda move: BattleUtilities.calculate_damage(move, battle.active_pokemon, battle.opponent_active_pokemon, True, True))
        # print(f'Best move was {best_move}, Calculated damage value was {self.calculate_damage(best_move, battle)}')
        return self.create_order(best_move)

    def choose_best_switch(self, battle): 
        if not battle.available_switches: 
            return None
        # Go through each Pokemon that can be switched to, and choose one with the best type matchup
        # (smaller multipliers are better) 
        best_score = float('inf')
        best_switch = battle.available_switches[0] 
        for switch in battle.available_switches: 
            score = self.get_matchup_score(switch, battle.opponent_active_pokemon)
            if score < best_score: 
                best_score = score
                best_switch = switch
        return best_switch
    
    # Gets a number that determines how well the Pokemon matches up with opponent. Lower scores are better
    def get_matchup_score(self, my_pokemon, opponent_pokemon):
        score = 0
        defensive_multiplier = BattleUtilities.get_defensive_type_multiplier(my_pokemon, opponent_pokemon)
        # A multiplier greater than 1 means we are at a type disadvantage. If there is a better type match, switch
        if defensive_multiplier == 4:
            score += 1
        elif defensive_multiplier == 2:
            score += 0.5
        elif defensive_multiplier == 0.5:
            score -= 0.5
        elif defensive_multiplier == 0.25:
            score -= 1
        if BattleUtilities.opponent_can_outspeed(my_pokemon, opponent_pokemon):
            score += 0.5
        return score

async def main(): 
    start = time.time()

    heuristic_player = SimpleHeuristicsPlayer(
            battle_format="gen8randombattle",
    )
    smart_damage_player = SmartDamagePlayer(
            battle_format="gen8randombattle",
    )

    start = time.time()
    await smart_damage_player.battle_against(heuristic_player, n_battles=500)

    print(
        "Smart damage player won %d / 500 battles against heuristic_player (this took %f seconds)"
        % (
            smart_damage_player.n_won_battles, time.time() - start
        )
    )

if __name__ == "__main__":
        asyncio.get_event_loop().run_until_complete(main())

