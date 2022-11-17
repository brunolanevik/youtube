from dotenv import load_dotenv, dotenv_values
import httpx
import json

load_dotenv()
config = dotenv_values(".env")
apikey = config.get('YOUTUBE_API_KEY')
base_url = "https://youtube.googleapis.com/youtube/v3/"
class Channel:
    def __init__(self, username):
        self.username = username
        self.channel_exist = False
        self.channel_data = {}
        self.uploads_playlist = ''
        self.playlist_videos = []
        self.videos = []

    def fetch_channel(self):
        username = self.username
        url = f"{base_url}channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={username}&key={apikey}"
        response = httpx.get(url).json();
        self.channel_exist = response['pageInfo']['totalResults'] > 0
        if self.channel_exist:
            self.channel_data = response['items'][0]
            self.uploads_playlist = self.channel_data['contentDetails']['relatedPlaylists']['uploads']
            self.fetch_videos_from_uploads()


    def fetch_videos_from_uploads(self):
        fetch = True
        next_page_token = ''
        while(fetch):
            response = self.fetch_videos_from_playlist(self.uploads_playlist, next_page_token)
            videos = [v['contentDetails']['videoId'] for v in response['items']]
            self.videos.extend(self.fetch_videos(videos)['items'])
            if 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
            else:
                fetch = False

    def fetch_videos_from_playlist(self,playlist_id,next_page_token = ''):
        url = f"{base_url}playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={playlist_id}&key={apikey}"
        if(len(next_page_token) > 0):
            url += f"&pageToken={next_page_token}"
        return httpx.get(url).json();

    def fetch_videos(self, videos):
        url = f"{base_url}videos?part=snippet%2CtopicDetails%2CcontentDetails%2Cstatistics"
        for video in videos:
            url += f"&id={video}"
        url += f"&key={apikey}"
        return httpx.get(url).json();