import support.firebase as fbdb
import matplotlib.pyplot as plt

db = fbdb.db

episode_key = '-LrijYL5Wpn5O00ifspU'

goal_x = None
goal_y = None
positions_x = []
positions_y = []
velocities_x = []
velocities_y = []

data = db.child('memories').child('IL').child(episode_key).get().val()

if data:
    goal_x = data['goal_x']
    goal_y = data['goal_y']
    positions_x = data['positions_x']
    positions_y = data['positions_y']
    velocities_x = data['velocities_x']
    velocities_y = data['velocities_y']
    plt.scatter(positions_x, positions_y)
    plt.axis('square')
    plt.show()
