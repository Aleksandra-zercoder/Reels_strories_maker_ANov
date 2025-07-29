from moviepy.editor import AudioFileClip

def prepare_audio(audio_path, video_duration):
    audio = AudioFileClip(audio_path)

    if audio.duration >= video_duration:
        audio = audio.subclip(0, video_duration)
    else:
        loops = int(video_duration // audio.duration) + 1
        audio = audio.fx(lambda a: a.loop(loops)).subclip(0, video_duration)

    return audio
