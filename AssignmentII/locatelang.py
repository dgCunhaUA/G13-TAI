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
    
    words_dict = dict({})
    for language in reference_file_dict:
        num_bits, words = lang.main(reference_file_dict[language], target_file_name, k, alpha, True)
        words_dict[language] = [words, num_bits]

        print("\nLanguage: ", language)
        print("Dictionary: ", words_dict[language])

    ### Sort the dicitonary by number of bits
    words_dict = {k: v for k, v in sorted(words_dict.items(), key=lambda item: item[1][1] )}


    ### Merge step
    merged_words_dict = {}
    for language in words_dict:     # For each language
        words = words_dict[language][0]     # Get the words of this language
        for word in words:     # For each word
            position_in_text = word[1]
            num_bits = words[word]
            if position_in_text in merged_words_dict:      # If the word is already in the merged dictionary
                assigned_language = merged_words_dict[position_in_text]     # Get the language that the word has at the moment
                if num_bits < words_dict[ assigned_language ][0][word]:     # If the new language compresses the word with less bits
                    merged_words_dict[position_in_text] = language          # Save the language that compresses with less bits
            else:
                merged_words_dict[position_in_text] = language   # Add the word to dictionary and save Ex: 4: ("ENG", 3.424)
    
    ### Sort the final dictionary by positions in text (keys)
    merged_words_dict = {k: v for k, v in sorted(merged_words_dict.items(), key=lambda item: item[0] )}

    print("\nMerged Dictionary: ", merged_words_dict, "\n")

    ### "truncate" the merged dict. Remove positions that have the same language of their last "neighbour"
    positions_in_text_list = list(merged_words_dict.keys())    # List of the merged dict keys
    positions_to_remove = []
    for i in range(len(positions_in_text_list)-1):
        if (merged_words_dict[positions_in_text_list[i]] == merged_words_dict[positions_in_text_list[i+1]]):
            positions_to_remove.append(positions_in_text_list[i+1])

    for position in positions_to_remove:
        del merged_words_dict[position]


    print("Target file name: ", target_file_name)
    print("Language Sections: ", merged_words_dict)
    return words_dict
    


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
    