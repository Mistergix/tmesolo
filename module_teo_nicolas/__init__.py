from .lib.strategies import createStrategy, Echauffement
import soccersimulator as soc

def get_team_q1(it):
	name = " Volley " if it == 1 else " Ball "
	team = soc.SoccerTeam (name = name)
	team.add(name, createStrategy(Echauffement()))

	return team