import pygame
import math

pygame.init()

FRAME_PER_SECOND = 120
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

BACKGROUND_COLOR = (204,204,204)
BACKGROUND_COLOR_HIGHLIGHT = (0,0,0)
FONT_COLOR = (0,0,0)
FONT_COLOR_HIGHLIGHT = (0,0,0)
FONT_SIZE = 32

setting_commands = ''
with open('setting.txt') as f:
	setting_commands = f.read()
exec( setting_commands )

raw_script = ''
with open('script.txt') as f:
	raw_script = f.read()

script_array = []
word = ''
for character in raw_script:
	if character == ' ' or character == '\n':
		script_array.append( word )
		script_array.append( character )
		word = ''
	else:
		word = word + character

def get_render_text_size( text ):
	my_font = pygame.font.SysFont('malgungothic', FONT_SIZE)
	return my_font.size( text );

font_height = 0
screen_line_number = 0
def change_font_size( size ):
	global font_height, screen_line_number
	font_height = get_render_text_size('a')[1]
	screen_line_number = math.ceil( SCREEN_HEIGHT / font_height)
change_font_size( FONT_SIZE )


script_array_arranged = []
script_array_index_of_first_word = []
def arrange_script():
	line = ''
	script_array_index_of_first_word.append(0);
	for index in range(len(script_array)):
		word = script_array[index]
		if word == '\n':
			script_array_arranged.append(line)
			script_array_index_of_first_word.append(index)
			line = ''
			continue
		if get_render_text_size( line + word )[0] > SCREEN_WIDTH:
			script_array_arranged.append(line)
			script_array_index_of_first_word.append(index)
			line = word
			continue
		if line == '':
			if word == ' ':
				continue
		line = line + word
	script_array_arranged.append(line)
arrange_script()

def change_setting():
	setting_commands = f'''
	# (red, green, blue): max 255

	BACKGROUND_COLOR = { str(BACKGROUND_COLOR) }
	BACKGROUND_COLOR_HIGHLIGHT = { str(BACKGROUND_COLOR_HIGHLIGHT) }
	FONT_COLOR = { str(FONT_COLOR) }
	FONT_COLOR_HIGHLIGHT = { str(FONT_COLOR_HIGHLIGHT) }
	FONT_SIZE = { str(FONT_SIZE) }
	'''
	with open('setting.txt','w') as f:
		f.write(setting_commands[1:].replace('	',''))

screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE )
pygame.display.set_caption('Teleprompter')


current_line_number = 0

def handle_key():
	pass

def render_text(text, coo, color=FONT_COLOR):
	my_font = pygame.font.SysFont('malgungothic',FONT_SIZE)
	rendered_text = my_font.render(text, True, color)
	screen.blit(rendered_text, coo)

def render_screen():
	screen.fill( BACKGROUND_COLOR )
	for i in range(screen_line_number):
		render_text(script_array_arranged[current_line_number+i], (0,i*font_height) )

print(script_array_arranged)

running = True
clock = pygame.time.Clock()
while running:
	clock.tick( FRAME_PER_SECOND )
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			handle_key()
		elif event.type == pygame.VIDEORESIZE:
			SCREEN_WIDTH, SCREEN_HEIGHT = event.size
			arrange_script()
		elif event.type == pygame.VIDEOEXPOSE:
			SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
			arrange_script()
	render_screen()
	pygame.display.flip()

pygame.quit();