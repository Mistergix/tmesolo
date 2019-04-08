import soccersimulator as soc
import math

class Action:
	def __init__(self, name):
		self.name = name
	def computeAction(self, superstate):
		return soc.SoccerAction()

class Move(Action):
	def __init__(self, name):
		Action.__init__(self, name)

class Shoot(Action):
	def __init__(self, name):
		Action.__init__(self, name)


class RunToEchauffementPos(Move):
	def __init__(self):
		Move.__init__(self, "RunToEchauffementPos")
	def computeAction(self, superstate):
		return soc.SoccerAction(acceleration = (superstate.echauffement_pos - superstate.player_pos))

class RunToDefensivePos(Move):
	def __init__(self):
		Move.__init__(self, "RunToDefensivePos")
		self.echauffement = RunToEchauffementPos()
	def computeAction(self, superstate):
		return self.echauffement.computeAction(superstate)
	

class ShootToNearestOpponent(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToNearestAlly")
	def computeAction(self, superstate):
		shootAct = (superstate.nearest_opp.position - superstate.player_pos)
		return soc.SoccerAction( shoot = shootAct)

class ShootToCornerFarFromOpp(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToCornerFarFromOpp")
		self.lastCorner = None
		self.maxDistance = 0

	def computeAction(self, superstate):
		corner = superstate.farthest_opp_corner_from_nearest_opp
		distance = corner.distance(superstate.player_pos)
		if self.lastCorner is None or (not (self.lastCorner.x == corner.x and self.lastCorner.y == corner.y))  :
			self.lastCorner = corner
			self.maxDistance = distance

		t = (distance) / (self.maxDistance + 5)
		force = t * soc.settings.maxPlayerShoot
		shootVec = (corner - superstate.player_pos).normalize() * force
		return soc.SoccerAction(shoot=shootVec)

class RunToFarthestCorner(Move):
	def __init__(self):
		Move.__init__(self, "RunToFarthestCorner")

	def computeAction(self, superstate):
		corner = superstate.farthest_opp_corner_from_nearest_opp
		run = (corner - superstate.player_pos)
		return soc.SoccerAction(acceleration=run)



# BEFORE VOLLEY

class ShootToNearestAlly(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToNearestAlly")
	def computeAction(self, superstate):
		return soc.SoccerAction( shoot = (superstate.nearest_ally.position - superstate.player_pos).normalize() * 6)

class RunToBall(Move):
	def __init__(self):
		Move.__init__(self, "RunToBall")

	def computeAction(self, superstate):
		return soc.SoccerAction( acceleration = superstate.vect_play_ball)

class RunToPredictBall(Move):
	def __init__(self):
		Move.__init__(self, "RunToPredictBall")
	def computeAction(self, superstate):
		return soc.SoccerAction( acceleration = (superstate.vect_play_ball + superstate.ball_vit * 20 * superstate.coeff_distance) )



class RunToCloseDefensivePos(Move):
	def __init__(self):
		Move.__init__(self, "RunToDefensivePos")
	def computeAction(self, superstate):
		return soc.SoccerAction(acceleration = (superstate.close_defensive_pos + superstate.ball_pos - superstate.player_pos))

class ShootToGoal(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToGoal")
	def computeAction(self, superstate):
		return soc.SoccerAction( shoot = ((superstate.opp_goal - superstate.player_pos).normalize() * 6) )


class ShootToNearestAllyFarFromOpponent(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootAllyFarOpp")
	def computeAction(self, superstate):
		shoot = (superstate.nearest_ally.position - superstate.player_pos).normalize() * 6
		shoot.angle += (math.pi / 12 * math.copysign(1, shoot.angle - (superstate.nearest_opp.position - superstate.player_pos).angle))
		return soc.SoccerAction( shoot = shoot )
			

class ShootToMoveToGoal(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToMove")
	def computeAction(self,superstate):
		return soc.SoccerAction(shoot = (superstate.opp_goal - superstate.player_pos).normalize() * 1.5)
	
class StrongShootToGoal(Shoot):
	def __init__(self):
		Shoot.__init__(self, "StrongShootToGoal")
	def computeAction(self,superstate):
		if (superstate.player_pos.distance(superstate.ball_pos) < 20):
			coeff = (40 - (superstate.player_pos - superstate.ball_pos).norm)/20 * 3
		else : coeff = 3
		return soc.SoccerAction(shoot = ((superstate.opp_goal - superstate.player_pos).normalize() * coeff))

class ShootToCornerFarFromOppOLD(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToCorner")
	def computeAction(self,superstate):
		shoot = (superstate.ally_corner_far_opp_near_player - superstate.player_pos).normalize() * 4
		return soc.SoccerAction( shoot = shoot)