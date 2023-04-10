from pytube import YouTube

yt_url = "https://www.youtube.com/watch?v=IvKsQewxcIU"

yt = YouTube(yt_url)
itag = yt.streams.filter(only_audio=True)[0].itag
stream = yt.streams.get_by_itag(itag)
stream.download()