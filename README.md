# FeedItToMe.py
### A Discord bot that sends you messages whenever there's an update on your favorite YouTube channels, podcasts, or whatever uses a RSS feed.

All you need is a .txt file containing the name and feed URL, separated by a ";".

Example of the 'Feed.txt' file: 

          PewDiePie;https://www.youtube.com/feeds/videos.xml?channel_id=UC-lHJZR3Gqxm24_Vd_AJ5Yw;New entry

          YouTube;https://www.youtube.com/feeds/videos.xml?channel_id=UC-lHJZR3Gqxm24_Vd_AJ5YwUCBR8-60-B28hp2BmDPdntcQ;New entry
          
          ...
          
          Name;URL;Last updated entry
          
          ...

The "Last updated entry" field can be left as "New entry" for when including new channels.
          
A verification is made every 5 minutes, but you can change this on the configurations section. If there is an update, a message is sent to the specified Discord channel containing the name, date and link of the last entry.

You can add and remove entries with "!add" and "!remove";
Clear the chat with "!clear";
And check the last entry for a single feed with "!check FeedName"
