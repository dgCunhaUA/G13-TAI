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
#
# Note: This function is used by a second implementation of locatelang.py. Detailed explanation was written in report document.
####
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






####
# Function that calculates number of bits required to compress a target file using a finite context model from a reference file.
#   - MultipleLangFlag is used to also store the sections of chars contained in target file that are well compressed.
####
def get_number_of_bits_required_to_compress_v2(fcm_model, target_file_name, target_alphabet, window_size, multiplelangflag):

    total_num_bits = 0
    different_chars_in_target = 0

    ### Calculate the number of different chars between the two alphabets
    for char in target_alphabet:
        if char not in fcm_model.alphabet:
            different_chars_in_target += 1

    sections_dict = []

    ### Choose a random first context
    current_context = random.choice(list(fcm_model.model.keys()))

    ### Threshold value to determine if a section is well compressed or not
    threshold = math.log2(len(target_alphabet)) / 2   

    ### Read Content of target file
    try:
        f = open(target_file_name, "r", encoding='utf-8-sig')
        
        window_initial_pos = 0
        window_buffer = [ None for i in range(window_size)]     # Window buffer of size k

        initial_chars = f.read(window_size)
        for i in range(len(initial_chars)):
            char = initial_chars[i]
            if current_context in fcm_model.state_probabilities:  # If the current context exists in fcm model
                if char in fcm_model.state_probabilities[current_context]:  # If char exists in the fcm model
                    num_bits = -math.log2( fcm_model.state_probabilities[current_context][char] )
                else:       # If char doesn't exist in fcm alphabet
                    num_bits = -math.log2( 1 / different_chars_in_target)

            else:       # If the current context does not exist in fcm model
                num_bits = -math.log2( fcm_model.alpha / (fcm_model.alpha*len(fcm_model.alphabet)) )
            
            total_num_bits += num_bits

            window_buffer[i] = num_bits     # Save position and num_bits in buffer

            current_context = current_context[1:] + char    # Update the context
        
        if multiplelangflag:
            window_total_bits = 0
            ### Sum of number of bits of all chars in current sliding window
            for i in range(len(window_buffer)):
                window_total_bits += window_buffer[i]

            if window_total_bits/window_size < threshold:       # If the average value of number of bits of this section is less than the threshold
                sections_dict.append( (window_initial_pos, window_initial_pos+window_size) )

        ### For the next chars, do the same process
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

                if window_total_bits/window_size < threshold:       # If the average value of number of bits of this section is less than the threshold
                    sections_dict.append( (window_initial_pos, window_initial_pos+window_size) )
            
            current_context = current_context[1:] + char    # Update the context
            char = f.read(1)                        

        f.close()

    except OSError:
        print("Error opening file: ", target_file_name)
        sys.exit()
        
    return total_num_bits, sections_dict



####
# Function that returns the sections that are well compressed using a higher threshold.
####
def get_sections_from_remaining_sections(fcm_model, target_file_name, target_alphabet, window_size, nonlangsections):

    total_num_bits = 0
    different_chars_in_target = 0

    ### Calculate the number of different chars between the two alphabets
    for char in target_alphabet:
        if char not in fcm_model.alphabet:
            different_chars_in_target += 1

    sections_dict = []

    ### Higher Threshold value to determine if a section is well compressed or not
    threshold = (3*math.log2(len(target_alphabet))) / 4   

    ### Read Content of target file
    try:
        f = open(target_file_name, "r", encoding='utf-8-sig')
        
        for section in nonlangsections:
            section_initial_pos = section[0]    # Get section initial position
            section_final_pos = section[1]      # Get section final position

            window_initial_pos = section_initial_pos        # Sliding window inital position
            window_final_pos = section_initial_pos     # Current char position in text

            if section_initial_pos - window_size < 0:   # If there are not enough chars before this section to build a initial context
                ### Seek file to section initial position
                f.seek(section_initial_pos)   
                
                ### Choose a random first context
                current_context = random.choice(list(fcm_model.model.keys()))
            else:
                ### Seek file to section inital position - window_size in order to read the first context of size window_size
                f.seek(section_initial_pos - window_size)

                ### Read the first context
                current_context = f.read(window_size)

            window_buffer = [ None for i in range(window_size)]     # Initialize buffer of size k
            
            initial_chars = f.read(window_size)         # Read section's first chars

            window_final_pos += window_size        # Increment the window_final_pos by window_size because we read the initial chars in the previous line

            for i in range(len(initial_chars)):
                char = initial_chars[i]
                if current_context in fcm_model.state_probabilities:    # If the current context exists in fcm model
                    if char in fcm_model.state_probabilities[current_context]:      # If the char exists in fcm model
                        num_bits = -math.log2( fcm_model.state_probabilities[current_context][char] )
                    else:       # If char doesn't exist in fcm alphabet
                        num_bits = -math.log2( 1 / different_chars_in_target)

                else:   # If the current context does not exist in fcm model
                    num_bits = -math.log2( fcm_model.alpha / (fcm_model.alpha*len(fcm_model.alphabet)) )
                
                total_num_bits += num_bits

                window_buffer[i] = num_bits     # Save position and num_bits in buffer
                current_context = current_context[1:] + char    # Update the context
            

            ### Sum of number of bits of all chars in current sliding window
            window_total_bits = 0
            for i in range(len(window_buffer)):
                window_total_bits += window_buffer[i]

            ### If the average value of the current sliding value is less than the threshold
            if window_total_bits/window_size < threshold:
                sections_dict.append( (window_initial_pos, window_final_pos) )

            char = f.read(1)
            window_final_pos += 1
            window_initial_pos += 1
            ### Analyse next chars until we reach the end of the section
            while window_final_pos <= section_final_pos:
                
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

                if window_total_bits/window_size < threshold:       # If the average value of number of bits of this section is less than the threshold
                    sections_dict.append( (window_initial_pos, window_final_pos) )
            

                current_context = current_context[1:] + char    # Update the context
                char = f.read(1)                        
                window_final_pos += 1
                window_initial_pos += 1

        f.close()

    except OSError:
        print("Error opening file: ", target_file_name)
        sys.exit()

    return total_num_bits, sections_dict





####
# Function that calculates number of bits required to compress a target file using multiple finite context models from a reference file.
####
def get_number_of_bits_required_to_compress_multiplemodel(first_fcm_model, second_fcm_model, target_file_name, target_alphabet):

    total_num_bits = 0
    percentage_first_model = 0.5
    percentage_second_model = 0.5
    different_chars_in_target = 0

    ### Calculate the number of different chars between the two alphabets (Since both models are created from same file, the value will be the same in both models.)
    for char in target_alphabet:
        if char not in first_fcm_model.alphabet:
            different_chars_in_target += 1

    ### Choose a random first context from second_fcm_model since it requires a bigger context (k=4)
    current_context_first_model = random.choice(list(first_fcm_model.model.keys()))  
    current_context_second_model = random.choice(list(second_fcm_model.model.keys()))  


    ### Read Content of target file
    try:
        f = open(target_file_name, "r", encoding='utf-8-sig')

        char = f.read(1)
        while char:

            ### Calculate required bits with first model
            if current_context_first_model in first_fcm_model.state_probabilities:
                if char in first_fcm_model.state_probabilities[current_context_first_model]:
                    num_bits_first_model = -math.log2( first_fcm_model.state_probabilities[current_context_first_model][char] )
                else:
                    num_bits_first_model = -math.log2( 1 / different_chars_in_target)
            else:
                num_bits_first_model = -math.log2( first_fcm_model.alpha / (first_fcm_model.alpha*len(first_fcm_model.alphabet)) )

            ### Calculate required bits with second model
            if current_context_second_model in second_fcm_model.state_probabilities:
                if char in second_fcm_model.state_probabilities[current_context_second_model]:
                    num_bits_second_model = -math.log2( second_fcm_model.state_probabilities[current_context_second_model][char] )
                else:
                    num_bits_second_model = -math.log2( 1 / different_chars_in_target)
            else:
                num_bits_second_model = -math.log2( second_fcm_model.alpha / (second_fcm_model.alpha*len(second_fcm_model.alphabet)) )
            
            total_num_bits += (percentage_first_model*num_bits_first_model) + (percentage_second_model*num_bits_second_model)


            ### Update percentage of each model
            if num_bits_first_model < num_bits_second_model and percentage_first_model <= 0.97:
                percentage_first_model += 0.02
                percentage_second_model -= 0.02
            elif num_bits_second_model < num_bits_first_model and percentage_second_model <= 0.97:
                percentage_first_model -= 0.02
                percentage_second_model += 0.02


            current_context_first_model = current_context_first_model[1:] + char        # Update the context
            current_context_second_model = current_context_second_model[1:] + char      # Update the context
            char = f.read(1)                        

        f.close()

    except OSError:
        print("Error opening file: ", target_file_name)
        sys.exit()
        
    return total_num_bits




            

def main(reference_file_name, target_file_name, k, alpha, multiplelangflag, multipleModelsFlag):

    
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

    if multipleModelsFlag:
        first_fcm_model = Fcm(reference_file_name, 2, alpha)
        first_fcm_model.calculate_probabilities()

        second_fcm_model =  Fcm(reference_file_name, 4, alpha)
        second_fcm_model.calculate_probabilities()
                
        bits = get_number_of_bits_required_to_compress_multiplemodel(first_fcm_model, second_fcm_model, target_file_name, target_alphabet)
        
        return bits
    else:
        ### Creation of Finite Context Model from reference text
        fcm_model = Fcm(reference_file_name, k, alpha)

        ### Calculate entropy
        fcm_model.calculate_probabilities()

        bits, sections = get_number_of_bits_required_to_compress_v2(fcm_model, target_file_name, target_alphabet, k, multiplelangflag)
    
        return bits, sections



if __name__ == "__main__":
    ### Verify Parameters
    parser = argparse.ArgumentParser(description='Define context length and a smoothing parameter.')
    parser.add_argument('-freference', type=str, required=True, help='Path to reference file with an text example')
    parser.add_argument('-ftarget', type=str, required=True, help='Path to target file')
    parser.add_argument('-k', type=checkKValue, required=True, help='Context length')
    parser.add_argument('-a', type=checkAlphaValue, required=True, help='Desired size of the generated text')
    parser.add_argument('--multiplelang', action='store_true', required=False, default=False, help='Flag to check for multiple lang in the target text')
    parser.add_argument('--multiplemodels', action='store_true', required=False, default=False, help='Flag to use multiple fcmodels to predict language for target text')

    args = parser.parse_args()

    reference_file_name = args.freference
    target_file_name = args.ftarget
    k = args.k
    alpha = args.a
    multiplelangflag = args.multiplelang
    multipleModelsFlag = args.multiplemodels

    if multipleModelsFlag:
        bits = main(reference_file_name, target_file_name, k, alpha, multiplelangflag, multipleModelsFlag)
    else:
        bits, foreign_words = main(reference_file_name, target_file_name, k, alpha, multiplelangflag, multipleModelsFlag)
    print("Number of bits required to compress: ", round(bits, 3))
    