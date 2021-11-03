#!/usr/bin/python

import sys
import argparse
import math
from fcm import Fcm
import random

def checkAlphaValue(a):
    ### Function to ensure alpha is between 0 and 1
    a = float(a)
    if a > 1 or a <= 0:
        raise argparse.ArgumentTypeError("Alpha must be a value within [0,1]")
    return a

def main():

    ### Verify Parameters
    parser = argparse.ArgumentParser(description='Define filename, context length, the smoothing parameter and the size of text to be generated.')
    parser.add_argument('-f', type=str, required=True)
    parser.add_argument('-k', type=int, required=True)
    parser.add_argument('-a', type=checkAlphaValue, required=True)
    parser.add_argument('-l', type=int, required=True)
    args = parser.parse_args()

    file_name = args.f
    k = args.k
    alpha = args.a
    text_size = args.l

    if text_size < k:
        print("Error: Can't generate text with size smaller than k.")
        sys.exit()

    ### Read Content
    try:
        f = open(file_name, "r")
        file_content = f.readlines()
        f.close()
    except OSError:
        print("Error opening file: ", file_name)
        sys.exit()

    # Create variable text that is a String with all content 
    text = ""
    for line in file_content:
        text += line

    ### Creation of Finite Context Model
    fcm_model = Fcm(text, k, alpha)
    fcm_model.create_fcm_model()
    print(fcm_model)

    ### Calculate entropy
    fcm_model.calculate_entropy()

    # Probabilities of each char in each context/state 
    state_probabilities = fcm_model.state_probabilities

    # Get the first context that is the first one, but can be a different one
    context = list(state_probabilities.keys())[0]

    generated_text = context    # Initialize the generated text with first context
    for i in range(0, text_size-k):     # Iterate text_size - k times because the first context with k chars is already in the generated text
        if context in state_probabilities:
            # Random char choice using their probabilities according to this context
            generated_text += random.choices( list(state_probabilities[context].keys()), list(state_probabilities[context].values()), k=1)[0]
        else:
            # If the context does not exist in the fcm model, then assign a random character (It can be risky, discuss later about this)
            generated_text += random.choice(list(fcm_model.alphabet))
        # Update context with the new generated char
        context = context[1:] + generated_text[-1]

    print("Generated text: ", generated_text)

if __name__ == "__main__":
    main()