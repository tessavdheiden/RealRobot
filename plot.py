import support.firebase as fbdb
import matplotlib.pyplot as plt

db = fbdb.db

episode_key = '-LqQvV_oSZKvMxu4e6Jt'

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
    plt.plot(positions_x, positions_y)
    plt.show()
