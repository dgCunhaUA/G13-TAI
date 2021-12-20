#!/usr/bin/python

import sys
import argparse
import random
import math

from fcm import Fcm


####
# Argument Verification Function
####

def checkAlphaValue(a):
    ### Function to ensure alpha is greater than 0
    try:
        a = float(a)
    except:
        raise argparse.ArgumentTypeError("Alpha must be a value greater than 0")
   
    if a <= 0:
        raise argparse.ArgumentTypeError("Alpha must be a value greater than 0")
    return a

def checkKValue(k):
    ### Function to ensure k is an integer value greater than 0
    try:
        k = int(k)
    except:
        raise argparse.ArgumentTypeError("K must be an integer value greater than 0")
    
    if k <= 0:
        raise argparse.ArgumentTypeError("K must be an integer value greater than 0")
    return k



####
# Function that calculates number of bits required to compress a target file using a finite context model from a reference file.
#   - MultipleLangFlag is used to also store the set of words contained in target file that belong to reference file language.
####
"""
def get_number_of_bits_required_to_compress_v1(fcm_model, target_file_name, target_alphabet, multiplelangflag):

    total_num_bits = 0
    different_chars_in_target = 0

    for char in target_alphabet:
        if char not in fcm_model.alphabet:
            different_chars_in_target += 1

    threshold = -math.log2(fcm_model.alpha / (fcm_model.alpha * len(fcm_model.alphabet)))   

    words = dict({})
    char_position_in_text = 0

    current_context = random.choice(list(fcm_model.model.keys()))

    ### Read Content of target file
    try:
        f = open(target_file_name, "r", encoding='utf-8-sig')
        
        word_creation = True       # Flag to tell that a word is being created
        new_word = ""
        word_total_bits = 0    
        initial_position = 0
        valid_word = True

        char = f.read(1)
        while char:
            if current_context in fcm_model.state_probabilities:
                if char in fcm_model.state_probabilities[current_context]:
                    num_bits = -math.log2( fcm_model.state_probabilities[current_context][char] )
                else:
                    num_bits = -math.log2( 1 / different_chars_in_target)
            else:
                num_bits = -math.log2( fcm_model.alpha / (fcm_model.alpha*len(fcm_model.alphabet)) )
                
            total_num_bits += num_bits

            if multiplelangflag: 
                if word_creation:                       # If a word is being created
                    if char != " " and char != '\n':    
                        if num_bits<threshold:   # If the char is compressed using a number of bits below the threshold
                            new_word += char            # Append the char to the word
                            word_total_bits += num_bits # Add the number of bits of this char to the word's total number of bits
                        else:
                            valid_word = False          # Flag to tell that this word has symbols that are not in this language, that's why it will not be saved
                    else:
                        if valid_word and len(new_word) > 2:      # Check if the word is valid. 1 - If it has no foreign symbols; 2 - If it has more than two chars
                            words[(new_word, initial_position + 1)] = round(word_total_bits, 3)
                        word_creation = False           # Word creation process ended
                
                if char == " " and not word_creation:   # This means that a new word will be created
                    new_word = ""                       # String for creating the word
                    word_total_bits = 0                 # Total number of bits of the word
                    initial_position = char_position_in_text    # Initial position of the word in text
                    valid_word = True                   # Flag used to tell that the word has symbols that are not in this language
                    word_creation = True                # Flag to tell that a new word will be created

            current_context = current_context[1:] + char    # Update the context
            char = f.read(1)                        
            char_position_in_text += 1

        f.close()

    except OSError:
        print("Error opening file: ", target_file_name)
        sys.exit()
    
    return total_num_bits, words

"""










####
# Function that calculates number of bits required to compress a target file using a finite context model from a reference file.
#   - MultipleLangFlag is used to also store the sections of chars contained in target file that are well compressed.
####
def get_number_of_bits_required_to_compress_v2(fcm_model, target_file_name, target_alphabet, window_size, multiplelangflag, nonlangsections):

    total_num_bits = 0
    different_chars_in_target = 0

    for char in target_alphabet:
        if char not in fcm_model.alphabet:
            different_chars_in_target += 1

    sections_dict = []

    current_context = random.choice(list(fcm_model.model.keys()))

    if nonlangsections == None:
        threshold = math.log2(len(target_alphabet)) / 2   

        ### Read Content of target file
        try:
            f = open(target_file_name, "r", encoding='utf-8-sig')
            
            window_initial_pos = 0
            window_buffer = [ None for i in range(window_size)]

            initial_chars = f.read(window_size)
            for i in range(len(initial_chars)):
                char = initial_chars[i]
                if current_context in fcm_model.state_probabilities:
                    if char in fcm_model.state_probabilities[current_context]:
                        num_bits = -math.log2( fcm_model.state_probabilities[current_context][char] )
                    else:
                        num_bits = -math.log2( 1 / different_chars_in_target)
                else:
                    num_bits = -math.log2( fcm_model.alpha / (fcm_model.alpha*len(fcm_model.alphabet)) )
                
                total_num_bits += num_bits

                window_buffer[i] = num_bits
            
            if multiplelangflag:
                window_total_bits = 0
                for i in range(len(window_buffer)):
                    window_total_bits += window_buffer[i]
                if window_total_bits/window_size < threshold:
                    sections_dict.append( (window_initial_pos, window_initial_pos+window_size) )

            char = f.read(1)
            while char:
                window_initial_pos += 1
                
                if current_context in fcm_model.state_probabilities:
                    if char in fcm_model.state_probabilities[current_context]:
                        num_bits = -math.log2( fcm_model.state_probabilities[current_context][char] )
                    else:
                        num_bits = -math.log2( 1 / different_chars_in_target)
                else:
                    num_bits = -math.log2( fcm_model.alpha / (fcm_model.alpha*len(fcm_model.alphabet)) )
                    
                total_num_bits += num_bits

                if multiplelangflag: 
                    ### Get the char position in buffer that does not belong to this new section
                    previous_char_index = (window_initial_pos + window_size - 1) % window_size

                    ### Remove the number of bits of this char to the window_total_bits
                    window_total_bits -= window_buffer[previous_char_index]

                    ### Sum the number of bits of the new char to the window_total_bits
                    window_total_bits += num_bits

                    ### Save the number of bits of the new char in the previous char position
                    window_buffer[previous_char_index] = num_bits

                    if window_total_bits/window_size < threshold:
                        sections_dict.append( (window_initial_pos, window_initial_pos+window_size) )
                

                current_context = current_context[1:] + char    # Update the context
                char = f.read(1)                        

            f.close()

        except OSError:
            print("Error opening file: ", target_file_name)
            sys.exit()
    else:
        threshold = (3*math.log2(len(target_alphabet))) / 4   
        char_position_in_text = 0

        ### Read Content of target file
        try:
            f = open(target_file_name, "r", encoding='utf-8-sig')
            
            for section in nonlangsections:

                section_initial_pos = section[0]
                section_final_pos = section[1]

                window_initial_pos = 0

                if section_initial_pos - window_size < 0:
                    f.seek(0)
                    char_position_in_text = 0
                    window_initial_pos = 0
                else:
                    f.seek(section_initial_pos - window_size)
                    char_position_in_text = section_initial_pos - window_size
                    window_initial_pos = section_initial_pos - window_size

                window_buffer = [ None for i in range(window_size)]

                initial_chars = f.read(window_size)

                char_position_in_text += window_size

                for i in range(len(initial_chars)):
                    char = initial_chars[i]
                    if current_context in fcm_model.state_probabilities:
                        if char in fcm_model.state_probabilities[current_context]:
                            num_bits = -math.log2( fcm_model.state_probabilities[current_context][char] )
                        else:
                            num_bits = -math.log2( 1 / different_chars_in_target)
                    else:
                        num_bits = -math.log2( fcm_model.alpha / (fcm_model.alpha*len(fcm_model.alphabet)) )
                    
                    total_num_bits += num_bits

                    window_buffer[i] = num_bits
                
                window_total_bits = 0
                for i in range(len(window_buffer)):
                    window_total_bits += window_buffer[i]

                if window_total_bits/window_size < threshold and window_initial_pos >= section_initial_pos:
                    sections_dict.append( (window_initial_pos, window_initial_pos+window_size) )

                char = f.read(1)
                char_position_in_text += 1
                window_initial_pos += 1
                while char_position_in_text <= section_final_pos:
                    
                    if current_context in fcm_model.state_probabilities:
                        if char in fcm_model.state_probabilities[current_context]:
                            num_bits = -math.log2( fcm_model.state_probabilities[current_context][char] )
                        else:
                            num_bits = -math.log2( 1 / different_chars_in_target)
                    else:
                        num_bits = -math.log2( fcm_model.alpha / (fcm_model.alpha*len(fcm_model.alphabet)) )
                        
                    total_num_bits += num_bits

                    ### Get the char position in buffer that does not belong to this new section
                    previous_char_index = (window_initial_pos + window_size - 1) % window_size

                    ### Remove the number of bits of this char to the window_total_bits
                    window_total_bits -= window_buffer[previous_char_index]

                    ### Sum the number of bits of the new char to the window_total_bits
                    window_total_bits += num_bits

                    ### Save the number of bits of the new char in the previous char position
                    window_buffer[previous_char_index] = num_bits

                    if window_total_bits/window_size < threshold and window_initial_pos >= section_initial_pos:
                        sections_dict.append( (window_initial_pos, window_initial_pos+window_size) )
                    

                    current_context = current_context[1:] + char    # Update the context
                    char = f.read(1)                        
                    char_position_in_text += 1
                    window_initial_pos += 1

            f.close()

        except OSError:
            print("Error opening file: ", target_file_name)
            sys.exit()

        
    return total_num_bits, sections_dict



            

def main(reference_file_name, target_file_name, k, alpha, multiplelangflag, target_alphabet=None, nonlangsections=None):

    if target_alphabet == None:
        ### Read Content of target file
        try:
            f = open(target_file_name, "r", encoding='utf-8-sig')

            ### Get Target Alphabet
            target_alphabet = set()

            char = f.read(1)
            while char:
                target_alphabet.add(char)
                char = f.read(1)
            f.close()

        except OSError:
            print("Error opening file: ", target_file_name)
            sys.exit()

    ### Creation of Finite Context Model from reference text
    fcm_model = Fcm(reference_file_name, k, alpha)

    ### Calculate entropy
    fcm_model.calculate_probabilities()

    bits, sections = get_number_of_bits_required_to_compress_v2(fcm_model, target_file_name, target_alphabet, k, multiplelangflag, nonlangsections)
    #bits, sections = get_number_of_bits_required_to_compress_v1(fcm_model, target_file_name, target_alphabet, multiplelangflag)
    
    return bits, sections



if __name__ == "__main__":
    ### Verify Parameters
    parser = argparse.ArgumentParser(description='Define context length and a smoothing parameter.')
    parser.add_argument('-freference', type=str, required=True, help='Path to reference file with an text example')
    parser.add_argument('-ftarget', type=str, required=True, help='Path to target file')
    parser.add_argument('-k', type=checkKValue, required=True, help='Context length')
    parser.add_argument('-a', type=checkAlphaValue, required=True, help='Desired size of the generated text')
    parser.add_argument('--multiplelang', action='store_true', required=False, default=False, help='Flag to check for multiple lang in the target text')
    args = parser.parse_args()

    reference_file_name = args.freference
    target_file_name = args.ftarget
    k = args.k
    alpha = args.a
    multiplelangflag = args.multiplelang
    
    bits, foreign_words = main(reference_file_name, target_file_name, k, alpha, multiplelangflag)
    print("Number of bits required to compress: ", round(bits, 3))
    