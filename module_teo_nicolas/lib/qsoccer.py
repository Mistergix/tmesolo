import random

import soccersimulator as soc

from . import strategies as strats
from . import getteam
from .soccer import action as act
from .soccer import discretizedterrain as d_terrain
from .soccer import soccertools as tools
from .utils.json import decode_json, encode_json
from .utils.tree import SoccerTree

nb_epochs = 5000
epsilon = 0.9
step_per_epoch = 100

class QSoccer:
    algo = None

    @staticmethod
    def get_instance(nb_player_per_team):
        if QSoccer.algo is None :
            QSoccer.algo = QSoccer(nb_player_per_team)
        return QSoccer.algo
        

    def __init__(self, nb_player_per_team):
        self.d_terrain = d_terrain.DiscretizedTerrain.getInstance()
        self.nb_player_per_team = nb_player_per_team
        self.terrain = tools.TerrainData.getInstance()

        self.dimension = self.d_terrain.getDimension()
        self.possibleActions = act.getAllActions(self.nb_player_per_team)

        self.data = self._Load()

        self.states = []
        self.actions = []
        self._initStateSpace()
        self._initQTableAndCounts()
        self._initActions()

        # Initiate Soccer
        self.simu = None
        
    def _initStateSpace(self):
        all_coords = self.d_terrain.AllPossibleCoords()
        tree = SoccerTree(all_coords, self.nb_player_per_team, self.dimension)
        self.states = tree.paths

        del tree

    def _initQTableAndCounts(self):
        try :
            data_with_dim = self.data["q_tables"][str(self.nb_player_per_team)][str(self.dimension)]
            self.q_table = data_with_dim["q_table"]
            self.counts = data_with_dim["counts"]
        except KeyError as e :
            self._newQTable()

    def getData(self, soccerstate, it, ip):
        path = self._getPath(soccerstate)
        if it == 2 :
            path = self._getSymetricalPath(path)

        tmp = path[ip]
        path[ip] = path[0]
        path[0] = tmp

        path = self._OptimizeState(path)

        q_row = self._getQRow(path)

        move_index, shoot_index = self._fromActionStrToTuple(self._getBest(q_row))

        actMove = self.possibleActions["moves"][self.data["moves"][move_index]]()
        actShoot = self.possibleActions["shoots"][self.data["shoots"][shoot_index]]()
        return actMove, actShoot

    def _getSymetricalPath(self, path):
        s_path = self.d_terrain.GetSymetricals(path)
        team2 = list(s_path[ : self.nb_player_per_team])
        team1 = list(s_path[self.nb_player_per_team : len(s_path) - 1])

        return team1 + team2 + [s_path[len(s_path) - 1]]

    def _initActions(self):
        moves = self.data["moves"]
        shoots = self.data["shoots"]
        moves_len = len(moves)
        shoots_len = len(shoots)

        for i in range(moves_len):
            for j in range(shoots_len):
                key = (i , j)
                self.actions.append(key)

        self.currentAction = str(self._getA0())


    def _newQTable(self):
        moves = self.data["moves"]
        shoots = self.data["shoots"]

        self.q_table = {}
        self.counts = {}
        moves_len = len(moves)
        shoots_len = len(shoots)
        for state in self.states :
            self.q_table[str(state)] = {}
            self.counts[str(state)] = {}
            for i in range(moves_len):
                for j in range(shoots_len):
                    key = (i , j)
                    self.q_table[str(state)][str(key)] = 0
                    self.counts[str(state)][str(key)] = 0

    def Train(self, show=False):
        self.epochs = nb_epochs
        self.epsilon = epsilon
        self.current_epoch = 0

        self.step_per_epoch = step_per_epoch
        self.max_steps = self.epochs * self.step_per_epoch

        team1 = getteam.get_team(self.nb_player_per_team, 1)
        team2 = getteam.get_team(self.nb_player_per_team, 2)

        self.simu = soc.Simulation(team1, team2, max_steps=self.max_steps) 
        self.simu.listeners += self

        if show: 
            soc.show_simu(self.simu) 
        else: 
            self.simu.start() 

    def _getPath(self, soccerstate):
        path = []
        for i in range(1, 3):
            team = [ (it, ip) for (it, ip) in soccerstate.players if it == i]
            for it, ip in team :
                p_state = soccerstate.player_state(it, ip)
                pos = p_state.position
                case = d_terrain.DiscretizedTerrain.getInstance().FromPositionToCase(pos)
                path.append(case)

        case = d_terrain.DiscretizedTerrain.getInstance().FromPositionToCase(soccerstate.ball.position)
        path.append(case)
        return path

    def _Save(self):
        print("Saving...")
        q_tables_key = "q_tables"
        if q_tables_key not in self.data :
            self.data[q_tables_key] = {}

        nb_players = str(self.nb_player_per_team)
        if nb_players not in self.data[q_tables_key] :
            self.data[q_tables_key][nb_players] = {}

        dim = str(self.dimension)
        if dim not in self.data[q_tables_key][nb_players] :
            self.data[q_tables_key][nb_players][dim] = {}

        self.data[q_tables_key][nb_players][dim]["q_table"] = self.q_table
        self.data[q_tables_key][nb_players][dim]["counts"] = self.counts
        
        encode_json(self.data, "q_data")

        print("saved")

    def _Load(self):
        try:
            data = decode_json("q_data")
        except FileNotFoundError:
            print("Fichier q_data non trouvé, création d'un data vide")
            data = {}

        move_key = "moves"
        if move_key not in data :
            data[move_key] = self.possibleActions[move_key]["names"]

        shoots_key = "shoots"
        if shoots_key not in data :
            data[shoots_key] = self.possibleActions[shoots_key]["names"]
        
        return data

    def _getS0(self):
        return random.choice(self.states)

    def _getA0(self):
        return random.choice(self.actions)

    def _get_ith_player_behavior(self, team):
        return team.players[0].strategy.behavior

    def _fromActionStrToTuple(self, action_str):
        """
        Way too fragile TODO NR : corriger ça 
        """
        l = list(action_str) # ['(', '0', ',', ' ' , '5', ')']
        mindex = int(l[1])
        sindex = int(l[4])
        return (mindex, sindex)

    def _get_current_action_for_ith_player(self):
        move_index, shoot_index = self._fromActionStrToTuple(self.currentAction)
        actMove = self.possibleActions["moves"][self.data["moves"][move_index]]()
        actShoot = self.possibleActions["shoots"][self.data["shoots"][shoot_index]]()
        return actMove, actShoot

    def _getNextAction(self, act_probs):
        if (random.random() < self.epsilon):
            return str(self._getA0())

        return self._getBest(act_probs)

    def _getBest(self, act_probs):
        best = None
        bestVal = 0
        for action in act_probs :
            if (bestVal < act_probs[action]) or best is None :
                best = action
                bestVal = act_probs[action]

        return best

    def _getWorst(self, act_probs):
        worst = None
        worstVal = 0
        for action in act_probs :
            if (worstVal > act_probs[action]) or worst is None :
                worst = action
                worstVal = act_probs[action]

        return worst

    def _getNextState(self, soccerstate):
        newState = []
        for i in range (2 * self.nb_player_per_team + 1):
            coord = self.currentState[i]
            pos = self.d_terrain.FromCaseToPosition(coord)
            if i < self.nb_player_per_team : #team1
                pos = self.simu.state.states[(1, i)].position
            elif i == len(self.currentState) - 1 : #ball
                pos = self.simu.state.ball.position
            else : #team2
                pos = self.simu.state.states[(2, i - self.nb_player_per_team)].position

            coord = self.d_terrain.FromPositionToCase(pos)
            newState.append(coord)

        state = self._OptimizeState(newState)
        return state

    def _OptimizeState(self, state):
        optimizedState = SoccerTree.OptimizePath(self.nb_player_per_team, list(state))
        return optimizedState

    def _evaluate(self, soccerstate):
        if self.currentState not in self.returns :
            self.returns[self.currentState] = {}

        if self.currentAction not in self.returns[self.currentState] :
            self.returns[self.currentState][self.currentAction] = 0

        distance_to_goal = soccerstate.ball.position.distance(self.terrain.getTheOtherGoal(1).vector)
        self.returns[self.currentState][self.currentAction] -= distance_to_goal / 100

        if soccerstate.goal > 0 :
            coeff = 3 * self.step_per_epoch / ((soccerstate.step % self.step_per_epoch) + 1)
            old = self.returns[self.currentState][self.currentAction]
            print("coeff ", coeff)
            if soccerstate.goal == 1 :
                print("team 1 marque")
                sign = 1
            elif soccerstate.goal == 2 :
                sign = -1
                print("team 2 marque")
        
            self.returns[self.currentState][self.currentAction]  += sign * abs(old) * coeff

        counts = self._getCounts(self.currentState, self.currentAction)
        self._setCounts(self.currentState, self.currentAction, counts + 1)


    def _updatePlayerBehavior(self, team):
        m, s = self._get_current_action_for_ith_player()
        self._get_ith_player_behavior(team).changeMoveAction(m)
        self._get_ith_player_behavior(team).changeShootAction(s)

    def _updateQTable(self):
        for state in self.returns :
            for action in self.returns[state] :
                old = self._getQValue(state, action)
                count = self._getCounts(state, action)
                new = old + (1.0 / count) * (self.returns[state][action] - old)
                self._setQValue(state, action, new)
                # print("({}, {}) : OLD = {} / NEW = {}".format(state, action, old, new))

    def _getQRow(self, state):
        state = self._OptimizeState(state)
        return self.q_table[str(state)]

    def _getQValue(self, state, action):
        row = self._getQRow(state)
        return row[str(action)]

    def _setQValue(self, state, action, value):
        row = self._getQRow(state)
        row[str(action)] = value

    def _getCounts(self, state, action):
        state = self._OptimizeState(state)
        row = self.counts[str(state)]
        return row[str(action)]
    
    def _setCounts(self, state, action, value):
        state = self._OptimizeState(state)
        row = self.counts[str(state)]
        row[str(action)] = value

    def printBestsAndWorsts(self):
        dico = {"states" : {}}
        for state in self.states :
            row = self._getQRow(state)
            best = self._getBest(row)
            worst = self._getWorst(row)

            bestMoveI, bestShootI = self._fromActionStrToTuple(best)

            bestMove = self.possibleActions["moves"][self.data["moves"][bestMoveI]]().name
            bestShoot = self.possibleActions["shoots"][self.data["shoots"][bestShootI]]().name

            move_index, shoot_index = self._fromActionStrToTuple(worst)

            worstMove = self.possibleActions["moves"][self.data["moves"][move_index]]().name
            worstShoot = self.possibleActions["shoots"][self.data["shoots"][shoot_index]]().name

            dico["states"][str(state)] = (bestMoveI, bestShootI)

            print("{} : Best = ({}, {}) Worst = ({}, {})".format(state, bestMove, bestShoot, worstMove, worstShoot))
        
        encode_json(dico, "worstbest-{}-{}".format(self.nb_player_per_team, self.dimension))
            

    def begin_match(self, team1, team2, state):
        pass

    def begin_round(self, team1, team2, state):
        #print("-------------------BEGIN ROUND--------------------")
        self.currentState = self._getS0()
        for i in range (len(self.currentState)):
            coord = self.currentState[i]
            pos = self.d_terrain.FromCaseToPosition(coord)
            if i < self.nb_player_per_team : #team1
                self.simu.state.states[(1, i)].position = pos
            elif i == len(self.currentState) - 1 : #ball
                self.simu.state.ball.position = pos
            else : #team2
                self.simu.state.states[(2, i - self.nb_player_per_team)].position = pos

        self._updatePlayerBehavior(team1)

        self.returns = {}

    def update_round(self, team1, team2, state):
        self._evaluate(state)

        act_probs = self._getQRow(self.currentState)
        self.currentAction = self._getNextAction(act_probs)

        self.currentState = self._getNextState(state)

        self._updatePlayerBehavior(team1)

        if state.step % self.step_per_epoch == 0 :
            self.simu.end_round()

    def end_round(self, team1, team2, state):
        self._evaluate(state)
        self._updateQTable()

        #print("Le round est fini, on passe à l'epoch suivante et on recommence au premier gene")
        self.current_epoch += 1
        self.current_epoch %= self.epochs
        
        if self.current_epoch == 0 :
            #print("On a fait le tours des epochs, on arrete le match")
            self.simu.end_match()
            return

        if self.current_epoch % 1000 == 1 :
            self._Save()

        print("Current epoch : {} / {}".format(self.current_epoch, self.epochs))

    def end_match(self, team1, team2, state):
        self._Save()
