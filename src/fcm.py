#!/usr/bin/python

import sys
import argparse
import math
import copy


## Not used. Can be removed
def fill_fcm_model(text, k, fcm_model):
    # Recursive way to create fcm_model has the problem of "Maximum recursion depth exceeded" when running with a big text
    # That's why we must use a iterative function instead

    if len(text) <= k:
        return fcm_model

    ctx = text[:k]
    letter = text[k:k+1]
    if ctx in fcm_model:
        if letter in fcm_model[ctx]:
            fcm_model[ctx][letter] += 1
        else:
            fcm_model[ctx][letter] = 1
    else:
        fcm_model[ctx] = {}
        fcm_model[ctx][letter] = 1

    return fill_fcm_model(text[1:], k, fcm_model)




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

        self.alphabet_size = len(self.alphabet)
        self.model = {}
        self.final_entropy = 0
        self.state_probabilities = {}

    
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


    def calculate_entropy(self):
        ### Entropy calculation

        self.state_probabilities = copy.deepcopy(self.model) # Same dictionary with the same keys to store the value of the probabilities of each char
        self.final_entropy = 0
        for state in self.model.keys():
            state_info = self.model[state]
            state_sum = sum(state_info.values())  # Sum of occurences
            state_entropy = 0
            
            if self.alpha > 0:  # If alpha != 0, the probabilities of the chars that didn't appear next to these context have importance
                number_of_not_shown_chars = self.alphabet_size - len(state_info) # Number of chars that didn't appear
                if number_of_not_shown_chars != 0:  # If there are at least one char that didn't appear
                    # Probability calculation with alpha parameter 
                    prob_chars = self.alpha / (state_sum + self.alpha * self.alphabet_size )
                    
                    # Entropy multiplied by the number of chars that didn't appear
                    state_entropy += number_of_not_shown_chars * (prob_chars * math.log2(prob_chars))
                    
                    for char in self.alphabet:
                        self.state_probabilities[state][char] = prob_chars   # Save the probability
                    
            for char in state_info: 
                # Probability calculation with alpha parameter 
                prob_char = (state_info[char] + self.alpha) / (state_sum + self.alpha * self.alphabet_size )
                self.state_probabilities[state][char] = prob_char   # Save the probability
                state_entropy += prob_char * math.log2(prob_char)
            
            state_entropy = -state_entropy
            

            # Probability of this context = number of occurences/number of all states
            prob_context = state_sum/self.number_of_states
            self.final_entropy += prob_context * (state_entropy)
            
        #print(self.model)
        print("Final Entropy: " + str(self.final_entropy))

def checkAlphaValue(a):
    ### Function to ensure alpha is between 0 and 1
    a = float(a)
    if a > 1 or a <= 0:
        raise argparse.ArgumentTypeError("Alpha must be a value within [0,1]")
    return a



def main():

    ### Verify Parameters
    parser = argparse.ArgumentParser(description='Define context length and a smoothing parameter.')
    parser.add_argument('-f', type=str, required=True)
    parser.add_argument('-k', type=int, required=True)
    parser.add_argument('-a', type=checkAlphaValue, required=True)
    args = parser.parse_args()

    file_name = args.f
    k = args.k
    alpha = args.a

    ### Read Content
    try:
        f = open(file_name, "r")
        file_content = f.readlines()
        f.close()
    except OSError:
        print("Error opening file: ", file_name)
        sys.exit()

    ### Get Alphabet and String Text
    text = ""
    for line in file_content:
        text += line

    ### Creation of Finite Context Model
    fcm_model = Fcm(text, k, alpha)
    fcm_model.create_fcm_model()

    ### Calculate entropy
    fcm_model.calculate_entropy()

if __name__ == "__main__":
    main()
    