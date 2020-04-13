import numpy as np
import pandas as pd
import time

# numpy 随机数种子，便于每次运行产生相同的结果
np.random.seed(2)

# 算法参数设置
N_STATES = 6                        # 状态数
ACTIONS = ['left', 'right']         # 动作空间
EPSILON = 0.9                       # greedy算法的参数，随机数大于该值，则按照 q_table 选取动作，否则随机选取动作
ALPHA = 0.1                         # 学习率
GAMMA = 0.9                         # 衰减系数
MAX_EPISODES = 13                   # 最大训练轮数
FRESH_TIME = 0.3                    # 环境更新间隔


# 初始化 q_table
def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),
        columns=actions
    )
    return table


# 按照 greedy 算法选择动作
def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.idxmax()
    return action_name


# 得到环境的反馈
def get_env_feedback(state, action):
    reward = 0
    if action == 'right':
        if state == N_STATES-2:
            state_ = 'terminal'
            reward = 1
        else:
            state_ = state+1
    else:
        if state == 0:
            state_ = state
        else:
            state_ = state-1
    return state_, reward


# 更新环境
def update_env(state, episode, step_counter):
    env_list = ['-']*(N_STATES-1) + ['T']
    if state == 'terminal':
        interaction = "Episode %s: total steps = %s" % (episode+1, step_counter)
        print("\r{}".format(interaction), end="")                # '\r' 表示打印之后，光标回到本行起点处
        time.sleep(2)
    else:
        env_list[state] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end="")
        time.sleep(FRESH_TIME)


# 算法主体
def rl():
    # 初始化 q_table
    q_table = build_q_table(N_STATES, ACTIONS)

    for episode in range(MAX_EPISODES):
        step_counter = 0
        state = 0
        is_terminated = False
        update_env(state, episode, step_counter)

        while not is_terminated:
            action = choose_action(state, q_table)
            state_, reward = get_env_feedback(state, action)
            q_predict = q_table.loc[state, action]
            if state_ != 'terminal':
                q_target = reward + GAMMA*q_table.iloc[state_, :].max()
            else:
                q_target = reward
                is_terminated = True

            # 更新 q_table
            q_table.loc[state, action] += ALPHA*(q_target-q_predict)
            state = state_

            # 更新环境表示
            step_counter += 1
            update_env(state, episode, step_counter)

    return q_table


if __name__ == '__main__':
    q_table = rl()
    print('\r\nQ-table:\n')
    print(q_table)








