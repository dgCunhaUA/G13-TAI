from lib2to3.pytree import convert
from os import listdir
from os.path import isfile, join
import subprocess

from pydub import AudioSegment
import os


def main(musics_list):
    database_path = "./database/"

    for f in musics_list:
        filename, format = os.path.splitext(f)

        # Convert to .wav
        if format == ".mp3":
            sound = AudioSegment.from_mp3(database_path + f)
            sound.export(database_path + filename + ".wav", format="wav")
        elif format == ".wav":
            sound = AudioSegment.from_wav(database_path + f)
            sound.export(database_path + filename + ".wav", format="wav")

        # Use sox to change sample rate of files to 44100Hz
        run_sox = subprocess.run(
            [
                "sox",
                database_path + filename + ".wav",
                "-G",
                "-r 44100",
                "-b 16",
                "./musics/" + filename + ".wav",
            ]
        )


if __name__ == "__main__":
    main([f for f in listdir("database/") if isfile(join("database/", f))])
