import pathlib

from channel import Channel
from export import Export

usernames = ['svt']

for username in usernames:
    channel = Channel(username)
    channel.fetch_channel()
    if channel.channel_exist:
        export = Export(channel)
        export.export_to_csv()