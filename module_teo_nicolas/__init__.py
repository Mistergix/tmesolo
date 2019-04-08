from .lib.strategies import GoalBehaviorAlone, createStrategy, GoalBehaviorTeam, AttaquantBehavior, newGoalBehaviorTeam
import soccersimulator as soc

def get_team ( nb_players ):
	team = soc.SoccerTeam ( name = " Inazuma {} ".format(nb_players))
	if nb_players == 1:
		team.add ( " Mark Evans " , createStrategy(GoalBehaviorAlone()))
	if nb_players == 2:
		team.add ( " Axel Blaze " , createStrategy(AttaquantBehavior()))
		team.add ( " Mark Evans " , createStrategy(newGoalBehaviorTeam()))
	if nb_players == 4:
		team.add ( " Axel Blaze " , createStrategy(AttaquantBehavior()))
		team.add ( " Mark Evans " , createStrategy(newGoalBehaviorTeam()))
		team.add ( " Axel Blaze " , createStrategy(AttaquantBehavior()))
		team.add ( " Mark Evans " , createStrategy(newGoalBehaviorTeam()))
	return team

def get_team_opp():
	team2 = soc.SoccerTeam ( name = " Royal Academy ")

	team2.add ( " Nul " , createStrategy(AttaquantBehavior()))
	team2.add ( " Nul " , createStrategy(newGoalBehaviorTeam()))
	team2.add ( " Nul " , createStrategy(AttaquantBehavior()))
	team2.add ( " Nul " , createStrategy(newGoalBehaviorTeam()))

	return team2