# -*- coding: utf-8 -*-

from poke_env.environment.move_category import MoveCategory

def calculate_damage(move, attacker, defender, pessimistic, is_bot_turn):
    if move is None:
        print("Why is move none?")
        return 0
    if move.category == MoveCategory.STATUS:
        return 0
    # Start with the base power of the move
    damage = move.base_power
    ratio = 1
    # Multiply by the attack / defense ratio
    if move.category == MoveCategory.PHYSICAL:
        # estimate physical ratio
        ratio = calculate_physical_ratio(attacker, defender, is_bot_turn)
    elif move.category == MoveCategory.SPECIAL:
        # estimate special ratio
        ratio = calculate_special_ratio(attacker, defender, is_bot_turn)
    damage = damage * ratio
    level_multiplier = ((2 * attacker.level) / 5 ) + 2
    damage = damage * level_multiplier
    # Finish calculating the base damage of the attack
    damage = (damage / 50) + 2;
    # Damage is multiplied by a random value between 0.85 and 1. Pessimistic flag gets a lower bound
    if pessimistic:
        damage = damage * 0.85
    if move.type == attacker.type_1 or move.type == attacker.type_2:
        damage = damage * 1.5
    type_multiplier = defender.damage_multiplier(move)
    damage = damage * type_multiplier
    # print(f"Damage calculation for move {move} against opponent {battle.opponent_active_pokemon} is {damage}")
    return damage

# The following two functions work very similarly, just focusing on different stats.
# They get the ratio between my Pokemon's attack and my opponent's estimated defense
# In random battles each Pokemon has 85 EVs in each stat and a neutral nature
# As far as I can tell IVs are random - assume average IVs (15)
def calculate_physical_ratio(attacker, defender, is_bot_turn):
    if is_bot_turn:
        # Get my attack value
        attack = attacker.stats["atk"]
        defense = 2 * defender.base_stats["def"]
        # I am adding 36 because it represents a very average amount of evs and ivs in the stat
        defense = defense + 36
        defense = ((defense * defender.level) / 100 ) + 5
    else:
        defense = defender.stats["def"]
        attack = 2 * attacker.base_stats["atk"]
        attack = attack + 36
        attack = ((attack * attacker.level) / 100) + 5
    return attack / defense   

def calculate_special_ratio(attacker, defender, is_bot_turn):
    if is_bot_turn:
        # Get my special attack value
        spatk = attacker.stats["spa"]
        spdef = 2 * defender.base_stats["spd"]
        # I am adding 36 because it represents a very average amount of evs and ivs in the stat
        spdef = spdef + 36
        spdef = ((spdef * defender.level) / 100 ) + 5
    else: 
        spdef = defender.stats["spd"]
        spatk = 2 * attacker.base_stats["spa"]
        spatk = spatk + 36
        spatk = ((spatk * attacker.level) / 100) + 5
    return spatk / spdef

def opponent_can_outspeed(my_pokemon, opponent_pokemon):
    my_speed = my_pokemon.stats["spe"]
    # Assume the worst - max IVs for opponent speed
    opponent_max_speed = 2 * opponent_pokemon.base_stats["spe"]
    # Add 52 - thats 31 for IVs and 21 for EVs (which are distributed evenly)
    opponent_max_speed = opponent_max_speed + 52
    opponent_max_speed = ((opponent_max_speed * opponent_pokemon.level) / 100) + 5
    if opponent_max_speed > my_speed: 
        return True
    else: 
        return False

def calculate_total_HP(pokemon, is_dynamaxed): 
    HP = pokemon.base_stats["hp"] * 2
    # Add average EVs and IVs to stat
    HP = HP + 36
    HP = ((HP * pokemon.level) / 100)
    HP = HP + pokemon.level + 10
    if is_dynamaxed: 
        HP = HP * 2
    return HP

# Returns a value that determines how well my_pokemon matches up with
# opponent_pokemon defensively. If opponent_pokemon has multiple types,
# return the value associated with the worse matchup
def get_defensive_type_multiplier(my_pokemon, opponent_pokemon):
    multiplier = 1
    first_type = opponent_pokemon.type_1
    first_multiplier = my_pokemon.damage_multiplier(first_type)
    second_type = opponent_pokemon.type_2
    if second_type is None:
        return first_multiplier
    second_multiplier = my_pokemon.damage_multiplier(second_type)
    multiplier = first_multiplier if first_multiplier > second_multiplier else second_multiplier
    return  multiplier
