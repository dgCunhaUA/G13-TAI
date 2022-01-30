import subprocess
import os

def main(files_origin, files_destiny):

    list_to_process = [f for f in os.listdir(files_origin) if os.path.isfile(os.path.join(files_origin, f))]
    list_to_process_size = len(list_to_process)
    available_formats = [".wav", ".flac", ".mp3", ".mp4"]

    ### Ouput initial feedback message
    print("New Musics found in {}: {}".format(files_origin, list_to_process_size))
    print("Preprocessing each music... 0/{}".format(list_to_process_size))

    musics_processed = 0
    for f in list_to_process:
        filename, format = os.path.splitext(f)

        ### Verify if file belongs to supported formats
        if format not in available_formats:
            list_to_process.remove(f)
            musics_processed+=1
            print("Format {} is not supported. File was removed.".format(format))
            os.remove(files_origin + f)
            continue

        ### Convert files to .wav
        if format == ".mp3" or format == ".mp4" or format == ".flac":
            run_ffmpeg = subprocess.run([
                "ffmpeg",
                "-i",
                files_origin + f,
                files_origin + filename + ".wav"
                ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)

            if run_ffmpeg.returncode != 0:
                print("ERROR: Could not convert {} file to .wav.".format(f))

        ### Use sox to change sample rate of files to 44100Hz
        run_sox = subprocess.run([
                "sox",                                      
                files_origin + filename + ".wav",
                "-G",
                "-r 44100",
                "-b 16",
                files_destiny + filename + ".wav"
                ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)

        if run_sox.returncode != 0:
            print("ERROR: Could not convert {} file to 44100hz".format(f))

        ### Remove files from origin folder
        if format == ".mp3":
            os.remove(files_origin + filename + ".mp3")
        elif format == ".mp4":
            os.remove(files_origin + filename + ".mp4")
        elif format == ".flac":
            os.remove(files_origin + filename + ".flac")
        os.remove(files_origin + filename + ".wav")

        ### Output update feedback message
        musics_processed+=1
        print("Preprocessing each music... {}/{}".format(musics_processed, list_to_process_size))

    print("Prepocessing ended sucessfully.")


if __name__ == "__main__":
    main("./newMusics/", "./database/")
    main("./newVideos/", "./videoToSample/")
