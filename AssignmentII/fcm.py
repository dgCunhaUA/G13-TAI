#!/usr/bin/python

import copy

class Fcm:

    def __init__(self, text:str, k:int, alpha:float):
        self.text = text
        self.k = k
        self.alpha = alpha

        ### Get Alphabet
        self.alphabet = set()
        for character in text:
            self.alphabet.add(character)

        # Number of total states(contexts) of text, calculated based on k value
        self.number_of_states = len(self.text) - k

        self.model = {}
        self.state_probabilities = {}   # Probabilities of each char in each context

    
    def create_fcm_model(self):
        # Creation of fcm model in iterative way
        self.model = {}
        for i in range(0, len(self.text)-self.k):
            ctx = self.text[i:i+self.k]
            char = self.text[i+self.k:i+self.k+1]
            if ctx in self.model:
                if char in self.model[ctx]:
                    self.model[ctx][char] += 1
                else:
                    self.model[ctx][char] = 1
            else:
                self.model[ctx] = {}
                self.model[ctx][char] = 1


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