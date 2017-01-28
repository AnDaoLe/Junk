import random, string
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    """QUESTION: What states have you identified that are appropriate for modeling the smartcab and environment? Why do you believe each of these states to be appropriate for this problem?"""
    """ The states whether they can move or not move in the direction, whether there is another vehicle in the way, whether they are to the right of the vehcile"""
    

    """learning rate (alpha), the discount factor (gamma) and the exploration rate (epsilon)"""        
    
    """using this idea from forums:
    Q-learning method 2:
1) Sense the environment (see what changes occur naturally in the environment) - store it as state_0
2) Take an action/reward - store as action_0 & reward_0

In the next iteration
1) Sense environment (see what changes occur naturally and from an action) - store as state_1
2) Update the Q-table using state_0, action_0, reward_0, state_1
3) Take an action - get a reward"""

    
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        
        # TODO: Initialize any additional variables here
        self.Q={}
        self.alpha=1.0
        self.gamma=0.5
        self.epsilon=.8
        self.total_reward=0
        self.policy=0
        self.next_state=None
        self.next_action=None
        #action = 
        #recall state is already randomize - self.state=[randint(1,6),randint(1,8)]
        self.qtable = {}
        self.avaiable_actions = [None, 'left', 'right', 'forward']
        waypoints = ['forward', 'left', 'right']
        trafficlight = ['red','green']
        oncoming = [None, 'left', 'right', 'forward']
        right = [None, 'left', 'right', 'forward']
        left = [None, 'left', 'right', 'forward']
        state = ()
 
        self.q_val = 0
        self.max_val = 0
        for a in waypoints:
                for b in trafficlight:
                        for c in oncoming:
                                for d in right:
                                    for e in left:
                                        new_key = (a,b,c,d,e)
                                        self.qtable[new_key] = {None:0, 'forward':0, 'right':0, 'left':0}
                                        
        
         #states[('forward', 'red', 'right', 'right', 'right')]['forward'] = 2
        #print self.qtable
        # do something different
        
    def Qmax(self, current_state):

        for state in self.qtable:
            for actions in self.avaiable_actions:
                if state == current_state and self.qtable[(state)][actions] > self.q_val:
                    #print "2", state
                    #print "2",current_state, qtable[(state)], actions
                    self.max_val = actions
                    q_val = self.qtable[(state)][actions]
    
        return self.max_val
            
    def mod_Q( self,state,action, reward):
            if  state not in qtable:
                 self.qtable[(state)][action] = 0
                 print "3", 
            else:
                 self.qtable[(state)][action] += (1-alpha)*(qtable[(state)][action])+alpha*(reward+reward*qtable[(state)][action])
                 print "3" , state, action

            
    
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        
        #Q=(1-alpha)*Q+alpha*(r+r*max(Q(s,a))
        alpha=self.alpha
        # TODO: Update state
        state = ()
        for x,y in inputs.items():
            state = state + (y,)
            print state
        state =  (self.next_waypoint,)    + state
        print "state :",state
        #the states are as follows: 
        # TODO: Select action according to your policy
        #action = argmax(self, current_state, table)
        action = self.Qmax(state)
        
        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        #argM_Q=max()
        #Q=(1-alpha)*Q+self.alpha*(reward+reward*argM_Q)
        #state=
        #Q=(1-alpha)*Q+alpha*(reward+reward*self.next_waypoint)
        #print Q
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        print "Waypoint: {}".format(self.next_waypoint)
        

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False
    
    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
