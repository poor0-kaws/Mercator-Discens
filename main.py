import numpy as np 
import random

class Casino: 
    def __init__(self, num_lever=3):
        self.q_table = np.zeros(num_lever)
        self.count_wins = np.zeros(num_lever)
        self.reward = np.zeros(num_lever)
        self.attempts = np.zeros(num_lever)
        
class Agent: 
    def __init__(self, num_lever=3):
        self.epsilon = 1 # willingnesss to explore different options
        self.eps_decay = 0.995 # willingness decreases over long time --> switch to exploit
        self.min_eps = 0.1
           
    def choose_action(self, num_lever=3): # Choose action 
        
        # Promote Exploration 
        if random.random() < self.epsilon:
            return random.randint(0, num_lever - 1)
        
        return np.argmax(self.q_table) # Returns the lever (1, 2, or 3...n)

    def reduce_exploration(self): 
        # Reduces willingness to explore 
        self.epsilon =  max(self.min_eps, self.epsilon * self.eps_decay)

    def learn(self, lever): 
        """ Gives reward for the action and updates the lever probabilites"""
        
        if random.random() < self.q_table[lever]: 
            self.attempts[lever] += 1 
            self.count_wins[lever]  += 1 # Win
            self.reward[lever] += 100
        else: 
            self.attempts[lever] += 1 
            self.count_wins[lever] += -1 # Loss
            self.reward[lever] -=100
        
        reduce_exploration()      
    
        self.q_table[lever] = self.count_wins[lever] / self.attempts[lever] # Updating the probabilites for the pulled lever
        

env = casino()
agent = Agent()

for episode in range (100): 
    action = agent.choose_action(num_lever=3)
    learn = casino.result(action)


    



        


    

 

 
    
    
    
    