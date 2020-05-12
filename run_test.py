from maze_environment import Maze
from RL_TrainAgent import QLearningMain
import matplotlib.pyplot as plt
import os
import pandas as pd

wd = os.getcwd()
output_file = os.path.join(wd, 'q_table_episode_result.csv')
x_axis = []
y_axis = []


def update():
    for episode in range(150):
        # initial decision_observe
        decision_observe = env.reset()
        total_step = 0

        while True:
            # fresh env
            env.render()
            total_step += 1
            # robot choose action based on decision_observe
            action = RL.choose_action(str(decision_observe))
            # take action and get reward from the environment
            step_observe, reward, done = env.step(action)
            # robot learns from the information(each step it takes and each state & reward)
            RL.learn(str(decision_observe), action, reward, str(step_observe))
            # based on MDP, swap the decision processes: N and N-1
            decision_observe = step_observe

            # break while loop when end of this episode
            if done:
                if reward != -1:
                    # win the game
                    x_axis.append(episode+1)
                    y_axis.append(total_step)
                    RL.getQTable().to_csv(output_file, index=False)
                # print("Total Reward: ", reward, ", Total movement: ", total_step, sep="")
                total_step = 0
                break

    _egreedy = str(RL.getParameter("e_greedy"))
    _discount = str(RL.getParameter("reward_discount"))
    _rl = str(RL.getParameter("learning_rate"))
    title_str ="Training 150 Episodes with reward = 100,\n" + " epsilon =" + _egreedy + ", discount factor = "+ _discount + ", learning rate = "+ _rl

    plt.title(title_str)
    plt.plot(x_axis, y_axis, c='red')
    plt.xlabel("Episode")
    plt.ylabel("Finished Steps")
    plt.show()

    print('GAME OVER!')
    env.destroy()

if __name__ == "__main__":
    env = Maze()
    action_lst = list(range(env.len_actions))
    # RL = QLearningMain(actions=list(range(env.len_actions)))
    RL = QLearningMain(action_lst,learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.8)
    # RL = QLearningMain(actions=list(range(env.len_actions)),learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.7)
    # RL = QLearningMain(actions=list(range(env.len_actions)),learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.6)

    # RL = QLearningMain(actions=list(range(env.len_actions)),learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.9)
    # RL = QLearningMain(actions=list(range(env.len_actions)),learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.9)
    # RL = QLearningMain(actions=list(range(env.len_actions)),learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.9)

    # RL = QLearningMain(actions=list(range(env.len_actions)),learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.9)
    # RL = QLearningMain(actions=list(range(env.len_actions)),learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.9)
    # RL = QLearningMain(actions=list(range(env.len_actions)),learning_rate=0.01, reward_discount=0.9, e_greedy_rate=0.9)

    env.after(50, update)
    env.mainloop()