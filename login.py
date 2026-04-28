# Filename: login.py
# Author: Jorge
# Description: This file implements the login screen for the Tamagotchi game using Pygame.
# It provides a user interface for players to enter their username and password, and buttons to either log in or create a new account.
# The login functionality is integrated with the auth_manager module, which manages user authentication and account creation.
import pygame
from pathlib import Path
from auth_manager import create_account, login

# run_login_screen
# This function runs the login screen loop. It displays input fields for username and password, and buttons for login and account creation.
# It handles user input, updates the display, and calls the appropriate functions from auth_manager to validate credentials or create accounts.
def run_login_screen(screen=None, pet=None, game_clock=None):

    standalone = screen is None  # fallback if called without game context

    pygame.init() # Initialize Pygame modules (e.g., font)

    # If no screen is provided, create a standalone window for the login screen. Otherwise, use the existing game screen.
    if standalone:
        width  = 500
        height = 500
        screen = pygame.display.set_mode((width, height))
    else:
        width  = screen.get_width()
        height = screen.get_height()

    font_path = Path(__file__).parent / "Fonts" / "Grand9K Pixel.ttf" # Load the custom font for the login screen
    
    # Define fonts for different UI elements using the loaded font file
    label_font   = pygame.font.Font(font_path, 18) # Font for labels like "Username:" and "Password:"
    input_font   = pygame.font.Font(font_path, 18) # Font for user input (username and password fields)
    button_font  = pygame.font.Font(font_path, 16) # Font for button labels ("Login" and "Create")
    message_font = pygame.font.Font(font_path, 14) # Font for displaying messages (e.g., error messages or success messages)
    
    # Variables to track user input and state
    username   = "" # Variable to store the current input for the username field
    password   = "" # Variable to store the current input for the password field
    active_box = "username" # Variable to track which input box is currently active (either "username" or "password")
    message    = "" # Variable to store messages to display to the user (e.g., error messages for invalid login or account creation issues)

    # Panel centered on screen
    panel_w, panel_h = width, height
    panel_x = 0
    panel_y = 0

    # Define rectangles for the username input box, password input box, login button, and create account button.
    username_box  = pygame.Rect(width // 2 - 90,  height // 2 - 80, 180, 32)
    password_box  = pygame.Rect(width // 2 - 90,  height // 2 - 30, 180, 32)
    login_button  = pygame.Rect(width // 2 - 160, height // 2 + 60, 140, 40)
    create_button = pygame.Rect(width // 2 + 20,  height // 2 + 60, 150, 40)

    #transparent dark panel (created once, drawn every frame)
    panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel_surf.fill((20, 20, 20, 210))

    running = True # Main loop for the login screen.

    # The loop continues until the user successfully logs in or creates an account, at 
    # which point the function will return the username of the logged-in user.
    while running:

        # If the login screen is running not in standalone mode and pet and game_clock are provided, 
        # update and draw the pet on the screen. Otherwise, fill the background with a plain color.
        if not standalone and pet is not None and game_clock is not None:
            dt = game_clock.tick(60)
            pet.update(dt)
            screen.fill((255, 255, 255))
            pet.draw(screen)
        else:
            screen.fill((30, 30, 30))  # plain background in standalone mode

        # Event handling for user input (keyboard and mouse events)
        for event in pygame.event.get():

            # Handle quit event to close the game window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle keyboard input for navigating between input boxes, entering text, and submitting the form
            if event.type == pygame.KEYDOWN:

                # Handle Tab key to switch between username and password input boxes
                if event.key == pygame.K_TAB:
                    active_box = "password" if active_box == "username" else "username"
                # Handle Backspace key to delete the last character in the active input box
                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the active input box (username or password) when Backspace is pressed
                    if active_box == "username":
                        username = username[:-1]
                    else:
                        password = password[:-1]
                # Handle Enter key to attempt login with the current username and password
                elif event.key == pygame.K_RETURN:
                    success, message = login(username, password) # Call the login function from auth_manager for current username and password
                    if success:
                        return username
                # Handle regular character input for the active input box (username or password)
                else:
                    # Append the typed character to the active input box (username or password) when a key is pressed
                    if active_box == "username":
                        username += event.unicode
                    else:
                        password += event.unicode
            # Handle mouse button down events for clicking on input boxes and buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on the username box, password box, login button, or create account button, and update the active box or attempt login/account creation accordingly
                if username_box.collidepoint(event.pos):
                    active_box = "username"
                # Check if the user clicked on the password box, and if so, set the active box to "password"
                elif password_box.collidepoint(event.pos):
                    active_box = "password"
                # Check if the user clicked on the login button, and if so, attempt to log in with the current username and password
                elif login_button.collidepoint(event.pos):
                    success, message = login(username, password) # Call the login function from auth_manager for current username and password
                    if success:
                        return username
                # Check if the user clicked on the create account button, and if so, attempt to create a new account with the current username and password
                elif create_button.collidepoint(event.pos):
                    success, message = create_account(username, password)

        # Draw login panel overlay on top of the game
        screen.blit(panel_surf, (panel_x, panel_y))
        pygame.draw.rect(screen, (100, 100, 255), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=8)

        # Render the title "Sign In" at the top of the panel, centered horizontally
        title_surf = label_font.render("Sign In", True, (255, 255, 255))
        screen.blit(title_surf, (panel_x + (panel_w - title_surf.get_width()) // 2, panel_y + 18))

        # Highlight the active input box by changing its color
        if active_box == "username":
            username_color = (110, 110, 110)
            password_color = (70,  70,  70)
        else:
            username_color = (70,  70,  70)
            password_color = (110, 110, 110)

        # Draw the input boxes, buttons, labels, and user input on the screen
        pygame.draw.rect(screen, username_color, username_box, border_radius=4)
        pygame.draw.rect(screen, password_color, password_box, border_radius=4)
        pygame.draw.rect(screen, (100, 150, 250), login_button,  border_radius=6)
        pygame.draw.rect(screen, (100, 250, 150), create_button, border_radius=6)

        # Render the labels for the username and password fields
        screen.blit(label_font.render("Username:", True, (255, 255, 255)), (width // 2 - 200, height // 2 - 80))
        screen.blit(label_font.render("Password:", True, (255, 255, 255)), (width // 2 - 200, height // 2 - 30))
        # Render the user input for the username and password fields
        screen.blit(input_font.render(username,             True, (255, 255, 255)), (username_box.x + 8, username_box.y + 7))
        screen.blit(input_font.render("*" * len(password), True, (255, 255, 255)), (password_box.x + 8, password_box.y + 7))

        # Render the labels for the login and create account buttons, centered within the buttons
        login_lbl  = button_font.render("Login",  True, (0, 0, 0))
        create_lbl = button_font.render("Create", True, (0, 0, 0))
        screen.blit(login_lbl,  (login_button.x  + (login_button.width  - login_lbl.get_width())  // 2,
                                  login_button.y  + (login_button.height - login_lbl.get_height()) // 2))
        screen.blit(create_lbl, (create_button.x + (create_button.width  - create_lbl.get_width())  // 2,
                                  create_button.y + (create_button.height - create_lbl.get_height()) // 2))
        # If there is a message to display (e.g., error message for invalid login), render it below the buttons
        if message:
            msg_surf = message_font.render(message, True, (255, 100, 100))
            screen.blit(msg_surf, (panel_x + (panel_w - msg_surf.get_width()) // 2, panel_y + 145))

        # Update the display to show all the drawn elements on the screen
        pygame.display.update()