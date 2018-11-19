import discord
import google.cloud.texttospeech as texttospeech
import logging
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\tonyz\\Documents\\Github\\DiscordLilyBot-c99c72ebfdfd.json"

googleClient = texttospeech.TextToSpeechClient()

global chosenVoice

TOKEN = 'Insert Token Here'

logging.basicConfig(level=logging.INFO)
discordClient = discord.Client()
# discord.opus.load_opus(opuslib)

voices = ['UK Female','UK Male','US Female', 'US Male', 'AUS Female', 'AUS Male']
voiceIDs = ['en-GB-Standard-A','en-GB-Standard-B','en-US-Standard-C','en-US-Standard-B','en-AU-Standard-A','en-AU-Standard-B']
chosenVoice = 0

lily = 'snickerton'

t = 'Hello World'

def to_speech(text):
    input_text = texttospeech.types.SynthesisInput(text=text)
    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    print(voiceIDs[chosenVoice][0:5])
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=voiceIDs[chosenVoice][0:5],
        name=voiceIDs[chosenVoice])

    audio_config = texttospeech.types.AudioConfig(
         audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = googleClient.synthesize_speech(input_text, voice, audio_config)
    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
         out.write(response.audio_content)
         print('Audio content written to file "output.mp3"')

    return response


@discordClient.event
async def on_message(message):
    global voice
    global channel
    global chosenVoice

    if message.content == "!voices":
        msg = ''
        for v in voices:
            msg = msg+str(voices.index(v)) + ": " + v +"\n"
        await discordClient.send_message(message.channel, msg)

    if message.content.startswith("!chooseVoice"):
        chosenVoice = int(message.content[13:14])
        print(str(chosenVoice))
        await discordClient.send_message(message.channel, "Voice chosen: " + voices[chosenVoice])

    if message.content == "!join" or message.content == "!connect":
        for vclient in discordClient.voice_clients:
            vclient.disconnect()
        channel = message.author.voice.voice_channel
        voice = await discordClient.join_voice_channel(channel)

    if message.content == "!unjoin" or message.content == "!disconnect":
        for vclient in discordClient.voice_clients:
            vclient.disconnect()

    if (not message.content.startswith("!")) and message.author.name == lily:
        if len(discordClient.voice_clients) == 0:
            channel = message.author.voice.voice_channel
            voice = await discordClient.join_voice_channel(channel)
        print('author is ' + lily)
        r = to_speech(message.content)
        # voice.play_audio(r.audio_content,encode=True)
        player = voice.create_ffmpeg_player('output.mp3')
        player.start()


@discordClient.event
async def on_ready():
    print('Logged in as')
    print(discordClient.user.name)
    print(discordClient.user.id)
    if discord.opus.is_loaded():
        print("opus loaded.")
    else:
        print("opus not loaded!")
    print('------')
    # voice = await discordClient.join_voice_channel(channel)


discordClient.run(TOKEN)


