from collections import namedtuple
import random
from minmax import Player, nim_sum_strategy, Nim, match

EPISODES = 10_000  # number of episodes
PRINT_SIZE = 30  # number of lines of output printed
OPP_STRATEGY = nim_sum_strategy  # opponent strategy
EXPLORATION_RATE = 0.1  # fraction of times the agent chooses a never tried action
MAX_REWARD = 10  # absolute value of the maximum reward
DISCOUNT_FACT = 0.9  # discount factor

Action = namedtuple("Action", "heap quantity")

class RLAgent(Player):
    def __init__(self, name: str, explore: bool):
        super().__init__(name, rl_strategy)
        self._explore = explore
        self._Q_table = dict()
        self._frequencies = dict()
        self._previous_state = None
        self._previous_action = None
        self._stats = {'SSE':0, 'updated':0, 'discovered':0}

    @property
    def Q_table(self):
        return self._Q_table

    @property
    def explore(self):
        return self._explore

    @explore.setter
    def explore(self, val):
        self._explore = val

    @property
    def stats(self):
        return self._stats

    def reward(self, state: tuple) -> float:
        return 0

    def generate_actions(self, cur_state: tuple) -> list:
        cur_actions = list()
        # loop for each heap...
        for heap_idx, heap_size in enumerate(cur_state):
            # ... and for each possible quantity to be taken off
            for q in range(1, heap_size+1):

                assert q > 0 and q <= heap_size  # check that the quantity is legal

                a = Action(heap_idx, q)  # create an Action
                cur_actions.append(a)  # add it to the list of legal actions

                # the current state is not in the Q-table add it
                if cur_state not in self._Q_table:
                    self._Q_table[cur_state] = dict()
                    self._frequencies[cur_state] = dict()
                    self._stats['discovered'] += 1

                # if the action for the current state is not in the Q-table add it
                if a not in self._Q_table[cur_state]:
                    self._Q_table[cur_state][a] = self.reward(
                        cur_state)  # compute its reward
                    # set its frequency to zero
                    self._frequencies[cur_state][a] = 0

        return cur_actions

    def learning_rate(self) -> float:
        # decrease with the frequency to ensure convergence of the utilities
        return len(self._Q_table)/(len(self._Q_table) + self._frequencies[self._previous_state][self._previous_action])

    def exploration_function(self, state: tuple) -> Action:
        r = random.random()
        if self._explore and r < EXPLORATION_RATE:  # exploration: choose the action less frequently chosen
            action_freqs = [(a, f)
                            for a, f in self._frequencies[state].items()]
            action_freqs.sort(key=lambda v: v[1])
            return action_freqs.pop(0)[0]
        else:  # exploitation: choose the action with the highest Q-value
            action_Qvals = [(a, q) for a, q in self._Q_table[state].items()]
            action_Qvals.sort(key=lambda v: v[1], reverse=True)
            return action_Qvals.pop(0)[0]

    def policy(self, current_state: Nim):
        cur_state = tuple(current_state.rows)

        assert cur_state is not None
        assert sum(cur_state) > 0
        assert cur_state != self._previous_state

        # generate legal actions from cur_state and add them to the tables
        cur_actions = self.generate_actions(cur_state)

        # update previous state
        if self._previous_state is not None and self._previous_action is not None:

            # increase frequency
            self._frequencies[self._previous_state][self._previous_action] += 1

            # get current state max Q value (utility)
            max_cur_state_Q_val = max(self._Q_table[cur_state].values())  
            
            # get previous state Q value
            prev_state_old_Q_val = self._Q_table[self._previous_state][self._previous_action]

            # compute the new Q value of the previous state
            prev_state_new_Q_val = prev_state_old_Q_val + self.learning_rate()*(
                self.reward(self._previous_state) + DISCOUNT_FACT*max_cur_state_Q_val - prev_state_old_Q_val)

            # save it in the Q table
            self._Q_table[self._previous_state][self._previous_action] = prev_state_new_Q_val

            # add it to the SSE
            self._stats['SSE'] += (prev_state_old_Q_val - prev_state_new_Q_val)**2 
            self._stats['updated'] += 1

        # choose action
        selected_action = self.exploration_function(cur_state)

        current_state.nimming(selected_action.heap,
                              selected_action.quantity, self)

        self._previous_state = cur_state
        self._previous_action = selected_action

    # parameters are flushed before every game, see the play function
    def flush_parameters(self) -> None:
        self._previous_action = None
        self._previous_state = None
        self._stats['SSE'] = 0
        self._stats['updated'] = 0
        self._stats['discovered'] = 0
        super().flush_parameters()

    def update_final_state(self, won: bool) -> None:

        past_val = self._Q_table[self._previous_state][self._previous_action]
        assert past_val is not None

        if won:
            cur_val = MAX_REWARD
        else:
            cur_val = -MAX_REWARD

            self._stats['SSE'] += (past_val - cur_val)**2  # update SSE
            self._stats['updated'] += 1  # increase the number of updated states
            
            # update value
            self._Q_table[self._previous_state][self._previous_action] = cur_val

    def Q_values_MSE(self) -> float:
        # mean squared error of the updated utilities
        if self._stats['updated'] > 0:
            return self._stats['SSE'] / self._stats['updated']
        else:
            return 0


# just a wrapper to make it works with the previous functions
def rl_strategy(agent: RLAgent, state: Nim):
    agent.policy(state)


def reinforcement_learning(heaps: Nim, agent_name: str) -> RLAgent:
    agent = RLAgent(agent_name, explore=True)
    opp = Player("opp", OPP_STRATEGY)
    for e in range(EPISODES):
        # returns a list of tuples (winner_name:str, n_plies:int), but here we have only one game
        winner = match(agent, opp, heaps, n_games=1)[0]

        # update final state, action Q-values with the reward
        if winner[0] == agent_name:
            agent.update_final_state(won=True)
        else:
            agent.update_final_state(won=False)

        # print infos
        if e % int(EPISODES/PRINT_SIZE) == 0:
            print(
                f" Episode: {e}, Q-values MSE = {agent.Q_values_MSE()}, updated states = {agent.stats['updated']}, discovered states = {agent.stats['discovered']}")

    return agent
