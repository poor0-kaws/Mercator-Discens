import numpy as np 
import random

class Casino: 
    def __init__(self, num_lever=3):
        self.__true_probs = np.random.uniform(0,1,num_lever) # True Probs of levers 
    
    def pull_lever(self, lever): 
        if random.random() < self.__true_probs:
            return 1 # win
        else: 
           return 0 # los
        
        
class Agent: 
    def __init__(self, num_lever=3):
        self.epsilon = 1 # willingnesss to explore different options
        self.eps_decay = 0.995 # willingness decreases over long time --> switch to exploit
        self.min_eps = 0.1
        self.q_table = np.zeros(num_lever) # Estimated Agent Probs of levers 
        self.count_wins = np.zeros(num_lever)
        self.attempts = np.zeros(num_lever)
           
    def choose_action(self, num_lever=3): # Choose action (Exploration or Exploitation)
        
        # Promote Exploration 
        if random.random() < self.epsilon:
            return random.randint(0, num_lever - 1)
    
        return np.argmax(self.q_table) # Returns the lever (1, 2, or 3...n)

    def reduce_exploration(self): 
        # Reduces willingness to explore 
        self.epsilon =  max(self.min_eps, self.epsilon * self.eps_decay)

    def learn(self, lever, reward): 
        """Reduces exploration & updates the lever probabilites"""
        
        self.attempts[lever] += 1 

        if reward == 1: 
            self.count_wins[lever] += 1
        else: 
            self.count_wins[lever] += 0
        
        reduce_exploration()      
        
        self.q_table[lever] = self.count_wins[lever] / self.attempts[lever] # Updating the probabilites for the pulled lever
        

env = Casino()
agent = Agent()

for episode in range (100): 
    action = agent.choose_action(num_lever=3)
    result = env.pull_lever(action)
    agent.learn(action, result)


    



        


    

 

 
    
    
    
    