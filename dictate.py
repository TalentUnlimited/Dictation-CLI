from gtts import gTTS
from playsound import *

import os
import time

import msvcrt
import click

from rich.progress import Progress
from rich.console import Console


console = Console()

@click.command()
@click.option("--file", required=True, help='Input a File [.txt recommended]', type=click.File('r'))
@click.option("--factor", default=1.0, help="Adjust Speed of Dictation")
def dictate(file, factor):
	'''
	A Dictation CLI Tool	
	'''
	text = file.read()

	text_list = ["_"] + (text.replace("\n", " newline ")).split() + ["_"]
	
	console.print("[light_goldenrod3]Press Enter to Pause \nPress Left Arrow to Rewind")
	with Progress(console=console, auto_refresh=False) as progress:
		task = progress.add_task(f'[green]{text_list[0]}, {text_list[1]}, {text_list[2]}', total=len(text_list)-2)
		word_index = 1

		while word_index < len(text_list)-1:
			word = text_list[word_index]
			tts = gTTS(word)
			
			tts.save('text.mp3')
			playsound('text.mp3')
			os.remove('text.mp3')

			time.sleep(len(word)/factor)
			
			if msvcrt.kbhit():
				key = ord(msvcrt.getch())
				if key == 13:
					progress.update(task, description=f'[white]{text_list[word_index-1]}, {text_list[word_index]}, {text_list[word_index+1]}', refresh=True)
					os.system("pause > nul")
				if key == 224:
					key = ord(msvcrt.getch())
					if key == 75:
						word_index -= 1
						progress.update(task, description=f"[green]{text_list[word_index-1]}, {text_list[word_index]}, {text_list[word_index+1]}", advance=-1, refresh=True)
						continue
			
			progress.update(task, description=f'[green]{text_list[word_index-1]}, {text_list[word_index]}, {text_list[word_index+1]}', advance=1, refresh=True)
			word_index += 1

if __name__ == '__main__':
	dictate()