# -*- coding: utf-8 -*-
import asyncio
import time
import sys

sys.path.append("..")

import BattleUtilities
from poke_env.player.random_player import RandomPlayer
from MaxDamagePlayer import MaxDamagePlayer
from SmartDamagePlayer import SmartDamagePlayer
from MiniMax import MinimaxPlayer
from poke_env.player.player import Player
from poke_env.player.baselines import SimpleHeuristicsPlayer

async def main():
    start = time.time()

    
    # Random vs Max
    random_player = RandomPlayer(
        battle_format="gen8randombattle",
    )
    max_damage_player = MaxDamagePlayer(
        battle_format="gen8randombattle",
    )

    await random_player.battle_against(max_damage_player, n_battles=1000)

    print(
        "random player won %d / 1000 battles against max_damage_player (this took %f seconds)"
        % (
            random_player.n_won_battles, time.time() - start
        )
    )

    # Random vs Smart
    start = time.time()
    random_player = RandomPlayer(
        battle_format="gen8randombattle",
    )
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )

    await random_player.battle_against(smart_damage_player, n_battles=1000)

    print(
        "random player won %d / 1000 battles against smart_damage_player (this took %f seconds)"
        % (
            random_player.n_won_battles, time.time() - start
        )
    )

    # Random vs Minimax
    start = time.time()
    random_player = RandomPlayer(
        battle_format="gen8randombattle",
    )
    minimax_player = MinimaxPlayer(
        battle_format="gen8randombattle",
    )

    await random_player.battle_against(minimax_player, n_battles=1000)

    print(
        "random player won %d / 1000 battles against minimax_player (this took %f seconds)"
        % (
            random_player.n_won_battles, time.time() - start
        )
    )

    # Random vs heuristic
    start = time.time()
    random_player = RandomPlayer(
        battle_format="gen8randombattle",
    )
    heuristic_player = SimpleHeuristicsPlayer(
        battle_format="gen8randombattle",
    )

    await random_player.battle_against(heuristic_player, n_battles=1000)

    print(
        "random player won %d / 1000 battles against heuristic_player (this took %f seconds)"
        % (
            random_player.n_won_battles, time.time() - start
        )
    )

    # Max vs Smart
    start = time.time()
    max_damage_player = MaxDamagePlayer(
        battle_format="gen8randombattle",
    )
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )

    await max_damage_player.battle_against(smart_damage_player, n_battles=1000)

    print(
        "max_damage_player won %d / 1000 battles against smart_damage_player (this took %f seconds)"
        % (
            max_damage_player.n_won_battles, time.time() - start
        )
    )
    
    # Max vs Minimax
    start = time.time()
    max_damage_player = MaxDamagePlayer(
        battle_format="gen8randombattle",
    )
    minimax_player = MinimaxPlayer(
        battle_format="gen8randombattle",
    )

    await max_damage_player.battle_against(minimax_player, n_battles=1000)

    print(
        "max_damage_player won %d / 1000 battles against minimax_player (this took %f seconds)"
        % (
            max_damage_player.n_won_battles, time.time() - start
        )
    )

    # Max vs Heuristic
    start = time.time()
    max_damage_player = MaxDamagePlayer(
        battle_format="gen8randombattle",
    )
    heuristic_player = SimpleHeuristicsPlayer(
        battle_format="gen8randombattle",
    )

    await max_damage_player.battle_against(heuristic_player, n_battles=1000)

    print(
        "max_damage_player won %d / 1000 battles against heuristic_player (this took %f seconds)"
        % (
            max_damage_player.n_won_battles, time.time() - start
        )
    )

    # Smart vs Minimax
    start = time.time()
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )
    minimax_player = MinimaxPlayer(
        battle_format="gen8randombattle",
    )

    await smart_damage_player.battle_against(minimax_player, n_battles=1000)

    print(
        "smart_damage_player won %d / 1000 battles against minimax_player (this took %f seconds)"
        % (
            smart_damage_player.n_won_battles, time.time() - start
        )
    )

    # Smart vs Heuristic
    start = time.time()
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )
    heuristic_player = SimpleHeuristicsPlayer(
        battle_format="gen8randombattle",
    )

    await smart_damage_player.battle_against(heuristic_player, n_battles=1000)

    print(
        "smart_damage_player won %d / 1000 battles against heuristic_player (this took %f seconds)"
        % (
            smart_damage_player.n_won_battles, time.time() - start
        )
    )

    # Minimax vs Heuristic
    start = time.time()
    minimax_player = MinimaxPlayer(
        battle_format="gen8randombattle",
    )
    heuristic_player = SimpleHeuristicsPlayer(
        battle_format="gen8randombattle",
    )

    await minimax_player.battle_against(heuristic_player, n_battles=1000)

    print(
        "minimax_player won %d / 1000 battles against heuristic_player (this took %f seconds)"
        % (
            minimax_player.n_won_battles, time.time() - start
        )
    )

if __name__ == "__main__":
        asyncio.get_event_loop().run_until_complete(main())
