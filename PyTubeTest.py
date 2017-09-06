from pytube import YouTube
yt = YouTube("https://www.youtube.com/watch?v=MmlMF5p_ZMY")
print(yt.get_videos())
yt.set_filename('smashvid2')
video = yt.get('mp4','720p')
video.download('')