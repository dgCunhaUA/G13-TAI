#!/usr/bin/python

import argparse
import lang


####
# Argument Verification Function
####

def check_arg_value(a):
    ### Function to ensure k and alpha are greater than 0
    a = int(a)
    if a <= 0:
        raise argparse.ArgumentTypeError("k and alpha must be a integer greater than 0")
    return a


def main(target_file_name, k, alpha):

    reference_file_dict = dict({"AFG": "example/texts/afghanistan.utf8",
                                "AFR": "example/texts/afrikaans.utf8",
                                "BUL": "example/texts/bulgarian-big.utf8",
                                "CRO": "example/texts/croatian-big.utf8",
                                "FIN": "example/texts/finnish-big.utf8",
                                "FRA": "example/texts/french-big.utf8",
                                "ENG": "example/texts/gb_english.utf8",
                                "GER": "example/texts/german.utf8",
                                "HUN": "example/texts/hungarian-big.utf8",
                                "ITL": "example/texts/italian-big.utf8",
                                "POL": "example/texts/polish-big.utf8",
                                "POR": "example/texts/portuguese.utf8",
                                "RUS": "example/texts/russian-big.utf8",
                                "SPA": "example/texts/spanish-big.utf8",
                                "UKR": "example/texts/ukrainian-big.utf8"
                                })    

    print("Searching for the best language...")
    best_choice = (None, None)
    for language in reference_file_dict:
        num_bits, foreign_words = lang.main(reference_file_dict[language], target_file_name, k, alpha, False)
        
        if best_choice[1] == None or best_choice[1] > num_bits:
            best_choice = (language, num_bits)
    
    print("Target file name: ", target_file_name)
    print("Predicted Language: ", best_choice[0])

if __name__ == "__main__":
    ### Verify Parameters
    parser = argparse.ArgumentParser(description='Define context length and a smoothing parameter.')
    parser.add_argument('-ftarget', type=str, required=True, help='Path to target file')
    parser.add_argument('-k', type=check_arg_value, required=True, help='Context length')
    parser.add_argument('-a', type=check_arg_value, required=True, help='Desired size of the generated text')
    args = parser.parse_args()

    target_file_name = args.ftarget
    k = args.k
    alpha = args.a

    main(target_file_name, k, alpha)
    