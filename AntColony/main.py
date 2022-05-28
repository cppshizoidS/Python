from grid import Grid
from colony import Colony
from application import Application


grid_map = Grid()

grid_map.load_grid("map.txt")


ants_colony = Colony(grid_map)

app = Application()

app.begin_draw(grid_map)

app.start_app(grid_map, ants_colony)
