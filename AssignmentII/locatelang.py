#!/usr/bin/python

import argparse
from typing import Final
import lang
import sys


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



def truncate_and_merge_sections(sections_dict, sections, language):
    merged_sections = []
    if len(sections) > 1:
        initial_section = sections[0]           # Get the first section
        merged_section = initial_section[0]     # Merged section initialized only with the starting value
        for i in range(1, len(sections)):       # For the next sections
            previous_section = sections[i-1]    # Get the previous section
            current_section = sections[i]       # Get the section

            if previous_section[1] < current_section[0] - 1:    # For example: (3, 9) (11, 17) = If 9 < 11 - 1 it means that this section has ended and is not continuos anymore 
                merged_section = (merged_section, previous_section[1])    # Create final merged section (starting, end). For example (3, 9)
                merged_sections.append(merged_section)
                merged_section = current_section[0]      # Assign the current section starting position to final_section
        
        merged_section = (merged_section, current_section[1])    # Final merged section is assigned with the end-value of the last section end-value
        merged_sections.append(merged_section)

    for section in merged_sections:
        if section in sections_dict:
            sections_dict[section].append( language )
        else:
            sections_dict[section] = [language]

    return sections_dict




def main(target_file_name, k, alpha):


    reference_file_dict = dict({"AFG": "example/AFG/afghanistan-medium.utf8",
                                "AFR": "example/AFR/afrikaans-small.utf8",
                                "ARA": "example/ARA/arabic-small.utf8",
                                "BUL": "example/BUL/bulgarian-medium.utf8",
                                "CRO": "example/CRO/croatian-medium.utf8",
                                "DEN": "example/DEN/danish-medium.utf8",
                                "ENG": "example/ENG/gb_english.utf8",
                                "SPA": "example/ESP/spanish-medium.utf8",
                                "FIN": "example/FIN/finnish-medium.utf8",
                                "FRA": "example/FRA/french-medium.utf8",
                                "GER": "example/GER/german-medium.utf8",
                                "GRE": "example/GRE/greek-medium.utf8",
                                "HUN": "example/HUN/hungarian-medium.utf8",
                                "ICE": "example/ICE/icelandic-medium.utf8",
                                "ITA": "example/ITA/italian-medium.utf8",
                                "POL": "example/POL/polish-medium.utf8",
                                "POR": "example/POR/portuguese-medium.txt",
                                "RUS": "example/RUS/russian-medium.utf8",
                                "UKR": "example/UKR/ukrainian-medium.utf8"
                                })  
    
    ### Read Content of target file
    try:
        f = open(target_file_name, "r", encoding='utf-8-sig')

        ### Get Target Alphabet
        target_alphabet = set()
        target_file_length = 0
        char = f.read(1)
        while char:
            target_file_length += 1
            target_alphabet.add(char)
            char = f.read(1)
        f.close()

    except OSError:
        print("Error opening file: ", target_file_name)
        sys.exit()


    sections_dict = dict({})
    for language in reference_file_dict:
        num_bits, sections = lang.main(reference_file_dict[language], target_file_name, k, alpha, True, target_alphabet, None)
        sections_dict = truncate_and_merge_sections(sections_dict, sections, language)

    ### Sort the dicitonary by number of bits
    sections_dict = {k: v for k, v in sorted(sections_dict.items(), key=lambda item: item[0][0] )}

    remainder_sections = []
    for i in range(target_file_length):
        valid = True
        for section in sections_dict:
            if section[0] == i:
                valid = False
            elif section[0] < i and section[1] >= i :
                valid = False
        if valid:
            remainder_sections.append( i )

    final_remainder_sections = []
    initial_pos = 0
    for i in range(len(remainder_sections) - 1):
        if remainder_sections[i] + 1 != remainder_sections[i+1]:
            if remainder_sections[i] - initial_pos > 5:
                final_remainder_sections.append( (initial_pos, remainder_sections[i]) )
            initial_pos = remainder_sections[i + 1]

    if remainder_sections[-1] - initial_pos > 5:
        final_remainder_sections.append( (initial_pos, remainder_sections[-1]) )
    final_remainder_sections = [(0, 6), (41, 55), (68, 76), (84, 90), (96, 109), (145, 156), (225, 232)]
    print(final_remainder_sections)
    
    print("Upgrading Threshold")
    for language in reference_file_dict:
        num_bits, sections = lang.main(reference_file_dict[language], target_file_name, k, alpha, True, target_alphabet, final_remainder_sections)
        sections_dict = truncate_and_merge_sections(sections_dict, sections, language)


    ### Sort the dicitonary by number of bits
    sections_dict = {k: v for k, v in sorted(sections_dict.items(), key=lambda item: item[0][0] )}

    for item in sections_dict.items():
        print("Posições: ", item[0], end="")
        print(", Language: ", item[1])



    """
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

    #print("\nMerged Dictionary: ", merged_words_dict, "\n")

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
    """


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
    