import subprocess
import os
import sys
import argparse
import preprocesser
import time

### Compressors
import gzip
import lzma
import bz2
import zlib
import lz4.frame


####
# Argument Verification Functions
####

def checkCompressorValue(a):
    ### Function to ensure compressor value is valid
    valid_compressors = ["gzip", "lzma", "bz2", "bzip2", "zlib", "lz4"]             #bz2 and bzip2 are the same compressor.
    if a not in valid_compressors:
        print("ERROR: {} compressor is not supported. Supported compressors: [gzip, lzma, bz2, bzip2, zlib, lz4]".format(a))
        raise argparse.ArgumentError("{} compressor is not supported.".format(a))
    return a

def checkTopValue(a):
    ### Function to ensure top value is valid
    try:
        a = int(a)
    except:
        raise argparse.ArgumentTypeError("Start must be an Integer")

    valid_top_values = [1, 3, 5, 10]
    if a not in valid_top_values:
        print("ERROR: {} top value is not supported. Supported values: [1, 3, 5, 10]".format(a))
        raise argparse.ArgumentError("{} top value is not supported.".format(a))
    return a


####
# End of Argument Verification Functions
####




####
# getMaxFreqs Function. Creates a signature of a music file to use to calculate ncd.
####

def getMaxFreqs(new_filename, target_file, target_fileformat, filetype):

    freqs_subdir = ""
    if filetype == "music":
        freqs_subdir = "database/"
    elif filetype == "sample":
        freqs_subdir = "samples/"

    run_get_max_freqs = subprocess.run(
        [
            "getmax/bin/GetMaxFreqs",
            "-w",
            "freqs/" + freqs_subdir + new_filename + ".freqs",
            target_file + target_fileformat
        ]
    )
    return run_get_max_freqs.returncode, new_filename




####
# Function that returns the number of bytes required to compress a string with a specific compressor.
####

def getNumBitsFromCompressor(compressor, str):
    if compressor == "lzma":
        return len(lzma.compress(str)) 
    elif compressor == "bz2" or compressor == "bzip2":
        return len(bz2.compress(str)) 
    elif compressor == "zlib":
        return len(zlib.compress(str))
    elif compressor == "lz4":
        return len(lz4.frame.compress(str)) 
    else:
        return len(gzip.compress(str)) 






def main(ftarget, compressor, top):
    
    start_time = time.time()

    database_dir_path = "./database/"
    sample_dir_path = "./samples/"

    ### Verify that the file provided is a valid sample
    if os.path.isfile(sample_dir_path+ftarget+".wav") == False:
        print("Error! Target file {} was not found in samples files.".format(ftarget))
        sys.exit()
    
    ### Update database with new musics
    preprocesser.main()  

    ### Obtain the list of musics in our database
    database = [f for f in os.listdir(database_dir_path) if os.path.isfile(os.path.join(database_dir_path, f))]
    
    ### Create the .freqs file for each music in database that do not have the signature file created yet.
    for music_file in database:
        filename, format = os.path.splitext(music_file)
        if os.path.isfile("freqs/database/"+filename+".freqs") == False:
            getMaxFreqs(filename, database_dir_path+filename, ".wav", "music")

    ### Create the .freqs file for our target sample
    getMaxFreqs(ftarget, sample_dir_path+ftarget, ".wav", "sample")


    with open("freqs/samples/" + ftarget + ".freqs", "rb") as f_music:        
        sample_file_content = f_music.read()
    f_music.close()
    sample_num_bits = getNumBitsFromCompressor(compressor, sample_file_content)

    ncd_dicts = dict({})
    ### Compare our target sample to each of our musics using the respective .freqs file
    for music_file in database:
        filename, format = os.path.splitext(music_file)
        with open("freqs/database/" + filename + ".freqs", "rb") as f_music:
            music_file_content = f_music.read()
        f_music.close()
        music_num_bits = getNumBitsFromCompressor(compressor, music_file_content)

        concatenated_file_content = sample_file_content + music_file_content
        concatenated_num_bits = getNumBitsFromCompressor(compressor, concatenated_file_content)

        ncd = ( concatenated_num_bits - min([sample_num_bits, music_num_bits]) ) / max([sample_num_bits, music_num_bits])
        ncd_dicts[filename] = ncd

    ncd_dicts = {k: v for k, v in sorted(ncd_dicts.items(), key=lambda item: item[1])}
    predicted_musics = list(ncd_dicts.keys())
   
    for i in range(top):
        print("\nPrediction Number: {}\nMúsic Prediction: {}\nNCD Value: {:.5f} ".format(i+1, predicted_musics[i], ncd_dicts[predicted_musics[i]]))
    print("Execution Time: {:.3f}".format(time.time() - start_time))


if __name__ == "__main__":
    ### Verify Parameters
    parser = argparse.ArgumentParser(description="Define context length and a smoothing parameter.")
    parser.add_argument("-ftarget", type=str, required=True, help="Target music file name")
    parser.add_argument("-compressor", type=checkCompressorValue, required=False, default="gzip", help="Desired compressor name")
    parser.add_argument("-top", type=checkTopValue, required=False, default=1, help="Number of most similar musics displayed in the results.")

    args = parser.parse_args()

    ftarget = args.ftarget
    compressor = args.compressor
    top = args.top


    main(ftarget, compressor, top)


