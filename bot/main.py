import telebot
from telebot import types
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

TOKEN = "6344833079:AAE7OwH-dZkkh-JXZeGnS7dJ_Dz9cHNPosQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Hello!")
	
@bot.message_handler(func=lambda message: message.text.startswith("http"))
def text(message):
	url_video = message.text
	chat_id = message.chat.id
	save_path = "./video"
	download_video(url_video, chat_id, message, save_path)

@bot.message_handler(content_types=["video"])
def video(message):
	chat_id = message.chat.id
	video_id = message.video.file_id
	
	# Получаем информацию о видео по его file_id
	video_info = bot.get_file(video_id)
	
	# Скачиваем видео
	save_path = f"./videos/{video_info.file_id}.mp4"
	url_video = f"https://api.telegram.org/file/bot{TOKEN}/{video_info.file_id}"
	download_video(url_video, chat_id, message, save_path)
	

def download_video(url, chat_id, message, save_path):
	try:
		yt = YouTube(url)
		video = yt.streams.get_lowest_resolution()
		print(f"Download video {yt.title}")
		bot.send_message(chat_id, f"Download video: {yt.title}", parse_mode="html")
		video.download(save_path)
		print("Download video: OK")
		bot.send_message(chat_id, "Download video: OK")
		#bot.edit_message_text(text="Download video: OK", chat_id=chat_id, message_id=message.message_id)
		ad = yt.title.replace('|', '').replace('?', '').replace(',', '')
		audio = f"./video/{ad}.mp4"
		convert(audio, f"./audio/{ad}.mp3", ad, chat_id, message)
	except Exception as e:
		print(f"Error: {str(e)}")
		bot.send_message(chat_id, "Sorry, an unexpected error occurred")


def convert(input_path, output_path, ad, chat_id, message):
	try:
		print("Convert...")
		bot.send_message(chat_id, "Convert...")
		#bot.edit_message_text(text="Convert...", chat_id=chat_id, message_id=message.message_id)
		video_clip = VideoFileClip(input_path)
		audio_clip = video_clip.audio
		audio_clip.write_audiofile(output_path)
		audio_clip.close()
		video_clip.close()
		print("Convert: OK")
		bot.send_message(chat_id, "Convert: OK")
		#bot.edit_message_text(text="Convert: OK", chat_id=chat_id, message_id=message.message_id)
		delete(input_path)
		send_audio(chat_id, f"./audio/{ad}.mp3")
	except Exception as e:
		print(f"Error: {str(e)}")
		bot.send_message(chat_id, f"Error: {str(e)}")
		delete(input_path)

def send_audio(chat_id, input_audio):
	with open(input_audio, "rb") as audio_file:
		bot.send_document(chat_id, audio_file)
		delete(input_audio)
			

def delete(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")
	
	
	
bot.polling(none_stop=True)
