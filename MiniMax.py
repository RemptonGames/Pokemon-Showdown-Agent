# -*- coding: utf-8 -*-

# This library will handle the actual implementation of the minimax (with alpha pruning) 
# algorithm. It will rely on the agent to provide an evaluation function for each move, 
# but should not require any other modifications to be used by multiple different agents.

import asyncio
import time
import sys

sys.path.append("..")

import BattleUtilities
from poke_env.player.random_player import RandomPlayer
from MaxDamagePlayer import MaxDamagePlayer
from SmartDamagePlayer import SmartDamagePlayer
from poke_env.player.player import Player
from poke_env.environment.move_category import MoveCategory
from GameNode import GameNode
from poke_env.environment.pokemon import Pokemon

class MinimaxPlayer(Player): 

    previous_action = None
    maxDepth = 1 
    # The nodes keep track of battle states, moves are transitions between states
    def choose_move(self, battle):
        # HP values for you and your opponent's Pokemon are a dictionary that maps Pokemon to HP
        current_hp = {}
        for pokemon in battle.team.values():
            current_hp.update({pokemon : pokemon.current_hp})
        opponent_hp = {}
        for pokemon in battle.opponent_team.values():
            opponent_hp.update({pokemon : pokemon.current_hp})
        starting_node = GameNode(battle, battle.active_pokemon, current_hp, battle.opponent_active_pokemon, opponent_hp, None, not battle.can_dynamax, battle.active_pokemon.is_dynamaxed, not battle.opponent_can_dynamax, battle.opponent_active_pokemon.is_dynamaxed, float('-inf'), None, self.previous_action)
        if battle.active_pokemon.current_hp <= 0: 
        #    print(f"Pokemon {battle.active_pokemon} fainted")
            self.pick_best_switch(starting_node, 0)
        else: 
            self.minimax(starting_node, 0, True)
        child_nodes = starting_node.children
        best_score = float('-inf')
        best_node = None
        for child in child_nodes:
            if child.score >= best_score: 
                best_score = child.score
                best_node = child
        if best_node == None: 
            #print(f"Best node is none for some reason! Length of child_nodes is {len(child_nodes)}")
            self.previous_action = None
            return self.choose_default_move(battle)
        #if isinstance(best_node.action, Pokemon): 
            #print(f"Switching from {battle.active_pokemon} (type matchup score {BattleUtilities.get_defensive_type_multiplier(battle.active_pokemon, battle.opponent_active_pokemon)}) to {best_node.action} (type matchup score {BattleUtilities.get_defensive_type_multiplier(best_node.action, battle.opponent_active_pokemon)}) against {battle.opponent_active_pokemon}")
        #else:
        #    print(f"Pokemon {battle.active_pokemon} attacking with {best_node.action} against {battle.opponent_active_pokemon}")
        self.previous_action = best_node.action
        return self.create_order(best_node.action)



    def minimax(self, node, depth, is_bot_turn):
        if depth == self.maxDepth or self.is_terminal(node): 
            self.score(node)
            return node.score
        if is_bot_turn:
            score = float('-inf')
            bot_moves = node.generate_bot_moves()
            for move in bot_moves: 
                child_score = self.minimax(move, depth, False)
                score = max(score, child_score)
                print
            node.score = score
            return score
        else: 
            score = float('inf')
            opponent_moves = node.generate_opponent_moves()
            if len(opponent_moves) > 0:
                for move in opponent_moves: 
                    child_score = self.minimax(move, depth + 1, True)
                    score = min(score, child_score)
            else: 
                score = float('-inf')
            node.score = score
            return score



    def pick_best_switch(self, node, depth): 
        switches = node.add_bot_switches()
        score = float('-inf')
        for switch in switches:
            child_score = self.minimax(switch, depth, False)
            score = max(score, child_score)
        node.score = score
        return score



    # This function determines if this is an end state and we should stop
    def is_terminal(self, node):
        all_fainted = True
        for pokemon in node.current_HP.keys(): 
            if node.current_HP[pokemon] > 0:
                all_fainted = False
        if all_fainted: 
            return True
        all_fainted = True
        for pokemon in node.opponent_HP.keys():
            if node.opponent_HP[pokemon]:
                all_fainted = False
        if all_fainted: 
            return True
        return False



    def score(self, node):
        score = 0
        # Get positive points for dealing damage and knocking out opponent
        for pokemon in node.opponent_HP.keys():
            if pokemon.current_hp is not None:
                if node.opponent_HP[pokemon] <= 0 and pokemon.current_hp > 0: 
                    score += 300
                else:
                    damage = pokemon.current_hp - node.opponent_HP[pokemon] 
                    score += 3 * damage
            #else: 
                #print(f"Pokemon is {pokemon}, HP is None")
        # Lose points for taking damage or getting knocked out
        for pokemon in node.current_HP.keys():
            if node.current_HP[pokemon] <= 0 and pokemon.current_hp > 0: 
                score -= 100
            else: 
                damage = (pokemon.current_hp / pokemon.max_hp) - (node.current_HP[pokemon] / pokemon.max_hp)
                score -= damage
        # Lose points for getting outsped by opponent
        #if BattleUtilities.opponent_can_outspeed(node.current_pokemon, node.opponent_pokemon):
        #    score -= 25
        # Add / Subtract points for type match-up
        #type_multiplier = BattleUtilities.get_defensive_type_multiplier(node.current_pokemon, node.opponent_pokemon)
        #if type_multiplier == 4: 
        #    score -= 50
        #if type_multiplier == 2: 
        #    score -= 25
        #if type_multiplier == 0.5:
        #    score += 25
        #if type_multiplier == 0.25:
        #    score += 50
        #if node.battle.can_dynamax and node.has_dynamaxed:
        #    score -= 25
        node.score = score
        return score
    
async def main():
    start = time.time()

    # We create two players.
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )
    minimax_player = MinimaxPlayer(
        battle_format="gen8randombattle",
    )

    await minimax_player.battle_against(smart_damage_player, n_battles=1000)

    print(
        "minimax player won %d / 100 battles against smart_damage_player (this took %f seconds)"
        % (
            minimax_player.n_won_battles, time.time() - start
        )
    )

if __name__ == "__main__":
        asyncio.get_event_loop().run_until_complete(main())
