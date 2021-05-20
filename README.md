# POKEMON SHOWDOWN AI BATTLEBOT ** 

Format: Gen 8 Random Battle (For now)
* 6 random Pokemon with random moves
* No choice of lead
* No preview of opponent's team
* 3 minute timer for actions

Strategy: 
Pessimistic min-max strategy
* Assume that all attacks I make will get bad damage rolls (0.85)
* Assume all attacks my opponents make get optimal damage rolls (1.0) 
* Assume all opponent's Pokemon have optimum EVs and IVs for all stats
* Assign values to moves based on hard-coded rules, choose best one found 
* Limit search to 1 minute 30 seconds

**Start rules simple, get more complicated over time.**

**Agent V1 - Aggressive max damage**
* Ignore opponent actions
* Choose attack that will inflict maximum damage
	* More sophisticated than basic max-damage bot - takes STAB and type-advantages into account
* Ignore non-damaging moves
