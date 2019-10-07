import math
import support.firebase as fbdb

class Episode:
    def __init__(self) -> None:
        super().__init__()
        self.key = None
        self.step_number = 0
        self.episode_started = False
        self.episode_ended = None
        self.positions_x = []
        self.positions_y = []
        self.velocities_x = []
        self.velocities_y = []
        self.rewards = []
        self.actions = []
        self.thetas = []
        self.goal_x = None
        self.goal_y = None
        self.db = fbdb.db
        self.setStreamer()


    def incrementStepNumber(self):
        self.step_number += 1

    def setPositions(self, pos_x, pos_y):
        self.positions_x.append(pos_x)
        self.positions_y.append(pos_y)

    def setVelocities(self, vel_x, vel_y):
        self.velocities_x.append(vel_x)
        self.velocities_y.append(vel_y)
        #self.thetas.append(math.atan(vel_y, vel_x))

    def setReward(self, reward):
        self.rewards.append(reward)

    def checkGoalReached(self, pos_x, pos_y):
        #Use Pythagoras to get a zone for robot to enter
        if ((self.goal_x - pos_x) ** 2 + (self.goal_y - pos_y) ** 2) ** 0.5 < 0.5:
            return True
        else:
            return False

    def episode_stream_handler(self, message):
        if message['data']:
            for k, v in message['data'].items():
                if k == 'episodeStarted':
                    self.episode_started = bool(v)
                if k == 'goalPosX':
                    self.goal_x = float(v)
                if k == 'goalPosY':
                    self.goal_y = float(v)
                if k == 'episodeEnded':
                    self.episode_ended = str(v)
                if k == 'key':
                    self.key = str(v)


    def setStreamer(self):
        self.db.child('currentEpisode').stream(self.episode_stream_handler)

    def uploadToServer(self, ending_message):
        self.db.child('currentEpisode').update({
            'episodeEnded': ending_message,
            'episodeStarted': False
        })

        values = []
        for i, reward in enumerate(self.rewards):
            values.append(sum([pow(self.gamma, max(t - i, 0) * self.robot.time_step * self.robot.v_pref) * reward
             * (1 if t >= i else 0) for t, reward in enumerate(self.rewards)]))

        self.db.child('memories').child('IL').child(self.key).update({
            'positions_x': self.positions_x,
            'positions_y': self.positions_y,
            'rewards': values,
            'velocities_x': self.velocities_x,
            'velocities_y': self.velocities_y,
            'thetas': self.thetas,
            'goal_x': self.goal_x,
            'goal_y': self.goal_y,
            'episodeEnded': ending_message
        })



