import soccersimulator as soc
from module_teo_nicolas.lib.strategies import *

if __name__ == '__main__':

    team1 = soc.SoccerTeam ( name = " Pain au chocolat ")
    team1.add("Auto", createStrategy(AutoBehavior()))
    team2 = soc.SoccerTeam ( name = " Chocolatine ")
    team2.add("Fonceur", createStrategy(FonceurBehavior()))
    match = soc.Simulation(team1, team2, 2000)
    match.start()
    soc.show_simu(match)
