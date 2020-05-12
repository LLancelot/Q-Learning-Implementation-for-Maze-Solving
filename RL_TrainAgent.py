import numpy as np
import pandas as pd


class QLearningMain:
    def __init__(self, actions, learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.9):
        self.actions = actions  # a list
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.learningRate = learning_rate
        self.gamma = reward_discount
        self.epsilon = e_greedy_rate

    def choose_action(self, observation):
        # check if state exists, if not, then append it.
        self.check_state_exist(observation)
        # action selection
        # if rand in (0~epsilon), then use Q learning, otherwise choose randomly.
        if np.random.uniform() < self.epsilon:
            # choose action with best Q-Value
            state_action = self.q_table.loc[observation, :]

            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'END':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is END
            print(self.q_table)
        self.q_table.loc[s, a] += self.learningRate * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        # if not exists, then append it
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def getParameter(self, para):
        if para == 'e_greedy':
            return self.epsilon
        elif para == 'reward_discount':
            return self.gamma
        elif para == 'learning_rate':
            return self.learningRate

    def getQTable(self):
        return self.q_table