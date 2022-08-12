import discord
import os
import random
from replit import db
# from keep_alive import keep_alive

# Questions are stored in an array inside the database

# Token is in hidden .env files. Please add your own.
TOKEN = os.environ['TOKEN']

client = discord.Client()

sample_question = ["https://leetcode.com/problems/two-sum/"]

# FUNCTIONS
# add question
def add_question(question_link):
  if "questions" in db.keys():
    questions = db["questions"]
    questions.append(question_link)
    db["questions"] = questions
  else:
    db["questions"] = [question_link]
  

# delete question
def del_question(index):
  questions = db["questions"]
  if len(questions) > index:
    del questions[index]
    db["questions"] = questions

# SETUP
@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

# USER COMMANDS
@client.event
async def on_message(message):
  # bot does not respond to itself
  if message.author == client.user:
      return
  # user's message
  msg = message.content

  # COMMANDS
  # test
  if msg.startswith('$test'):
    await message.channel.send("I'm working, YAY!")

  # generate question
  if msg.startswith('$leetcode'):
    # allow for database (if it exists) to be used with sample question
    options = sample_question
    if "questions" in db.keys():
      options.extend(db["questions"])
    await message.channel.send(random.choice(options))

  # add new question
  if msg.startswith('$add'):
    question_link = msg.split('$add ', 1)[1]
    add_question(question_link)
    await message.channel.send("New question added.")

  # delete question by index
  if msg.startswith('$del'):
    questions = []
    if "questions" in db.keys():
      index = int(msg.split("$del", 1)[1])
      del_question(index)
      questions = db["questions"]
    # send user list of questions
    await message.channel.send(questions)

client.run(TOKEN)