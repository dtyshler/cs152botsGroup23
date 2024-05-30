import discord
import os
import json
import logging
import re
from report import Report
from mod import Mod

# Set up logging to the console
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# There should be a file called 'tokens.json' inside the same folder as this file
token_path = 'tokens.json'
if not os.path.isfile(token_path):
    raise Exception(f"{token_path} not found!")
with open(token_path) as f:
    # If you get an error here, it means your token is formatted incorrectly. Did you put it in quotes?
    tokens = json.load(f)
    discord_token = tokens['discord']


class ModBot(discord.Client):
    def __init__(self): 
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.group_num = None
        self.mod_channels = {} # Map from guild to the mod channel id for that guild
        self.reports = {} # Map from user IDs to the state of their report
        self.mod_flows = {} # Map from moderator's ID to state of their mod flow
        self.mod_channel = None

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord! It is these guilds:')
        for guild in self.guilds:
            print(f' - {guild.name}')
        print('Press Ctrl-C to quit.')

        # Parse the group number out of the bot's name
        match = re.search('[gG]roup (\d+) [bB]ot', self.user.name)
        if match:
            self.group_num = match.group(1)
        else:
            raise Exception("Group number not found in bot's name. Name format should be \"Group # Bot\".")

        # Find the mod channel in each guild that this bot should report to
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == f'group-{self.group_num}-mod':
                    self.mod_channels[guild.id] = channel
                    self.mod_channel = channel
        

    async def on_message(self, message):
        '''
        This function is called whenever a message is sent in a channel that the bot can see (including DMs). 
        Currently the bot is configured to only handle messages that are sent over DMs or in your group's "group-#" channel. 
        '''
        # Ignore messages from the bot 
        if message.author.id == self.user.id:
            return

        # Check if this message was sent in a server ("guild") or if it's a DM
        if message.guild:
            if message.channel == self.mod_channel:
                await self.handle_mod_message(message)
            else:
                await self.handle_channel_message(message)
        else:
            await self.handle_dm(message)

    async def handle_dm(self, message):
        # Handle a help message
        if message.content == Report.HELP_KEYWORD:
            reply =  "Use the `report` command to begin the reporting process.\n"
            reply += "Use the `cancel` command to cancel the report process.\n"
            await message.channel.send(reply)
            return

        author_id = message.author.id
        responses = []

        # Only respond to messages if they're part of a reporting flow
        if author_id not in self.reports and not message.content.startswith(Report.START_KEYWORD):
            return

        # If we don't currently have an active report for this user, add one
        if author_id not in self.reports:
            self.reports[author_id] = Report(self)

        # Let the report class handle this message; forward all the messages it returns to uss
        responses = await self.reports[author_id].handle_message(message, self.mod_channel)
        for r in responses:
            await message.channel.send(r)
        
        # If the report is complete or cancelled, remove it from our map
        if self.reports[author_id].report_complete():
            self.reports.pop(author_id)

    async def handle_channel_message(self, message):
        # Only handle messages sent in the "group-#" channel
        if not message.channel.name == f'group-{self.group_num}':
            return

        # Forward the message to the mod channel
        mod_channel = self.mod_channels[message.guild.id]
        await mod_channel.send(f'Forwarded message:\n{message.author.name}: "{message.content}"')
        scores = self.eval_text(message.content)
        await mod_channel.send(self.code_format(scores))

    async def handle_mod_message(self, message):
        author_id = message.author.id
        responses = []
        if author_id not in self.mod_flows and not message.content.startswith(Mod.START_KEYWORD):
            return
        # If we don't currently have an active mod class for this user, add one
        if author_id not in self.mod_flows:
            self.mod_flows[author_id] = Mod(self)
        
        # Let the report class handle this message; forward all the messages it returns to us
        responses = await self.mod_flows[author_id].handle_message(message, self.mod_channel)
        for r in responses:
            await message.channel.send(r)

        # Modify the eval_text and code_format functions here
        # Assuming that the report object is accessible and contains the classification result
        if self.mod_flows[author_id].state == State.REPORT_SUBMITTED:
            report = self.mod_flows[author_id]
            message_content = report.reported_message.content
            evaluation_result = report.classify_message(message_content)
            formatted_result = self.code_format(evaluation_result)
            await message.channel.send(formatted_result)

        # If the report is complete or cancelled, remove it from our map
        if self.mod_flows[author_id].report_complete():
            self.mod_flows.pop(author_id)

    def eval_text(self, message):
        ''''
        Placeholder for message evaluation logic
        '''
        return classify_message(message)

    def code_format(self, evaluation_result):
        ''''
        Formats the string to be shown in the mod channel.
        '''
        print(f"evaluation_result: {evaluation_result}")  # Print the evaluation result for debugging

        # Unpack the evaluation result
        message_content, is_issue = evaluation_result

        # Format the output message
        if is_issue:
            return f"Evaluated: Message '{message_content}' is an issue."
        else:
            return f"Evaluated: Message '{message_content}' is not an issue."


def classify_message(message_content):
    # Dummy classification logic for demonstration
    # In a real scenario, this would call an actual classification function
    is_issue = "issue" in message_content.lower()
    return message_content, is_issue


client = ModBot()
client.run(discord_token)
