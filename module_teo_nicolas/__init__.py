from .lib.strategies import createStrategy, Echauffement, Attaque, Defense
import soccersimulator as soc

def get_team_q1(it):
	name = " Volley " if it == 1 else " Ball "
	team = soc.SoccerTeam (name = name)
	team.add(name, createStrategy(Echauffement()))

	return team

def get_team_q2(it):
	name = " Volley " if it == 1 else " Ball "
	team = soc.SoccerTeam (name = name)
	team.add(name, createStrategy(Attaque()))

	return team

def get_team_q3(it):
	name = " Volley " if it == 1 else " Ball "
	team = soc.SoccerTeam (name = name)
	team.add(name, createStrategy(Attaque() if it == 1 else Defense()))

	return team