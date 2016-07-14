# House Points Slackbot

This amazing bot will let everyone on your slack team award points to different House. Our code of honor is

  - No awarding points to your own house
  - Cheating will be punished with great wrath and greater whimsy

To set it up, just insert your slack API token, the channel you'd like to listen on, pip install the requirements, and run `python main.py` on some server somewhere. Hackathon style!


![Bot in action][slack]


[slack]: https://files.slack.com/files-pri/T029GG40X-F0Q6DDGN7/pasted_image_at_2016_03_03_01_48_pm.png?pub_secret=83fd31bc54

### Setup
Getting your slack API token

* Create a slack bot via the instructions in https://api.slack.com/bot-usersour
* After creating the bot, look at your bot via the inspect button
* You should see a field called API token
* Paste it into consts.py

Getting your chat channel token

If you are posting to a public channel, it'll be in the API documentation, under channels.list
I'm lazy, so I look using https://api.slack.com/methods/channels.list/test

If it's private, it'll be under groups.list
I'm lazy, so I look using https://api.slack.com/methods/groups.list/test