from . import strategies as st
import soccersimulator as soc

def get_team ( nb_players, it ):
    team = soc.SoccerTeam ( name = " Inazuma {} (team {})".format(nb_players, it))
    if nb_players == 1:
        strat = st.TraineeBehavior() if it == 1 else st.GoalBehaviorAlone()
        team.add ( " Lone Wolf " , st.createStrategy(strat))
    elif nb_players == 2:
        strat = st.TraineeBehavior() if it == 1 else st.AttaquantBehavior()
        team.add ( " SNK " , st.createStrategy(strat))
        team.add ( " Mark Evans " , st.createStrategy(st.GoalBehaviorTeam()))
    elif nb_players == 3:
        strat = st.TraineeBehavior() if it == 1 else st.AttaquantBehavior()
        team.add ( " SNK " , st.createStrategy(strat))
        team.add ( " Mark Evans " , st.createStrategy(st.GoalBehaviorTeam()))
        team.add ( " Axel Blaze " , st.createStrategy(st.AttaquantBehavior()))
    elif nb_players == 4:
        strat = st.TraineeBehavior() if it == 1 else st.AttaquantBehavior()
        team.add ( " SNK " , st.createStrategy(strat))
        team.add ( " Mark Evans " , st.createStrategy(st.GoalBehaviorTeam()))
        team.add ( " Axel Blaze " , st.createStrategy(st.AttaquantBehavior()))
        team.add ( " Shaun Frost " , st.createStrategy(st.AttaquantBehavior()))  


    return team