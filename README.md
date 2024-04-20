# CS 152 - Trust and Safety Engineering
## Discord Bot Framework Code

This is the base framework for students to complete Milestone 2 of the CS 152 final project. Please follow the instructions you were provided to fork this repository into your own repository and make all of your additions there. 

## Discord bot setup guide

For this milestone your group will be making your very own Discord bot. Discord bots are implemented in Python (or Javascript) - don’t stress if you haven’t written Python before! It’s a pretty readable language, so you should be able to pick it up as you go, and the TAs are always here to help.

If you’re not familiar with Discord, that’s totally okay! [Check out this short video](https://www.youtube.com/watch?v=rnYGrq95ezA) which overviews Discord’s features and quirks.

### [All group members] Joining your group channels

First, every member of the team (both CS and POLISCI) should join the Discord server using this invite link: 

https://discord.gg/K4XmF7Yr

Discord can be used in your web browser, although most people prefer the [thick client apps.](https://discord.com/download)

For the next two milestones, you and your group will have two channels to test and develop your bot in: group-#, and group-#-mod, where # is your group’s number. We will give you and your bot a special role such that only you and the staff can see those channels; that way, everyone will have their own small workspace. 

To get the role for your group, click on the TA Bot user to bring up this window. 
Type in: .join # where # is replaced by your group number. 


![Screenshot 2024-04-20 at 3 20 44 PM](https://github.com/stanfordio/cs152bots/assets/35933488/50ea58fd-158c-4552-9bd9-e2d7772beea2)


If all goes according to plan, you should receive a message back saying that you have been given a role corresponding to your group number and you should see a new role on your user in the server:


![Screenshot 2024-04-20 at 3 21 11 PM](https://github.com/stanfordio/cs152bots/assets/35933488/93af3f0b-4589-40ff-a4e0-bac25f66d0b7)


Additionally, you should be able to see two new channels under one of the “Group Channels” categories:


![Screenshot 2024-04-20 at 3 21 44 PM](https://github.com/stanfordio/cs152bots/assets/35933488/8c534b72-06d6-43d6-b853-3e52e67f9a58)

If you accidentally join the wrong group, just message the TA Bot ```.leave #``` to have the role removed and leave those channels. 

#### Please let Anthony Mensah know if something goes awry in this process! 

### [One student per group] Setting up your bot

##### Note: only ONE student per group should follow the rest of these steps.

#### Download files

Fork and clone the GitHub repository [here](https://github.com/stanfordio/cs152bots). For instructions on how to fork a github repo, [see this article](https://docs.github.com/en/get-started/quickstart/fork-a-repo). In order for your group to be able to collaborate effectively on this project, we recommend you create a shared GitHub repository; when you do, make sure you use the .gitignore file included in the starter code so that you don’t accidentally upload your tokens to GitHub. Our GitHub repository already has tokens.json in its .gitignore file. When you clone your project from there, you will have to create your own tokens.json file in the same folder as your bot.py file. The tokens.json file should look like this, replacing the “your key here” with your key. In the below sections, we explain how to obtain Discord keys.
```
{
	"discord": "your key here"
}
```

#### Making the bot

The first thing you’ll want to do is make the bot. To do that, log in to https://discord.com/developers and click “New Application” in the top right corner. 

![Screenshot 2024-04-20 at 3 33 56 PM](https://github.com/stanfordio/cs152bots/assets/35933488/6e4e166e-b1c3-44f0-86d1-1c1019b8ad7a)


Name your application <mark> Group # Bot </mark>, where # is replaced with your group number. So, for instance, Group 0 would name their bot like so: 


![Screenshot 2024-04-20 at 3 35 38 PM](https://github.com/stanfordio/cs152bots/assets/35933488/59ab135e-a3e0-4e58-a7dc-046cf722fdf4)

##### It is very important that you name your bot exactly following this scheme; some parts of the bot’s code rely on this format.


1. Next, you’ll want to click on the tab labeled “Bot” under “Settings.”
2. Click “Copy” to copy the bot’s token. If you don’t see “Copy”, hit “Reset Token” and copy the token that appears (make sure you’re the first team member to go through these steps!)
3. Open tokens.json and paste the token between the quotes on the line labeled “discord”.
4. Scroll down to a region called “Privileged Gateway Intents”
5. Tick the options for “Presence Intent”, “Server Members Intent”, and “Message Content Intent”, and save your changes. See the image for what it should look like.


![Screenshot 2024-04-20 at 3 37 35 PM](https://github.com/stanfordio/cs152bots/assets/35933488/1d327d46-c325-4404-830e-0ae0be288e8d)


An aside: It’s unsafe to embed API keys in your code directly. If you put that code on GitHub, then anyone could find and use that key! (GitHub actually tries to detect code like this and forbids programmers from uploading it.) That’s why we’re storing them in a separate file which can be ignored by version control software.

Next, we’ll add the bot to the 152 Discord server! You’ll need to generate a link that the teaching team can use to invite your bot.



1. Click on the tab labeled “OAuth2” under “Settings”
2. Click the tab labeled “URL Generator” under “OAuth2”.
3. Check the box labeled “bot”. Once you do that, another area with a bunch of options should appear lower down on the page.
4. Check these permissions, then copy the link that’s generated.


![Screenshot 2024-04-20 at 3 39 25 PM](https://github.com/stanfordio/cs152bots/assets/35933488/af2db3fe-16a9-4715-a591-9fb26e62d7b5)

5. Send that link to any of the TAs via Discord (or by email) - they will use it to add your bot to the server. Once they do, your bot will appear in the #general channel and will be a part of the server!


Note that these permissions are just a starting point for your bot. We think they’ll cover most cases, but it’s entirely possible you’ll run into cases where you want to be able to do more. If you do, you’re welcome to send updated links to the teaching team to re-invite your bot with new permissions. 


#### Setting up the starter code


First things first, the starter code is written in Python. You’ll want to make sure that you have Python 3 installed on your machine; if you don’t, follow [these instructions to install PyCharm](https://web.stanford.edu/class/cs106a/handouts/installingpycharm.html), the Stanford-recommended Python editor. Alternatively, you can use a text editor of your choice.


Once you’ve done that, open a terminal in the same folder as your bot.py file. (If you haven’t used your terminal before, check out [this guide](https://www.macworld.com/article/2042378/master-the-command-line-navigating-files-and-folders.html)!)



You’ll need to install some libraries if you don’t have them already, namely:


	# python3 -m pip install requests
	# python3 -m pip install discord.py


## Guide to the starter code

Next up, let’s take a look at what bot.py already does. To do this, run bot.py and leave it running in your terminal. Next, go into your team’s private group-# channel and try typing any message. You should see something like this pop up in the group-#-mod channel:


![Screenshot 2024-04-20 at 3 50 02 PM](https://github.com/stanfordio/cs152bots/assets/35933488/b5654bc6-8db1-4ea2-9f4c-5f4dca344058)


The default behavior of the bot is, any time it sees a message (from a user), it sends that message to the moderator channel with no possible actions. This is obviously not the final behavior you’ll want for your bot - you should update this to match your report flow. However, the infrastructure is there for your bot to automatically flag messages and (potentially) moderate them somehow.

Next up, click on your app in the right sidebar under “Online” to begin direct messaging it (or click on its name). First of all, try sending “help”. You should see a response like this (but with your group number instead of Group 0):


![Screenshot 2024-04-20 at 3 50 29 PM](https://github.com/stanfordio/cs152bots/assets/35933488/6ff900e9-03c0-44b0-be0b-5b4515abcbcb)



Try following its instructions from there by reporting a message from one of the channels to get a sense for the reporting flow that’s already built out for you. (Make sure to only report messages from channels that the bot is also in.)

If you look through the starter code, you’ll see the beginnings of the reporting flow that are already there. It will be up to you to build that out in whatever way your group decides is best. You’re welcome to edit any part of the starter code you’d like if you want to change what’s already there - we encourage it! This is just meant to be a starting point that you can pattern match off of.

If you’re not familiar with Python and asynchronous programming, please come to a section for an introduction. The TAs are happy to walk you through the starter code and explain anything that’s unclear.


## Troubleshooting


### Exception: tokens.json not found!

If you’re seeing this error, it probably means that your terminal is not open in the right folder. Make sure that it is open inside the folder that contains bot.py and tokens.json. You can check this by typing in ls and verifying that the output looks something like this:

```
	# ls
	bot.py 	tokens.json
```

 ### SSL: CERTIFICATE_VERIFY_FAILED error


Discord has a slight incompatibility with Python3 on Mac. To solve this, navigate to your /Applications/Python 3.6/ folder and double click the Install Certificates.command. Try running the bot again; it should be able to connect now. 

If you’re still having trouble, try running a different version of Python (i.e. use the command python3.7 or python3.8) instead. If that doesn’t work, come to section and we’ll be happy to help!


### intents has no attribute message_content error



This is an issue with the version of Discord API that is installed. Try the following steps: 
1. running ```pip install --upgrade``` discord in the terminal in your folder in the project that contains this file
2. IF that does not work, try changing the line in bot.py that says ```intents.message_content = True``` to  ```intents.messages = True```