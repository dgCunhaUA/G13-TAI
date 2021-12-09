#!/usr/bin/python

import sys
import argparse
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
    parser.add_argument('-f', type=str, required=True, help='Path to file with an text example')
    parser.add_argument('-k', type=int, required=True, help='Context length')
    parser.add_argument('-a', type=checkAlphaValue, required=True, help='Smoothing parameter')
    parser.add_argument('-l', type=int, required=True, help='Desired size of the generated text')
    args = parser.parse_args()

    file_name = args.f
    k = args.k
    alpha = args.a
    text_size = args.l

    if text_size <= 0:
        print("Error: Can't generate text with size smaller than 0.")
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

    ### Calculate entropy
    fcm_model.calculate_entropy()

    # Probabilities of each char in each context/state 
    state_probabilities = fcm_model.state_probabilities
    # Probabilities of each context in the text
    context_probabilities = fcm_model.context_probabilities

    # Get the first context that is the first one, but can be a different one
    context = list(context_probabilities.keys())[0]

    if text_size < k:
        generated_text = context[:text_size]    # The generated text will be the first text_size chars of first context
    else:
        generated_text = context     # Initialize the generated text with first context

        while len(generated_text) != text_size: # Iterate until we finished generating text with size text_size
            if context in state_probabilities:
                # Random char choice using their probabilities according to this context
                generated_text += random.choices( list(state_probabilities[context].keys()), list(state_probabilities[context].values()), k=1)[0]
            else:
                
                if text_size - len(generated_text) >= k:  # If the remaning text has size > k
                    # Choose a random context using their probabilities
                    generated_text += random.choices( list(context_probabilities.keys()), list(context_probabilities.values()), k=1)[0]   
                else:
                    # Assign a random character
                    generated_text += random.choice(list(fcm_model.alphabet))
                
            # Update context with last k chars of the new generated text
            context = generated_text[-k:]

    print("Generated text: ", generated_text)

if __name__ == "__main__":
    main()