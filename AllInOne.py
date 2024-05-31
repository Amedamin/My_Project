from flask import Flask, render_template, url_for, redirect
import pygame
import os
import sys
from pygame.locals import *
from time import strftime
import calendar
from datetime import datetime
import random

app = Flask(__name__)

A_ll = [
{
        'id': 1,
        'name': 'Calculator',
        'icon': 'calculator.png',
        'description': 'Effortlessly crunch numbers with our calculator. It is calculates more than one mathematical operation in one colect, and you can perform another operation on the previous result.'
    },

        {
        'id': 2 ,
        'name': 'Time with Date',
        'icon': 'clock.png',
        'description': 'Stay in sync with the universe with our elegant timepiece, always keeping you grounded in the present moment. It show the date and time based on your device. Enjoy with it.'
    },

    {
        'id': 3 ,
        'name': 'Calendar',
        'icon': 'calendar.png',
        'description': "Your personal assistant for organizing life's moments. Scroll through all the months and years using the keyboard or the calendar window. You can also specify the day to increase your focus."
    },
        {
        'id': 4 ,
        'name': 'To Do List',
        'icon': 'ToDoList.jpg',
        'description': 'Transform chaos into order with this dynamic to-do list. Streamline your thoughts and enhance focus on tasks. Add tasks by clicking "ADD" or pressing Enter. Delete tasks by selecting them and pressing Delete. You can delete the last character by pressing backspace. Tasks are written in a single line for clarity and simplicity.'
    },

        {
        'id': 5,
        'name': 'Timer',
        'icon': 'timer.png',
        'description': 'Command time with precision using our versatile timer, maximizing productivity and focus.'
    },
]

Games = [

        {
        'id': 6 ,
        'name': 'Ping Pong',
        'icon': '6.png',
        'description': 'Control your paddle with keyboard inputs to hit the ball back and forth. Score points by outmaneuvering your opponent and making it difficult for them to return the ball.'
    },


        {
        'id': 7,
        'name': 'Music Color',
        'icon': 'music.png',
        'description': 'Stay alert and responsive to the rhythm of the music to accurately match colors and create mesmerizing visual symphonies. It make you relaxed and to perform your tasks with more focus.'
    }
]

Comment = [
        {
        'id': 9,
        'name': 'Comment',
    } ]

BLACK = (0,0,0) 

def calc(): # Function to Calculations
    pygame.init()  # Initialize Pygame
    FONT = pygame.font.Font(None, 60)  # Set the font
    WIDTH_C, HEIGHT_C = 400, 600  # Window size
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (180, 100, 50)

    class Beg:
        def __init__(self, text, x, y, w, h):
            self.text = text
            self.rect = pygame.Rect(x, y, w, h)  # Create a rectangle for the button
            self.color = ORANGE  # Button color

        def draw(self, win):
            # Draw the button rectangle
            pygame.draw.rect(win, self.color, self.rect)
            pygame.draw.rect(win, BLACK, self.rect, 2)
            txt_surface = FONT.render(self.text, True, BLACK)  # Render the text on the button
            # Center the text on the button
            win.blit(txt_surface, (self.rect.x + (self.rect.width - txt_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - txt_surface.get_height()) // 2))

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)  # Check if the button is clicked

    def create_buttons():
        # Function to create calculator buttons
        return [
            Beg("7", 0, 150, 100, 100), Beg("8", 100, 150, 100, 100), Beg("9", 200, 150, 100, 100),
            Beg("/", 300, 150, 100, 100),
            Beg("4", 0, 250, 100, 100), Beg("5", 100, 250, 100, 100), Beg("6", 200, 250, 100, 100),
            Beg("*", 300, 250, 100, 100),
            Beg("1", 0, 350, 100, 100), Beg("2", 100, 350, 100, 100), Beg("3", 200, 350, 100, 100),
            Beg("-", 300, 350, 100, 100),
            Beg("0", 100, 450, 100, 100), Beg(".", 0, 450, 100, 100), Beg("=", 200, 450, 100, 100),
            Beg("+", 300, 450, 100, 100),
            Beg("C", 0, 550, 300, 50)
        ]

    def initialize_calculator_state():
        return {"begin_input": "", "operation": "", "sec_operand": None, "calculation_process": ""}

    def calculate(first_operand, second_operand, operation):
        # Function to handle arithmetic calculations
        try:
            if operation == "+":
                return str(first_operand + second_operand)
            elif operation == "-":
                return str(first_operand - second_operand)
            elif operation == "*":
                return str(first_operand * second_operand)
            elif operation == "/":
                return str(first_operand / second_operand)
        except Exception as e:
            return "Error"

    def handle_button_click(button, state):
        # Function to handle button clicks
        if button.text == "C":
            state["begin_input"] = ""
            state["sec_operand"] = None
            state["operation"] = ""
            state["calculation_process"] = ""
        elif button.text in "0123456789.":
            state["begin_input"] += button.text
            state["calculation_process"] += button.text
        elif button.text in "+-*/":
            if state["begin_input"]:
                if state["sec_operand"] is None:
                    state["sec_operand"] = float(state["begin_input"])
                else:
                    state["sec_operand"] = float(calculate(state["sec_operand"], float(state["begin_input"]), state["operation"]))
                state["operation"] = button.text
                state["begin_input"] = ""
                state["calculation_process"] += " " + button.text + " "
        elif button.text == "=":
            if state["begin_input"] and state["sec_operand"] is not None:
                second_operand = float(state["begin_input"])
                result = calculate(state["sec_operand"], second_operand, state["operation"])
                state["begin_input"] = result
                state["sec_operand"] = None
                state["operation"] = ""
                state["calculation_process"] += " = " + result

    def draw_calculator(win, buttons, state):
        win.fill(WHITE)  # Clear the window

        # Render the ongoing calculation process
        display_text = state["calculation_process"]
        wrapped_text = wrap_text(FONT, display_text, WIDTH_C - 20)

        # Render the wrapped text
        y = 10
        for line in wrapped_text:
            win.blit(line, (10, y))
            y += line.get_height()

        for button in buttons:
            button.draw(win)
        pygame.display.update()

    def wrap_text(font, text, max_width):
        # Wrap text to fit within the given width
        words = text.split(' ')
        lines = []
        while words:
            line = ''
            while words and font.size(line + words[0])[0] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(font.render(line, True, BLACK))
        return lines

    # Main function to run the calculator
    def run_calculator():
        win = pygame.display.set_mode((WIDTH_C, HEIGHT_C))  # Set up the window
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the directory
        icon_path = os.path.join(script_dir, 'static', 'calculator.png')
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Calculator")

        buttons = create_buttons()  # Create calculator buttons
        state = initialize_calculator_state()
        RUN = True
        while RUN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUN = False
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for button in buttons:
                        if button.is_clicked(pos):
                            handle_button_click(button, state)
            if RUN == False:
                break
            draw_calculator(win, buttons, state)
            pygame.display.update()

    run_calculator()
    pygame.quit()

def time_widgets(): # Function to update time and date
    # Set up the window
    pygame.init()
    WIDTH, HEIGHT = 320, 180
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Get the icon and name
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path of the directory where pythonic.py is located
    icon_path = os.path.join(script_dir, 'static', 'clock.png')
    Icon = pygame.image.load(icon_path)
    pygame.display.set_icon(Icon) 
    pygame.display.set_caption("Clock & Date")

    # Font settings
    font_time = pygame.font.Font(None, 60)
    font_date = pygame.font.Font(None, 30)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return 0
        
        # Get current time and date strings
        time_string = strftime("%I:%M:%S %p")
        day_string = strftime("%A")
        date_string = strftime("%B %d, %Y")
        
        # Render time and date strings as text surfaces
        time_surface = font_time.render(time_string, True, (0, 255, 0))
        day_surface = font_date.render(day_string, True, (255, 255, 255))
        date_surface = font_date.render(date_string, True, (255, 255, 255))
        
        # Clear the window
        window.fill(BLACK)
        
        # Blit time and date text surfaces onto the window
        window.blit(time_surface, (50, 50))
        window.blit(day_surface, (50, 120))
        window.blit(date_surface, (50, 150))
        # Update the display
        pygame.display.update()
        # Wait for 1 second before updating again
        pygame.time.wait(1000)
    pygame.quit()

def Calendar(): # Function to show Calendar
    # Initialize Pygame
    pygame.init()
    # Set up display
    WIDTH_cl, HEIGHT_cl = 400, 500
    screen = pygame.display.set_mode((WIDTH_cl, HEIGHT_cl))
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 24)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (108,109,111)
    DARKRED = (130, 0, 0)
    # Get current date
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    selected_day = None
    # Function to draw the calendar on the screen
    def draw_calendar(year, month, selected_day):
        screen.fill(LIGHT_GRAY)

        # Month and Year
        month_year_text = f"{calendar.month_name[month]} {year}"
        text_surface = font.render(month_year_text, True, BLACK)
        screen.blit(text_surface, (WIDTH_cl // 2 - text_surface.get_width() // 2, 10))

        # Days of the week
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            text_surface = small_font.render(day, True, BLACK)
            screen.blit(text_surface, (i * 50 + 20, 50))

        # Calendar days
        cal = calendar.monthcalendar(year, month)
        for week_index, week in enumerate(cal):
            for day_index, day in enumerate(week):
                if day != 0:
                    day_rect = pygame.Rect(day_index * 50 + 20, week_index * 50 + 80, 40, 40)
                    if day == selected_day:
                        pygame.draw.rect(screen, DARKRED, day_rect)
                    text_surface = small_font.render(str(day), True, BLACK)
                    screen.blit(text_surface, (day_index * 50 + 30, week_index * 50 + 90))

        # Year Input
        year_text = small_font.render("Year:", True, BLACK)
        screen.blit(year_text, (20, HEIGHT_cl - 70))
        year_input = small_font.render(str(current_year), True, BLACK)
        screen.blit(year_input, (80, HEIGHT_cl - 70))

        # Month Input
        month_text = small_font.render("Month:", True, BLACK)
        screen.blit(month_text, (200, HEIGHT_cl - 70))
        month_input = small_font.render(str(current_month), True, BLACK)
        screen.blit(month_input, (270, HEIGHT_cl - 70))

    # Get the icon and name
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path of the directory
    icon_path = os.path.join(script_dir, 'static', 'calendar.png')
    Icon = pygame.image.load(icon_path)
    pygame.display.set_icon(Icon)
    pygame.display.set_caption("Calendar")

    RUN = True
    clock = pygame.time.Clock()
    input_active = False
    input_type = None
    user_text = ""

    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                pygame.quit()
                return 0
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 < y < 400:
                    row = (y - 80) // 50
                    col = (x - 20) // 50
                    if 0 <= row < 6 and 0 <= col < 7:
                        cal = calendar.monthcalendar(current_year, current_month)
                        if cal[row][col] != 0:
                            selected_day = cal[row][col]
                elif HEIGHT_cl - 80 < y < HEIGHT_cl - 50:
                    if 80 < x < 140:
                        input_active = True
                        input_type = "year"
                        user_text = ""
                    elif 270 < x < 330:
                        input_active = True
                        input_type = "month"
                        user_text = ""
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if input_type == "year":
                        try:
                            current_year = int(user_text)
                        except ValueError:
                            pass
                    elif input_type == "month":
                        try:
                            month = int(user_text)
                            if 1 <= month <= 12:
                                current_month = month
                        except ValueError:
                            pass
                    input_active = False
                    input_type = None
                    user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        # Handle left and right arrow key presses for changing the month
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            current_month -= 1
            if current_month < 1:
                current_month = 12
                current_year -= 1
            selected_day = None
            pygame.time.delay(200)
        if keys[pygame.K_RIGHT]:
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
            selected_day = None
            pygame.time.delay(200)

        draw_calendar(current_year, current_month, selected_day)
        # Handle input field rendering if active
        if input_active:
            input_rect = pygame.Rect(80 if input_type == "year" else 270, HEIGHT_cl - 70, 60, 30)
            pygame.draw.rect(screen, WHITE, input_rect)
            input_surface = small_font.render(user_text, True, BLACK)
            screen.blit(input_surface, input_rect.topleft)

        pygame.display.flip() # Update the display and control the frame rate
        clock.tick(30)
        
    pygame.quit() # Quit Pygame

def ToDoList(): # Function to show To-Do List
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 520, 700
    BLUE = (10,200,225)  
    LIGHT_GRAY = (108,109,111) 
    BG_COLOR = (30, 30, 30)
    BUTTON_COLOR = (70, 70, 70)
    FONT_SIZE = 30
    FO = 50

    # Setup the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # Get the icon and name
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path of the directory where pythonic.py is located
    icon_path = os.path.join(script_dir, 'static', 'check.png')
    Icon = pygame.image.load(icon_path)
    pygame.display.set_icon(Icon) 
    pygame.display.set_caption("To-Do List")

    # Font
    font = pygame.font.Font(None, FONT_SIZE)
    font_add = pygame.font.Font(None, FO)
    # Input box
    input_box = pygame.Rect(10, 50, 400, 60)
    user_text = ''
    # Buttons
    add_button = pygame.Rect(420, 50, 90, 60)

    # To-Do list items
    todo_items = []
    selected_index = None

    def draw_text(text, x, y, font, color): # Helper function to draw text on the screen.
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def draw_button(button_rect, text, font, color, hover_color): # Helper function to draw a button with text on the screen.
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, button_rect)
        else:
            pygame.draw.rect(screen, color, button_rect)
        draw_text(text, button_rect.x + 10, button_rect.y + 10, font, BLUE)

    clock = pygame.time.Clock()
    RUN = True
    # Main loop
    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Exit the program
                RUN = False
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  # Remove last character from input
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:  # Add task on Enter key
                    if user_text.strip():
                        todo_items.append(user_text.strip())
                        user_text = ''
                else:  # Add character to input
                    # Check if adding a character will exceed the input box width
                    if font.size(user_text)[0] <= input_box.width:
                        user_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if add_button.collidepoint(event.pos): # Add task
                    if user_text.strip():
                        todo_items.append(user_text.strip())
                        user_text = ''
                else:  # Select task
                    for idx in range(len(todo_items)):
                        item_rect = pygame.Rect(50, 120 + idx * 40, 700, 40)
                        if item_rect.collidepoint(event.pos):
                            selected_index = idx
                            break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE and selected_index is not None:  # Delete selected task
                    del todo_items[selected_index]
                    selected_index = None
                    user_text = ''

        if RUN == False:
            break
        # Fill the background
        screen.fill(BG_COLOR)
        
        # Draw input box
        pygame.draw.rect(screen, BUTTON_COLOR, input_box)
        # Render text with word wrapping
        lines = [user_text[i:i+34] for i in range(0, len(user_text), 30)]
        for i, line in enumerate(lines):
            draw_text(line, input_box.x + 10, input_box.y + 10 + i*20, font, BLUE)

        # Draw buttons
        draw_button(add_button, "Add", font_add, BUTTON_COLOR, LIGHT_GRAY)

        # Draw the to-do list items
        for idx, item in enumerate(todo_items):
            item_text = f"{idx + 1}. {item}"
            item_color = BLUE if idx != selected_index else LIGHT_GRAY
            draw_text(item_text, 20, 150 + idx * 33, font, item_color)
        
        # Update the display
        pygame.display.flip()
        clock.tick(30)  # Maintain 30 FPS
    pygame.quit()

def comment(): # Function to take the user comments
    pygame.init()

    # Constants
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    BACKGROUND_COLOR = (255, 255, 255)
    TEXT_COLOR = (0, 0, 0)
    BOX_COLOR = (200, 200, 200)
    BUTTON_COLOR = (200, 128, 50)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    FONT_SIZE = 24
    PADDING = 10

    # Initialize screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Get the icon and name
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path of the directory
    icon_path = os.path.join(script_dir, 'static', 'comments.png')
    Icon = pygame.image.load(icon_path)
    pygame.display.set_icon(Icon)
    pygame.display.set_caption("Comment Service")

    # Introductory text
    intro_text = "Please enter your comment in english"

    # Text box
    text_box = pygame.Rect(PADDING, PADDING + FONT_SIZE + 2 * PADDING, WINDOW_WIDTH - 2 * PADDING, FONT_SIZE + 2 * PADDING)
    text = ''
    input_active = True

    # Save button
    button_font = pygame.font.Font(None, FONT_SIZE)
    button_text = button_font.render("Save", True, BUTTON_TEXT_COLOR)
    button_width, button_height = button_text.get_size()
    button_rect = pygame.Rect(WINDOW_WIDTH - button_width - 2 * PADDING, WINDOW_HEIGHT - button_height - 2 * PADDING, button_width + PADDING, button_height + PADDING)
    # Function to save text to file
    def save_text_to_file(text):
        with open("comments.txt", "a", encoding='utf-8') as file:
            file.write(text.replace('\n', ' ') + '\n')
    # Function to draw the text box with word wrapping
    def draw_text_box(screen, text, rect, font, text_color, box_color):
        pygame.draw.rect(screen, box_color, rect)  # Draw the box
        words = text.split(' ')  # Split text into words
        space_width, space_height = font.size(' ')  # Get space dimensions
        x, y = rect.x + PADDING, rect.y + PADDING  # Initial cursor position
        max_width = rect.width - 2 * PADDING  # Maximum width for text in the box
        lines = [] # List to store lines of text
        current_line = ""
        # Loop through each word and add to current line or start a new line
        for word in words:
            word_surface = font.render(word, True, text_color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                lines.append(current_line)  # Save the current line
                current_line = word + " "  # Start a new line
                x = rect.x + PADDING  # Reset x position
                y += word_height + 5  # Move to next line
            else:
                current_line += word + " "
            x += word_width + space_width

        lines.append(current_line) # Move x position
        y = rect.y + PADDING # Reset y position for drawing
        # Render and draw each line of text
        for line in lines:
            line_surface = font.render(line, True, text_color)
            screen.blit(line_surface, (rect.x + PADDING, y))
            y += line_surface.get_height() + 5

        rect.height = y - rect.y + PADDING # Update rectangle height
        return rect
    Run = True # Main loop control variable
    # Main loop
    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:# Handle quit event
                Run = False
                pygame.quit()
                return 0
            if event.type == pygame.KEYDOWN: # Handle key press events
                if input_active:
                    if event.key == pygame.K_RETURN: # Save text on Enter
                        save_text_to_file(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:# Remove last character on Backspace
                        text = text[:-1]
                    else:
                        text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    save_text_to_file(text)
                    text = ''

        screen.fill(BACKGROUND_COLOR)# Clear the screen

        # Render the introductory text
        font = pygame.font.Font(None, FONT_SIZE)
        intro_surface = font.render(intro_text, True, TEXT_COLOR)
        intro_rect = intro_surface.get_rect(center=(WINDOW_WIDTH // 2, 30))  # Position the text at the top center
        screen.blit(intro_surface, intro_rect)

        # Render the text box
        text_box = draw_text_box(screen, text, text_box, font, TEXT_COLOR, BOX_COLOR)

        # Render the save button
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        screen.blit(button_text, (button_rect.x + PADDING // 2, button_rect.y + PADDING // 2))

        pygame.display.flip() # Update the display

def reset_b(ball, ball_speed_x, ball_speed_y, screen_width):# Function to reset the ball's position and speed
    ball.x = screen_width / 2 - 10
    ball.y = random.randint(10, 100)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])
    return ball_speed_x, ball_speed_y
def point_w(winner, ball, ball_speed_x, ball_speed_y, screen_width, cpu_points, player_points):# Function to update points and reset ball after a point is won
    if winner == "cpu":
        cpu_points += 1
    if winner == "player":
        player_points += 1

    ball_speed_x, ball_speed_y = reset_b(ball, ball_speed_x, ball_speed_y, screen_width)
    return cpu_points, player_points, ball_speed_x, ball_speed_y
def animate_b(ball, ball_speed_x, ball_speed_y, screen_width, screen_height, cpu_points, player_points, player, cpu):# Function to animate the movement of the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y
     # Ball collision with top or bottom of the screen
    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1
    # Ball collision with right or left side of the screen (point won)
    if ball.right >= screen_width:
        cpu_points, player_points, ball_speed_x, ball_speed_y = point_w("cpu", ball, ball_speed_x, ball_speed_y, screen_width, cpu_points, player_points)

    if ball.left <= 0:
        cpu_points, player_points, ball_speed_x, ball_speed_y = point_w("player", ball, ball_speed_x, ball_speed_y, screen_width, cpu_points, player_points)
    # Ball collision with player or CPU paddles
    if ball.colliderect(player) or ball.colliderect(cpu):
        ball_speed_x *= -1

    return ball_speed_x, ball_speed_y, cpu_points, player_points
def animate_p(player, player_speed, screen_height):# Function to animate the player's paddle
    player.y += player_speed
     # Keep player paddle within screen bounds
    if player.top <= 0:
        player.top = 0
    
    if player.bottom >= screen_height:
        player.bottom = screen_height
def animate_cpu(cpu, ball, cpu_speed, screen_height):# Function to animate the CPU's paddle
    if ball.centery <= cpu.centery: # CPU follows the ball's vertical position
        cpu_speed = -6
    if ball.centery >= cpu.centery:
        cpu_speed = 6

    cpu.y += cpu_speed
     # Keep CPU paddle within screen bounds
    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height

    return cpu_speed
def pingpong(): # Main function to run the game
    # Initialize pygame and set up the game window
    pygame.init()
    screen_width = 800
    screen_height = 600
    GRAEE = (128, 128, 128)
    screen = pygame.display.set_mode((screen_width, screen_height))
    # Get the icon and name
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path of the directory
    icon_path = os.path.join(script_dir, 'static', '6.png')
    Icon = pygame.image.load(icon_path)
    pygame.display.set_icon(Icon)
    pygame.display.set_caption("Ping-Pong")

    clock = pygame.time.Clock()
    # Initialize game objects and variables
    ball = pygame.Rect(0, 0, 30, 30)
    ball.center = (screen_width / 2, screen_height / 2)

    cpu = pygame.Rect(0, 0, 20, 100)
    cpu.centery = screen_height / 2

    player = pygame.Rect(0, 0, 20, 100)
    player.midright = (screen_width, screen_height / 2)

    ball_speed_x = 6
    ball_speed_y = 6
    player_speed = 0
    cpu_speed = 6

    cpu_points, player_points = 0, 0

    score_font = pygame.font.Font(None, 100)
    
    Run = True
    while Run:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed = -6
                if event.key == pygame.K_DOWN:
                    player_speed = 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_speed = 0
                if event.key == pygame.K_DOWN:
                    player_speed = 0

        # Change the positions of the game objects
        ball_speed_x, ball_speed_y, cpu_points, player_points = animate_b(ball, ball_speed_x, ball_speed_y, screen_width, screen_height, cpu_points, player_points, player, cpu)
        animate_p(player, player_speed, screen_height)
        cpu_speed = animate_cpu(cpu, ball, cpu_speed, screen_height)

        # Clear the screen
        screen.fill(GRAEE)

        # Draw the score
        cpu_score_surface = score_font.render(str(cpu_points), True, "white")
        player_score_surface = score_font.render(str(player_points), True, "white")
        screen.blit(cpu_score_surface, (screen_width / 4, 20))
        screen.blit(player_score_surface, (3 * screen_width / 4, 20))

        # Draw the game objects
        pygame.draw.aaline(screen, 'white', (screen_width / 2, 0), (screen_width / 2, screen_height))
        pygame.draw.ellipse(screen, 'black', ball)
        pygame.draw.rect(screen, 'white', cpu)
        pygame.draw.rect(screen, 'white', player)

        # Update the display
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
@app.route('/All/<int:All_id>')
def start_All(All_id):
    if All_id == 1:
        calc()

    elif All_id == 2:
        time_widgets()

    elif All_id == 3:
        Calendar()

    elif All_id == 4:
        ToDoList()

    #elif All_id == 5:
        #timer()

    elif All_id == 6:
        pingpong()

    #elif All_id == 7:
       # music_colors()

    return render_template('begin.html', A_ll=A_ll, Games=Games)

@app.route('/Comment/<int:All_id>')
def start_Comment(All_id):
    if All_id == 9:
        comment()
    return render_template('endcom.html')

@app.route("/Begin")
def Start():
    return render_template('begin.html', A_ll=A_ll, Games=Games)

if __name__=="__main__":
    app.run(debug=True)
