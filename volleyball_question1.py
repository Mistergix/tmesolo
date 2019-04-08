import soccersimulator as soc
from module_teo_nicolas import get_team_q1

if __name__ == '__main__':
	team1 = get_team_q1(1)
	team2 = get_team_q1(2)

	match = soc.VolleySimulation(team1, team2, 2000)
	match.start()
	soc.volley_show_simu(match)