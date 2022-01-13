import subprocess
from os import listdir
from os.path import isfile, join
import argparse
from tkinter.messagebox import NO


def getMaxFreqs(filepath, filename):
    run_get_max_freqs = subprocess.run(
        [
            "getmax/bin/GetMaxFreqs",
            "-w",
            "freqs/" + filename[:-4] + ".freqs",
            filepath + filename,
        ]
    )
    return run_get_max_freqs.returncode, filename[:-4] + ".freqs"


def main(ftarget):
    musics_basedir_path = "musics/"
    musics_list = [
        f for f in listdir(musics_basedir_path) if isfile(join(musics_basedir_path, f))
    ]
    print(musics_list)

    music_samples = {}
    for music_filename in musics_list:

        code, music_sample = getMaxFreqs(musics_basedir_path, music_filename)
        if code == 0:
            music_samples[music_filename] = music_sample

    code, target_sample = getMaxFreqs("/samples", ftarget)

    print(music_samples)


if __name__ == "__main__":
    ### Verify Parameters
    parser = argparse.ArgumentParser(
        description="Define context length and a smoothing parameter."
    )
    parser.add_argument(
        "-ftarget", type=str, required=True, help="Target music file name"
    )
    args = parser.parse_args()

    ftarget = args.ftarget

    main(ftarget)
