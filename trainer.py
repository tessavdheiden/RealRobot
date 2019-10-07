import support.firebase as fbdb
import time
import logging
import threading
import torch
from model.memory import ReplayMemory
from model.model import ValueNetwork
from model.state import FullState
from torch.utils.data import DataLoader
from torch.autograd import Variable

class Trainer:
    def __init__(self, batch_size, device):
        self.memory = ReplayMemory(capacity=10000)
        self.batch_size = batch_size
        self.epochs = 50
        self.device = device
        self.db = fbdb.db
        self.data_loader = None
        self.download_finished = threading.Event()

    def downloadMemories(self):
        memories = self.db.child('memories').child('IL').get().val()
        if memories:
            self.download_finished.set()
            for memory_key, memory_values in memories.items():
                if memory_values:
                    goal_x = None
                    goal_y = None
                    positions_x = None
                    positions_y = None
                    velocities_x = None
                    velocities_y = None
                    if 'episodeEnded' in memory_values.keys():
                        episode_ended = memory_values['episodeEnded']
                        if episode_ended == 'Reach Goal' or episode_ended == 'Collision' or episode_ended == 'Timeout':
                            if memory_values['goal_x']:
                                goal_x = memory_values['goal_x']
                            if memory_values['goal_y']:
                                goal_y = memory_values['goal_y']
                            if memory_values['positions_x']:
                                positions_x = memory_values['positions_x']
                            if memory_values['positions_y']:
                                positions_y = memory_values['positions_y']
                            if memory_values['velocities_x']:
                                velocities_x = memory_values['velocities_x']
                            if memory_values['velocities_y']:
                                velocities_y = memory_values['velocities_y']
                            if goal_x and goal_y and positions_x and positions_y and velocities_x and velocities_y:
                                for i in range(len(positions_x)):
                                    state = FullState(px=positions_x[i],
                                                      py=positions_y[i],
                                                      vx=velocities_x[i],
                                                      vy=velocities_y[i],
                                                      gx=goal_x,
                                                      gy=goal_y,
                                                      theta=0.0)
                                    state = torch.cat([torch.Tensor([state.px]),
                                                      torch.Tensor([state.py]),
                                                      torch.Tensor([state.vx]),
                                                      torch.Tensor([state.vy]),
                                                      torch.Tensor([state.gx]),
                                                      torch.Tensor([state.gy]),
                                                      torch.Tensor([0.0])])
                                    self.memory.push(state)

    def train(self):

        self.download_finished.wait()

        if self.data_loader is None:
            self.data_loader = DataLoader(self.memory, self.batch_size, shuffle=True)

        for e in range(self.epochs):
            start_time = time.time()
            losses = 0
            for data in self.data_loader:
                states = data
                states = Variable(states).to(self.device)

                losses += 1

            logging.info('Epoch: {}, Loss: {}, Time: {}', e, losses, time.time() - start_time)
trainer = Trainer(1000, 'cpu')
trainer.downloadMemories()
trainer.train()




