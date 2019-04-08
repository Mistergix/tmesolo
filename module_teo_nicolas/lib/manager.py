from . import qsoccer
from .soccer import action as act
from .soccer import discretizedterrain as d_terrain
from .soccer import soccertools as ut
from .soccer import strategy_encapsulator as strat


class Manager:

    manager = None

    def __init__(self):
        """
        Singleton to compute the next actions for all players each tick
        """
        pass

    @staticmethod
    def getInstance():
        if not Manager.manager :
            Manager.manager = Manager()
        return Manager.manager

    def getNextActions(self, state, id_team, id_player):
        assert id_player in [0,1,2,3]
        return self._computeNextAction(state, id_team, id_player)

    def _computeNextAction(self, state, it, ip):
        nb_player_per_team = len(state.players) // 2

        action = qsoccer.QSoccer.get_instance(nb_player_per_team).getData(state, it, ip)
        return action


if __name__ == "__main__":
    pass
