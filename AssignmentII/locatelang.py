#!/usr/bin/python

import argparse
import lang
import copy     

def checkAlphaValue(a):
    ### Function to ensure alpha is between 0 and 1
    a = float(a)
    if a > 1 or a <= 0:
        raise argparse.ArgumentTypeError("Alpha must be a value within ]0,1]")
    return a



def main():

    ### Verify Parameters
    parser = argparse.ArgumentParser(description='Define context length and a smoothing parameter.')
    #parser.add_argument('-freference', type=str, required=True, help='Path to reference file with an text example')
    parser.add_argument('-ftarget', type=str, required=True, help='Path to target file')
    parser.add_argument('-k', type=int, required=True, help='Context length')
    parser.add_argument('-a', type=checkAlphaValue, required=True, help='Desired size of the generated text')
    args = parser.parse_args()

    #reference_file_name = args.freference
    target_file_name = args.ftarget
    reference_file_dict = dict({"ENG": "example/example.txt", "PT": "example/lusiadas.txt"})    
    k = args.k
    alpha = args.a

    #words_dict = dict({})
    languages_dict = dict({})
    for language in reference_file_dict:
        #num_bits, words = lang.main(reference_file_dict[language], target_file_name, k, alpha, True)
        #words_dict[language] = [words, num_bits]

        num_bits, symbols = lang.main(reference_file_dict[language], target_file_name, k, alpha, True)
        languages_dict[language] = [symbols, num_bits]


    #mainLanguage = None
    #for language in languages_dict:
    #    if mainLanguage == None or languages_dict[mainLanguage][1] > languages_dict[language][1]:
    #        mainLanguage = language


    languages_dict = {k: v for k, v in sorted(languages_dict.items(), key=lambda item: item[1][1] )}
    mainLanguage = list(languages_dict.keys())[0]
    target_file_size =  len(languages_dict[mainLanguage][0])
    section_dict = dict({})

    print(languages_dict[mainLanguage])

    for i in range(0, target_file_size, 8):
        bestLanguage = (None, None)

        for language in languages_dict:
            num_bits = 0
            for l in range(i, i+8):
                if l < target_file_size:
                    num_bits = languages_dict[language][0][l]
            if bestLanguage[1] == None or bestLanguage[1] > num_bits:
                bestLanguage = (language, num_bits)
        
        section_dict[i] = bestLanguage[0]

    print(section_dict)

    #for k, v in copy.deepcopy(section_dict).items():
    positions_list = list(section_dict.keys())
    positions_to_remove = []

    for i in range(len(positions_list)-1):

        if (section_dict[positions_list[i]] == section_dict[positions_list[i+1]]):
            positions_to_remove.append(positions_list[i+1])

    for position in positions_to_remove:
        del section_dict[position]
            
    print(section_dict)
    
    return section_dict
    


if __name__ == "__main__":
    main()
    