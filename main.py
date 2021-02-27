from __future__ import unicode_literals
import youtube_dl
import math
import contextlib
import wave
import speech_recognition as sr


def main():
    url = "https://www.youtube.com/watch?v=Sm3Wye6uKXQ&t=23s"
    response, vid_id = download_youtube_as_mp3(url)
    make_transcript(response, vid_id)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_youtube_as_mp3(url):
    ydl_opts = get_ydl_opts()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        video_title = video_title.replace(":", "-")
        video_title = video_title.replace("**", "_")
        video_id = info_dict.get("id", None)
        return video_title, video_id


def get_ydl_opts():
    ydl_opts = {
        'format': 'bestaudio/best',
        # 'outtmpl': './audio_output/%(title)s.%(ext)s',
        'outtmpl': './audio_output/1.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'progress_hooks': [my_hook],
    }
    return ydl_opts


def make_transcript(title, vid_id):
    fp = "./audio_output/1.wav"

    duration = get_duration(fp)
    total_duration = math.ceil(duration / 60)

    r = sr.Recognizer()
    f = open(f"./transcript/{title}.txt", "a")
    f.write("Title: " + title + "\n")
    f.write("ID: " + vid_id + "\n")
    f.write("Transcript:\n")
    for i in range(0, total_duration):
        with sr.AudioFile(fp) as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source, offset=i * 60, duration=60)
        
        f.write(r.recognize_google(audio))
        f.write(" ")
    f.close()


def get_duration(file_path):
    with contextlib.closing(wave.open(file_path, "r")) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


main()
