import math

import soccersimulator as soc


class MyVector2D:
    @staticmethod
    def getDirection(fromVector, toVector):
        vec = (toVector - fromVector)
        vec.normalize()
        return vec

class SuperState:
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.it = id_team
        self.ip = id_player
        self.key = lambda r: r[0]
        self.nb_player_per_team = len(state.players) // 2

    @property
    def can_shoot(self):
        """
        Returns true only if the player is within the range of the ball
        """
        return self.dist_play_ball <= soc.settings.PLAYER_RADIUS + soc.settings.BALL_RADIUS

    @property
    def getMyGoal(self):
        """
        Returns a GoalData
        """
        return self.terrainData.getMyGoal(self.it)

    @property
    def getTheOtherGoal(self):
        """
        Returns a GoalData
        """
        return self.terrainData.getTheOtherGoal(self.it)

    @property
    def opp_it(self):
        if self.it == 1:
            return 2
        return 1

    @property
    def ball(self):
        """
        Returns a MobileMixin
        """
        return self.state.ball
        
    @property
    def ball_pos(self):
        return self.ball.position

    @property
    def ball_vit(self):
        return self.ball.vitesse

    @staticmethod
    def nearest_player(pos, player_list):
        return min([(player.position.distance(pos), player) for player in player_list])[1]

    @property
    def player(self):
        """
        Returns a MobileMixin
        """
        return self.state.player_state(self.it, self.ip)

    @property	
    def player_pos(self):
        return self.state.player_state(self.it,self.ip).position
	
    @property	
    def player_vit(self):
        return self.state.player_state(self.it,self.ip).vitesse

    @property	
    def nearest_opp(self):
        return min([(opp.position.distance(self.player_pos), opp) for opp in self.opponents], key=self.key)[1]
		
    @property	
    def nearest_ally(self):
        l = [(ally.position.distance(self.player_pos), ally) for ally in self.allies]
        if len(l) > 0 :
            return min(l, key=self.key)[1]
        return self.player

    
		
    @property
    def nearest_player(self):
        return min([(player.position.distance(self.player_pos), player) for player in self.players], key=self.key)[1]

    @property
    def nearest_ball_all_allies(self):
        return min([(ally.position.distance(self.ball_pos), ally) for ally in self.all_allies], key=self.key)[1]

    @property
    def nearest_ball_ally(self):
        l = [(ally.position.distance(self.ball_pos), ally) for ally in self.allies]
        if len(l) > 0 :
            return min(l, key=self.key)[1]
        return self.player
	
    @property	
    def nearest_ball_opp(self):
        return min([(opp.position.distance(self.ball_pos), opp) for opp in self.opponents], key=self.key)[1]
		
    @property
    def nearest_ball_player(self):
        return min([(player.position.distance(self.ball_pos), player) for player in self.players], key=self.key)[1]
		
    @property
    def players(self):
        return [self.state.player_state(it,ip) for (it,ip) in self.state.players]
		
    @property
    def allies(self):
        return [self.state.player_state(it,ip) for (it,ip) in self.state.players if (it == self.it and ip != self.ip)]
		
    @property
    def all_allies(self):
        return [self.state.player_state(it,ip) for (it,ip) in self.state.players if it == self.it]
		
    @property
    def opponents(self):
        return [self.state.player_state(it,ip) for (it,ip) in self.state.players if it != self.it]

    @property
    def vect_play_ball(self):
        return self.ball_pos - self.player_pos

    @property
    def dist_play_ball(self):
        return self.vect_play_ball.norm

    @property
    def opp_goal(self):
        return self.getTheOtherGoal.vector    
        
    @property	
    def nearest_opp_goal_opp(self):
        return min([(opp.position.distance(self.opp_goal), opp) for opp in self.opponents], key=self.key)[1]

    @property
    def is_opp_goal_nearer(self):
        return self.player_pos.distance(self.opp_goal) < self.nearest_opp_goal_opp.position.distance(self.opp_goal)
	
    @property
    def ally_goal(self):
        return self.getMyGoal.vector

    @property
    def is_ball_nearest(self):
        return (self.player_pos.distance(self.ball_pos) + 0.5 < self.nearest_ball_opp.position.distance(self.ball_pos)) and (self.player_pos.distance(self.ball_pos) <= self.nearest_ball_all_allies.position.distance(self.ball_pos) )

    @property
    def coeff_distance(self):
        if self.dist_play_ball > 40 : 
            return 1
        return self.dist_play_ball / 40

    @property
    def ally_goal_top(self):
        return self.getMyGoal.top

    @property
    def ally_goal_bot(self):
        return self.getMyGoal.bottom

    @property
    def opp_goal_top(self):
        return self.getTheOtherGoal.top

    @property
    def opp_goal_bot(self):
        return self.getTheOtherGoal.bottom

    @property
    def defensive_pos(self):
        return soc.Vector2D(norm = ((self.ally_goal - self.ball_pos).x / 1.5 ) / math.cos(self.angle_median_ally_goal(self.ball_pos)), angle = self.angle_median_ally_goal(self.ball_pos))

    @property
    def echauffement_pos(self):
        if self.nb_player_per_team == 1 :
            return self.ally_goal
        return self.all_goal

    @property
    def is_ball_on_our_side(self):
        return self.terrainData.ballOnWhichSide(self.ball_pos) == self.it

    @property
    def is_ball_near_center(self):
        return abs(self.ball_pos.x - self.terrainData.center.x) <= self.terrainData.width / 6

    @property
    def is_ball_near_opp(self):
        return self.ball_pos.distance(self.nearest_opp.position) <= soc.settings.PLAYER_RADIUS + soc.settings.BALL_RADIUS

    @property
    def farthest_opp_corner_from_nearest_opp(self):
        nearest = self.nearest_opp
        corner = self.terrainData.farthestCorner(nearest.position, self.it)
        return corner

    @property
    def farthest_ally_corner(self):
        corner = self.terrainData.farthestCorner(self.player_pos, self.opp_it)
        return corner


    @property
    def close_defensive_pos(self):
        return soc.Vector2D(norm = ((self.ally_goal - self.ball_pos).x / 4. ) / math.cos(self.angle_median_ally_goal(self.ball_pos)), angle = self.angle_median_ally_goal(self.ball_pos))

    def angle_median_ally_goal(self, pos):
        return (((self.ally_goal_top - pos).angle + (self.ally_goal_bot - pos).angle) / 2) % (2 * math.pi)

    def angle_median_opp_goal(self, pos):
        return (((self.opp_goal_top - pos).angle + (self.opp_goal_bot - pos).angle ) / 2) % (2 * math.pi)

    @property
    def terrainData(self):
        return TerrainData.getInstance()

    @property
    def has_an_ally(self):
        return (len(self.allies) > 0)

    @property
    def bot_ally_corner(self):
        return soc.Vector2D((self.it - 1) * 150,90)

    @property
    def top_ally_corner(self):
        return soc.Vector2D((self.it - 1) * 150, 0)

    @property
    def top_opp_corner(self):
        return soc.Vector2D((self.it % 2) * 150,90)

    @property
    def bot_opp_corner(self):
        return soc.Vector2D((self.it % 2) * 150, 0)

    @property
    def ball_in_corner(self):
        return (abs(self.ball_pos.x - self.top_ally_corner.x) < 10 and abs(self.ball_pos.y - self.top_ally_corner.y) < 20) or (abs(self.ball_pos.x - self.bot_ally_corner.x) < 10 and abs(self.ball_pos.y - self.bot_ally_corner.y) < 20)

    @property
    def ally_corner_far_opp_near_player(self):
        corner = self.top_ally_corner
        if self.player_pos.distance(corner) > self.nearest_opp.position.distance(corner):
            return self.bot_ally_corner
        else : return corner

    @property
    def is_ball_near_our_goal(self):
        return abs((self.ball_pos - self.ally_goal).x) < 60

    @property
    def is_attacked(self):
        return all([((opp.position.distance(self.player_pos) < 10) and ((opp.player_vit.angle - self.player_pos.angle) < math.pi / 1.5)) for opp in self.opponents()])

    @property
    def is_team_is_ball_nearest(self):
        return nearest_ball_ally == nearest_ball_player

    @property
    def is_from_allies_our_goal_nearest(self):
        return all([ally.position.distance(self.ally_goal) < self.player_pos.distance(ally_goal) for ally in self.allies])


        
class GoalData:
    """
    Get data about the goal : its height, range, pos, center etc.
    """
    def __init__(self, team_id):
        assert team_id in [1,2]
        self.it = team_id
        self.vector = soc.Vector2D(soc.settings.GAME_WIDTH * (1 + (team_id - 1) * 2) / 4, soc.settings.GAME_HEIGHT / 2)

    def __repr__(self):
        return self.vector

    @property
    def top(self):
        return self.vector + soc.Vector2D(0, soc.settings.GAME_HEIGHT/2 + 5)

    @property
    def bottom(self):
        return self.vector - soc.Vector2D(0, soc.settings.GAME_HEIGHT/2 - 5)

    @property
    def left(self):
        return self.vector - soc.Vector2D(soc.settings.GAME_WIDTH/4 + 0 if self.it == 1 else 10, 0)

    @property
    def right(self):
        return self.vector + soc.Vector2D(soc.settings.GAME_WIDTH/4 - 0 if self.it == 2 else 10, 0)
        
class TerrainData:

    terrain = None

    def __init__(self):
        """
        Singleton to get some data about the terrain such as its width, height, center, the goals etc.
        """
        self.width = soc.settings.GAME_WIDTH
        self.height = soc.settings.GAME_HEIGHT
        self.center = soc.Vector2D(self.width, self.height) / 2
        self.goals = [GoalData(1), GoalData(2)]

    @staticmethod
    def getInstance():
        if not TerrainData.terrain :
            TerrainData.terrain = TerrainData()
        return TerrainData.terrain

    def getMyGoal(self, id_team):
        assert id_team in [1,2]
        return self.goals[id_team - 1]

    def getTheOtherGoal(self, id_team):
        assert id_team in [1,2]
        if id_team == 1 :
            return self.getMyGoal(2)
        return self.getMyGoal(1)

    def ballOnWhichSide(self, ball_pos):
        ball_x = ball_pos.x
        return 1 if ball_x < self.center.x else 2

    def farthestCorner(self, opp_pos, it):
        goal = self.getTheOtherGoal(it)
        x = goal.left.x if opp_pos.x >= goal.vector.x else goal.right.x
        y = goal.bottom.y if opp_pos.y >= goal.vector.y else goal.top.y
        return soc.Vector2D(x, y)
