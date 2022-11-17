import csv
import pathlib

class Export:
    def __init__(self, channel):
        self.channel = channel

    def export_to_csv(self):
        name = self.channel.username + ".csv"
        path = pathlib.Path().resolve().absolute() / 'export' / name
        with open(path,'w', encoding='UTF-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Channel', 'Subscribers'])
            writer.writerow([self.channel.username, self.channel.channel_data['statistics']['subscriberCount']])
            writer.writerow(['Video title', 'id', 'View count'])
            for video in self.channel.videos:
                writer.writerow([video['snippet']['title'],video['id'],video['statistics']['viewCount']])