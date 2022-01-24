import subprocess
import os
import sys
import argparse

####
# Argument Verification Function
####

def checkStartValue(a):
    ### Function to ensure start value is valid
    try:
        a = int(a)
    except:
        raise argparse.ArgumentTypeError("Start must be an Integer")
   
    if a < 8:
        raise argparse.ArgumentTypeError("Start value must be greater or equal than 8")
    return a

def checkDurationValue(a):
    ### Function to ensure duration value is valid
    try:
        a = int(a)
    except:
        raise argparse.ArgumentTypeError("Duration must be an Integer")
   
    if a < 8:
        raise argparse.ArgumentTypeError("Duration value must be greater or equal than 8")
    return a

def checkNoiseValue(a):
    ### Function to ensure noise value is valid
    try:
        a = float(a)
    except:
        raise argparse.ArgumentTypeError("Duration must be a float")

    if a < 0 or a > 1:
        raise argparse.ArgumentTypeError("Noise volume value must be in the interval [0, 1]")
    return a

def checkTypeValue(a):
    ### Function to ensure noise type is valid
    valid_noise_types = ["whitenoise", "pinknoise", "brownnoise"]
    if a not in valid_noise_types:
        print("ERROR: {} noise type is not supported. Supported types: [whitenoise, pinknoise, brownnoise]".format(a))
        raise argparse.ArgumentError("{} noise type is not supported.".format(a))
    return a

####
# End of Argument Verification Function
####



def main(ftarget, start, duration, noise, noisetype):
    
    database_dir_path = "./database/"
    sample_dir_path = "./samples/"

    ### Verify that the file provided is a valid music in the database
    if os.path.isfile(database_dir_path+ftarget+".wav") == False:
        print("Error! Target file {} was not found in database.".format(ftarget))
        sys.exit()

    run_sox = subprocess.run([
            "sox",                                      
            database_dir_path + ftarget + ".wav",
            sample_dir_path + ftarget + ".wav",
            "trim",
            str(start),
            str(duration)
            ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)

    run_sox_returncode = run_sox.returncode

    if noise > 0:
        run_sox_returncode = subprocess.call(
            "sox "+
            "\"" + sample_dir_path + ftarget + ".wav" + "\"" +
            " -p synth "+ noisetype + " vol " + str(noise) + " | " +
            "sox -m " +
            "\"" + sample_dir_path + ftarget + ".wav" + "\"" +
            " - " +
            "\"" + sample_dir_path + ftarget + " Noise.wav" + "\"",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)

        os.remove(sample_dir_path + ftarget + ".wav")
    
    if run_sox_returncode == 0:
        print("New sample created sucessfully.")
        if noise > 0:
            print("New sample file: {}".format("\""+sample_dir_path+ftarget+" Noise.wav\""))
        else:
            print("New sample file: {}".format("\""+sample_dir_path+ftarget+".wav\""))
    else:
        print("ERROR: An error occured while creating new sample.")

if __name__ == "__main__":
    ### Verify Parameters
    parser = argparse.ArgumentParser(description="Define context length and a smoothing parameter.")
    parser.add_argument("-ftarget", type=str, required=True, help="Target music file name")
    parser.add_argument('-start', type=checkStartValue, required=False, default=0, help="Select new sample start second")
    parser.add_argument('-duration', type=checkDurationValue, required=False, default=20, help="Select new sample duration")
    parser.add_argument('-noise', type=checkNoiseValue, required=False, default=0, help="Select new sample noise volume")
    parser.add_argument('-type', type=checkTypeValue, required=False, default="whitenoise", help="Select new sample noise type")


    args = parser.parse_args()

    ftarget = args.ftarget
    start = args.start
    duration = args.duration
    noise = args.noise
    noisetype = args.type

    main(ftarget, start, duration, noise, noisetype)


