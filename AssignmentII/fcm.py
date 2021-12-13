#!/usr/bin/python

import copy
import sys

class Fcm:

    def __init__(self, reference_file_name:str, k:int, alpha:float):
        self.k = k
        self.alpha = alpha
        self.state_probabilities = {}   # Probabilities of each char in each context
        self.number_of_states = 0       # Number of total states(contexts) in text
        self.alphabet = set()           # Different chars in text
        self.model = {}
        self.create_fcm_model(reference_file_name)

    def create_fcm_model(self, reference_file_name:str):
        # Creation of fcm model in iterative way
        try:
            f = open(reference_file_name, "r", encoding='utf-8-sig')
            ctx = f.read(self.k)
            char = f.read(1)
            while char:
                self.alphabet.add(char)     # Add char to alphabet set
                self.number_of_states += 1  # Increment number of states
                if ctx in self.model:
                    if char in self.model[ctx]:
                        self.model[ctx][char] += 1
                    else:
                        self.model[ctx][char] = 1
                else:
                    self.model[ctx] = {}
                    self.model[ctx][char] = 1
                ctx = ctx[1:] + char
                char = f.read(1)
            f.close()
        except OSError:
            print("Error opening file: ", reference_file_name)
            sys.exit()


    def calculate_probabilities(self):

        alphabet_size = len(self.alphabet)

        self.state_probabilities = copy.deepcopy(self.model) # Same dictionary with the same keys to store the value of the probabilities of each char

        for state in self.model.keys():
            state_info = self.model[state]
            state_sum = sum(state_info.values())  # Sum of occurences
            
            
            number_of_not_shown_chars = alphabet_size - len(state_info) # Number of chars that didn't appear
            if number_of_not_shown_chars != 0:  # If there are at least one char that didn't appear
                # Probability calculation with alpha parameter 
                prob_chars = self.alpha / (state_sum + self.alpha * alphabet_size )
                
                for char in self.alphabet:
                    self.state_probabilities[state][char] = prob_chars   # Save the probability
                    
            for char in state_info: 
                # Probability calculation with alpha parameter 
                prob_char = (state_info[char] + self.alpha) / (state_sum + self.alpha * alphabet_size )
                self.state_probabilities[state][char] = prob_char   # Save the probability