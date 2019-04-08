"""
We only define compute_strategy here and ways to create strategies from them
"""
import math

import soccersimulator as soc
from .soccer import action as act
from .soccer import strategy_encapsulator as strat


def createStrategy(behavior):
    return strat.SimpleStrategy(behavior)

def createStrategies(behaviors):
    strats = []
    for behavior in behaviors:
        strats.append(strat.SimpleStrategy(behavior))
    return strats

class Echauffement(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Echauffement", act.RunToEchauffementPos(), act.ShootToNearestOpponent())

    def updateActions(self, super_state):
        if super_state.is_ball_on_our_side:
            self.changeMoveAction(act.RunToPredictBall())
        else :
            self.changeMoveAction(act.RunToEchauffementPos())

class Attaque(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Attaque", act.RunToPredictBall(), act.ShootToCornerFarFromOpp())
            self.passes_a_soi = 0
    def updateActions(self, super_state):
        if super_state.is_ball_on_our_side:
            self.changeMoveAction(act.RunToPredictBall())
        else :
            self.changeMoveAction(act.RunToDefensivePos())

class Defense(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Attaque", act.RunToDefensivePos(), act.DontShoot())
            self.passes_a_soi = 0
    def updateActions(self, super_state):
        if (not super_state.is_ball_on_our_side and super_state.is_ball_near_center and super_state.is_ball_near_opp) or super_state.is_ball_on_our_side:
            
            self.changeMoveAction(act.RunToPredictBall())
        else :
            self.changeMoveAction(act.RunToDefensivePos())


# BEFORE VOLLEY

        
class GoalBehaviorTeam(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Goal Team", act.RunToDefensivePos(), act.ShootToNearestAlly())

    def updateActions(self, super_state):
        if super_state.is_ball_nearest :
            self.changeMoveAction(act.RunToPredictBall())
            if ((super_state.opp_goal - super_state.player_pos).angle - (super_state.nearest_ally.position - super_state.player_pos).angle) < math.pi/3:
                self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            elif ((super_state.player_pos - super_state.opp_goal).norm < 30) and (super_state.is_opp_goal_nearer):
                self.changeShootAction(act.StrongShootToGoal())
            else :
                self.changeShootAction(act.ShootToMoveToGoal())

        else :
            self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            if super_state.is_ball_near_our_goal :
                self.changeMoveAction(act.RunToCloseDefensivePos())
            else :self.changeMoveAction(act.RunToDefensivePos())

class newGoalBehaviorTeam(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Goal", act.RunToDefensivePos(), act.ShootToNearestAlly())

    def updateActions(self, super_state):
        if super_state.is_ball_nearest :
            self.changeMoveAction(act.RunToPredictBall())
            if ((super_state.opp_goal - super_state.player_pos).angle - (super_state.nearest_ally.position - super_state.player_pos).angle) < math.pi/3:
                self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            elif ((super_state.player_pos - super_state.opp_goal).norm < 30) and (super_state.is_opp_goal_nearer):
                self.changeShootAction(act.StrongShootToGoal())
            else :
                self.changeShootAction(act.ShootToMoveToGoal())

        else :
            self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            self.changeMoveAction(act.RunToCloseDefensivePos())


class GoalBehaviorAlone(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Goal Alone", act.RunToDefensivePos(), act.ShootToCornerFarFromOpp())
            self.oppPos = soc.Vector2D(0,0)
            self.hasMoved = False
            

    def updateActions(self, super_state):
        if not(self.hasMoved):
            if self.oppPos == soc.Vector2D(0,0) :
                self.oppPos = super_state.nearest_opp.position
            elif super_state.nearest_opp.position.distance(self.oppPos) < 1:
                self.oppPos = super_state.nearest_opp.position
                self.changeMoveAction(act.RunToPredictBall())
                if super_state.player_pos.distance(super_state.opp_goal) > 30:
                    self.changeShootAction(act.ShootToMoveToGoal())
                else : 
                    self.changeShootAction(act.StrongShootToGoal())
            else :
                self.hasMoved = True
            
        else :
            self.changeMoveAction(act.RunToDefensivePos()) 
            if super_state.ball_in_corner:
                self.changeMoveAction(act.RunToCloseDefensivePos())
                self.changeShootAction(act.ShootToGoal())
            elif super_state.is_ball_nearest :
                self.changeMoveAction(act.RunToPredictBall())
                if (super_state.is_opp_goal_nearer) :
                    self.changeShootAction(act.ShootToMoveToGoal())
                else : 
                    self.changeShootAction(act.ShootToCornerFarFromOpp())
            else :
                self.changeShootAction(act.ShootToCornerFarFromOpp())
                if super_state.is_ball_near_our_goal :
                    self.changeMoveAction(act.RunToCloseDefensivePos())
                else :self.changeMoveAction(act.RunToDefensivePos())
