from pytube import YouTube
yt = YouTube("https://www.youtube.com/watch?v=PL8MnD5KBMI")
print(yt.get_videos())
yt.set_filename('smashvid')
video = yt.get('mp4','720p')
video.download('')