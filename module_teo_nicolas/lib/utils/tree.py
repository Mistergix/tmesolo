from . import json
import cProfile

cp = cProfile.Profile()


class SoccerTree:
    def __init__(self, all_coords, nbPlayersPerTeam, dimensions):
        cp.enable()
        nb_combi = len(all_coords) ** (nbPlayersPerTeam * 2 + 1)
        print(nb_combi)
        self.nbPlayersPerTeam = nbPlayersPerTeam
        self.dimensions = dimensions

        self.file_title = "tree-{}-{}".format(self.nbPlayersPerTeam, self.dimensions)

        self._LoadPaths(all_coords)
        cp.disable()
        cp.print_stats()

    def _LoadFile(self):
        try:
            self.indexes = json.decode_json(self.file_title)["indexes"]
        except FileNotFoundError:
            print("Fichier tree non trouvé, création d'un data vide")
            self._LoadIndexes()

    def _SaveFile(self):
        json.encode_json({"indexes" : self.indexes}, self.file_title)

    def _LoadIndexes(self):
        paths = []

        w, h = self.dimensions
        size = w * h 

        if self.nbPlayersPerTeam == 1 :
            for pos_p1 in range(size):
                for pos_p2 in range(size):
                    for pos_ball in range(size):
                        paths.append((pos_p1, pos_p2, pos_ball))
        elif self.nbPlayersPerTeam == 2 :
            for pos_p1 in range(size):
                for pos_p2 in range(size):
                    for pos_p3 in range(size):
                        for pos_p4 in range(pos_p3,size):
                            for pos_ball in range(size):
                                paths.append((pos_p1, pos_p2, pos_p3, pos_p4, pos_ball))
        elif self.nbPlayersPerTeam == 4 :
            for pos_p1 in range(size):
                for pos_p2 in range(size):
                    for pos_p3 in range(pos_p2,size):
                        for pos_p4 in range(pos_p3,size):
                            for pos_p5 in range(size):
                                for pos_p6 in range(pos_p5, size):
                                    for pos_p7 in range(pos_p6, size):
                                        for pos_p8 in range(pos_p7,size):
                                            for pos_ball in range(size):
                                                paths.append((pos_p1, pos_p2, pos_p3, pos_p4, pos_p5, pos_p6, pos_p7, pos_p8, pos_ball))
                                                
        self.indexes = paths
        self._SaveFile()

    def _LoadPaths(self, all_coords):
        self._LoadFile()
        paths = []
        for indexes in self.indexes:
            path = []
            for index in indexes :
                path.append(all_coords[int(index)])
            paths.append(tuple(path))

        self.paths = paths

    
    @staticmethod
    def OptimizePath(nbPlayersPerTeam, path):
        team1 = path[1 : nbPlayersPerTeam] # ignore 1st player
        ball = [path[len(path) - 1]]
        team2 = path[nbPlayersPerTeam : len(path) - 1]

        team1.sort()
        team2.sort()
        return tuple([path[0]] + team1 + team2 + ball)