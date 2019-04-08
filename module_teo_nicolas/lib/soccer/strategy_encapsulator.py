import abc
import soccersimulator as soc
from . import soccertools as ut

class SimpleStrategy(soc.Strategy):
    def __init__(self, strategyBehavior):
        soc.Strategy.__init__(self, strategyBehavior.name)
        self.behavior = strategyBehavior

    def compute_strategy(self, state, id_team, id_player):
        super_state = ut.SuperState(state,id_team,id_player)
        self.behavior.updateActions(super_state)
        acc = self.behavior.get_acc(super_state)
        shoot = self.behavior.get_shoot(super_state)
        return acc + shoot

class StrategyBehavior(metaclass=abc.ABCMeta):
    def __init__(self, name, moveAction, shootAction):
        """
        Redefine compute_acc and compute_shoot
        You don't have to care about if you can shoot or not
        """
        self.name = name
        self.moveAction = moveAction
        self.shootAction = shootAction
        
    def compute_acc(self, super_state):
        return self.moveAction.computeAction(super_state)
        
    def compute_shoot(self, super_state):
        return self.shootAction.computeAction(super_state)

    def get_acc(self, super_state):
        return self.compute_acc(super_state)

    def get_shoot(self, super_state):
        if(super_state.can_shoot):
            return self.compute_shoot(super_state)
        return soc.SoccerAction()

    def changeMoveAction(self, moveAction):
        self.moveAction = moveAction

    def changeShootAction(self, action):
        self.shootAction = action

    def updateActions(self, super_state):
        pass
