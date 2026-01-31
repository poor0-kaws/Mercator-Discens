import numpy as np 
import random

class Casino: 
    def __init__(self, num_lever=3):
        self.__true_probs = np.random.uniform(0,1,num_lever) # True Probs of levers 
    
    def pull_lever(self, lever): 
        if random.random() < self.__true_probs[lever]:
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
        
        self.reduce_exploration()  
        
        self.q_table[lever] = self.count_wins[lever] / self.attempts[lever] # Updating the probabilites for the pulled lever
        

env = Casino()
agent = Agent()

# Multiple Episodes
for episode in range (1000): 
    action = agent.choose_action(num_lever=3)
    result = env.pull_lever(action)
    agent.learn(action, result)

# Formatting for results
def format_values(value): 
    formated = "{:.2f}".format(value)
    return formated

# Print Results
for i in range(3): 
    
    true_prob = format_values(env._Casino__true_probs[i])
    agent_prob = format_values(agent.q_table[i])
    attempts = agent.attempts[i]
    print(f"Slot Machine {i+1} | True Probability: {true_prob} | Agent Probability: {agent_prob} | Total Attempts: {attempts}")

    



        


    

 

 
    
    
    
    