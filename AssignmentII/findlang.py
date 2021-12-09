#!/usr/bin/python

import argparse
import lang


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
    reference_file_dict = dict({"example/example.txt": "ENG", "example/small.txt":"ENG", "example/lusiadas.txt":"PT"})    
    k = args.k
    alpha = args.a

    best_choice = (None, None)
    for reference_file in reference_file_dict:
        num_bits, foreign_words = lang.main(reference_file, target_file_name, k, alpha, False)
        
        if best_choice[1] == None or best_choice[1] > num_bits:
            best_choice = (reference_file, num_bits)
    
    print("Target file name: ", target_file_name)
    print("Predicted Language: ", reference_file_dict[best_choice[0]])

if __name__ == "__main__":
    main()
    