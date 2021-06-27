# -*- coding: utf-8 -*-

import asyncio
import sys

from poke_env.player.random_player import RandomPlayer
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ShowdownServerConfiguration

sys.path.append("./showdown_agent")

from MaxDamagePlayer import MaxDamagePlayer
from SmartDamagePlayer import SmartDamagePlayer
from MiniMax import MinimaxPlayer
from poke_env.player.baselines import SimpleHeuristicsPlayer

async def main(): 
    
    #print("Random Player:")

    # Create a player with the online server configuration
    #player = RandomPlayer(
    #        player_configuration=PlayerConfiguration("RemptonGames", "Cwalrus96!"),
    #        server_configuration=ShowdownServerConfiguration
    #)

    # Play a game on the ladder
    #await player.ladder(1)

    #print("Max Damage Player")

    #player = MaxDamagePlayer(
    #        player_configuration=PlayerConfiguration("RemptonGames", "Cwalrus96!"),
    #        server_configuration=ShowdownServerConfiguration
    #)

    # Play a game on the ladder
    #await player.ladder(1)

    #print("Smart Damage Player")

    #player = SmartDamagePlayer(
    #        player_configuration=PlayerConfiguration("RemptonGames", "Cwalrus96!"),
    #       server_configuration=ShowdownServerConfiguration
    #)

    # Play a game on the ladder
    #await player.ladder(1)

    #print("Minimax Player")

    #player = MinimaxPlayer(
    #        player_configuration=PlayerConfiguration("RemptonGames", "Cwalrus96!"),
    #        server_configuration=ShowdownServerConfiguration
    #)

    # Play a game on the ladder
    #await player.ladder(1)

    print("Simple Heuristic Player")

    player = SimpleHeuristicsPlayer(
            player_configuration=PlayerConfiguration("RemptonGames", "Cwalrus96!"),
            server_configuration=ShowdownServerConfiguration
    )

    # Play a game on the ladder
    await player.ladder(1)


if __name__ == "__main__": 
    asyncio.get_event_loop().run_until_complete(main())
