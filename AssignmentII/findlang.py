#!/usr/bin/python

import argparse
import lang


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



def main(target_file_name, k, alpha):

    reference_file_dict = dict({"AFG": "example/AFG/afghanistan-medium.utf8",
                                "AFR": "example/AFR/afrikaans-big.utf8",
                                "ARA": "example/ARA/arabic-big.utf8",
                                "BUL": "example/BUL/bulgarian-big.utf8",
                                "CRO": "example/CRO/croatian-big.utf8",
                                "DEN": "example/DEN/danish-big.utf8",
                                "ENG": "example/ENG/gb_english.utf8",
                                "SPA": "example/ESP/spanish-big.utf8",
                                "FIN": "example/FIN/finnish-big.utf8",
                                "FRA": "example/FRA/french-big.utf8",
                                "GER": "example/GER/german-big.utf8",
                                "GRE": "example/GRE/greek-big.utf8",
                                "HUN": "example/HUN/hungarian-big.utf8",
                                "ICE": "example/ICE/icelandic-big.utf8",
                                "ITA": "example/ITA/italian-big.utf8",
                                "POL": "example/POL/polish-big.utf8",
                                "POR": "example/POR/portuguese-big.utf8",
                                "RUS": "example/RUS/russian-big.utf8",
                                "UKR": "example/UKR/ukrainian-big.utf8"
                                })    

    print("Searching for the best language...")
    best_choice = (None, None)
    for language in reference_file_dict:
        num_bits, words = lang.main(reference_file_dict[language], target_file_name, k, alpha, False)
        
        if best_choice[1] == None or best_choice[1] > num_bits:
            best_choice = (language, num_bits)
            
    print("Target file name: ", target_file_name)
    print("Predicted Language: ", best_choice[0])

if __name__ == "__main__":
    ### Verify Parameters
    parser = argparse.ArgumentParser(description='Define context length and a smoothing parameter.')
    parser.add_argument('-ftarget', type=str, required=True, help='Path to target file')
    parser.add_argument('-k', type=checkKValue, required=True, help='Context length')
    parser.add_argument('-a', type=checkAlphaValue, required=True, help='Desired size of the generated text')
    args = parser.parse_args()

    target_file_name = args.ftarget
    k = args.k
    alpha = args.a

    main(target_file_name, k, alpha)
    