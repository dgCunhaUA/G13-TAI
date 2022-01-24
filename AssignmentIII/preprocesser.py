import subprocess
import os

def main():

    database_path = "./database/"
    new_musics_path = "./newMusics/"
    new_musics_list = [f for f in os.listdir("newMusics/") if os.path.isfile(os.path.join("newMusics/", f))]
    new_music_size = len(new_musics_list)
    available_formats = [".wav", ".flac", ".mp3", ".mp4"]

    ### Ouput initial feedback message
    print("New Musics found: ", new_music_size)
    print("Preprocessing each music... 0/{}".format(new_music_size))

    musics_processed = 0
    for f in new_musics_list:
        filename, format = os.path.splitext(f)

        ### Verify if file belongs to supported formats
        if format not in available_formats:
            new_musics_list.remove(f)
            musics_processed+=1
            print("Format {} is not supported. File was removed.".format(format))
            os.remove(new_musics_path + f)
            continue

        ### Convert files to .wav
        if format == ".mp3" or format == ".mp4" or format == ".flac":
            run_ffmpeg = subprocess.run([
                "ffmpeg",
                "-i",
                new_musics_path + f,
                new_musics_path + filename + ".wav"
                ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)

            if run_ffmpeg.returncode != 0:
                print("ERROR: Could not convert {} file to .wav.".format(f))


        ### Use sox to change sample rate of files to 44100Hz
        run_sox = subprocess.run([
                "sox",                                      ### VER SOX REQUIREMENTS
                new_musics_path + filename + ".wav",
                "-G",
                "-r 44100",
                "-b 16",
                database_path + filename + ".wav"
                ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)

        if run_sox.returncode != 0:
            print("ERROR: Could not convert {} file to 44100hz".format(f))

        ### Remove files from newMusics folder
        if format == ".mp3":
            os.remove(new_musics_path + filename + ".mp3")
        elif format == ".mp4":
            os.remove(new_musics_path + filename + ".mp4")
        elif format == ".flac":
            os.remove(new_musics_path + filename + ".flac")
        os.remove(new_musics_path + filename + ".wav")

        ### Output update feedback message
        musics_processed+=1
        print("Preprocessing each music... {}/{}".format(musics_processed, new_music_size))

    print("Prepocessing ended sucessfully.")


if __name__ == "__main__":
    main()
