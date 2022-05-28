from ant import Ant
import params

class Colony:

    def __init__(self, grid):

        self.ants_count = params.ants_count
        self.colony = [Ant(grid) for _ in range(self.ants_count)]

    def work(self):
        """ Make all ants works !
        """
        for ant in self.colony:
            ant.work()
