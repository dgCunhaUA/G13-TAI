#!/usr/bin/python

import sys
import argparse
import random
import math

from fcm import Fcm


def get_number_of_bits_required_to_compress(fcm_model, text, target_alphabet, multiplelangflag):

    total_num_bits = 0
    different_chars_in_target = 0

    for char in target_alphabet:
        if char not in fcm_model.alphabet:
            different_chars_in_target += 1

    threshold = -math.log2(fcm_model.alpha / (fcm_model.alpha * len(fcm_model.alphabet))) 
    symbols = dict({})
    words = dict({})
    char_position_in_text = 0

    current_context = random.choice(list(fcm_model.model.keys()))
    for char in text:

        if current_context in fcm_model.state_probabilities:
            if char in fcm_model.state_probabilities[current_context]:
                num_bits = -math.log2( fcm_model.state_probabilities[current_context][char] )
            else:
                num_bits = -math.log2( 1 / different_chars_in_target)
        else:
            num_bits = -math.log2( fcm_model.alpha / (fcm_model.alpha*len(fcm_model.alphabet)) )

        if multiplelangflag and num_bits < threshold:
            symbols[char_position_in_text] = num_bits
            
        total_num_bits += num_bits

        current_context = current_context[1:] + char
        char_position_in_text += 1

    current_pos = 0
    while current_pos < len(text):
        if text[current_pos] == " ":
            current_pos += 1        
            initial_position = current_pos
            new_word = ""
            word_total_bits = 0
            completeWord = True
            while True:
                if current_pos == len(text) - 1:
                    break
                if text[current_pos] != " ":
                    if current_pos in symbols:
                        new_word += text[current_pos]
                        word_total_bits += symbols[current_pos]
                        current_pos += 1
                    else:
                        completeWord = False
                        current_pos += 1
                        break
                else:
                    if completeWord and len(new_word) > 2:
                        words[(new_word, initial_position)] = round(word_total_bits, 3)
                    break
        else:
            current_pos += 1

    return total_num_bits, words


    #for element in symbols:
    #    if text[element-1] == " ":
    #        word_total_bits = symbols[element]
    #        new_word = text[element]
    #        completeWord = True
    #        contador = 1
    #        for char in text[element+1:]:
    #            if char != " ":
    #                if element+contador in symbols:
    #                    new_word += char
    #                    word_total_bits += symbols[element]
    #                    contador += 1
    #                else:
    #                    completeWord = False
    #            else:
    #                break       
    #        if completeWord and len(new_word) > 2:
    #            words[new_word] = round(word_total_bits, 3)


    #return total_num_bits, words
            

def checkAlphaValue(a):
    ### Function to ensure alpha is between 0 and 1
    a = float(a)
    if a > 1 or a <= 0:
        raise argparse.ArgumentTypeError("Alpha must be a value within ]0,1]")
    return a



def main(reference_file_name, target_file_name, k, alpha, multiplelangflag):

    reference_file_text = ""
    target_file_text = ""
    
    ### Read Content of reference file
    try:
        f = open(reference_file_name, "r", encoding='utf-8-sig')
        file_content = f.readlines()
        f.close()

        ### Get String Text
        for line in file_content:
            reference_file_text += line

    except OSError:
        print("Error opening file: ", reference_file_name)
        sys.exit()

    ### Read Content of target file
    try:
        f = open(target_file_name, "r", encoding='utf-8-sig')
        file_content = f.readlines()
        f.close()

        ### Get String Text
        for line in file_content:
            target_file_text += line

        ### Get Target Alphabet
        target_alphabet = set()
        for character in target_file_text:
            target_alphabet.add(character)

    except OSError:
        print("Error opening file: ", target_file_name)
        sys.exit()
    

    ### Creation of Finite Context Model from reference text
    fcm_model = Fcm(reference_file_text, k, alpha)
    fcm_model.create_fcm_model()

    ### Calculate entropy
    fcm_model.calculate_probabilities()

    bits, foreign_words = get_number_of_bits_required_to_compress(fcm_model, target_file_text, target_alphabet, multiplelangflag)
    
    return bits, foreign_words



if __name__ == "__main__":
    ### Verify Parameters
    parser = argparse.ArgumentParser(description='Define context length and a smoothing parameter.')
    parser.add_argument('-freference', type=str, required=True, help='Path to reference file with an text example')
    parser.add_argument('-ftarget', type=str, required=True, help='Path to target file')
    parser.add_argument('-k', type=int, required=True, help='Context length')
    parser.add_argument('-a', type=checkAlphaValue, required=True, help='Desired size of the generated text')
    parser.add_argument('--multiplelang', action='store_true', required=False, default=True, help='Flag to check for multiple lang in the target text')
    args = parser.parse_args()

    reference_file_name = args.freference
    target_file_name = args.ftarget
    k = args.k
    alpha = args.a
    multiplelangflag = args.multiplelang
    
    main(reference_file_name, target_file_name, k, alpha, multiplelangflag)
    