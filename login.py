import pygame
from pathlib import Path
from auth_manager import create_account, login


def run_login_screen():

    pygame.init()

    width = 500
    height = 500

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Login")

    font_path = Path(__file__).parent / "Fonts" / "Grand9K Pixel.ttf"

    label_font = pygame.font.Font(font_path, 18)
    input_font = pygame.font.Font(font_path, 18)
    button_font = pygame.font.Font(font_path, 16)
    message_font = pygame.font.Font(font_path, 14)

    username = ""
    password = ""

    active_box = "username"
    message = ""

    username_box = pygame.Rect(250, 180, 180, 32)
    password_box = pygame.Rect(250, 230, 180, 32)

    login_button = pygame.Rect(60, 330, 140, 40)
    create_button = pygame.Rect(250, 330, 190, 40)

    running = True

    while running:

        screen.fill((30, 30, 30))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:
                    if active_box == "username":
                        active_box = "password"
                    else:
                        active_box = "username"

                elif event.key == pygame.K_BACKSPACE:
                    if active_box == "username":
                        username = username[:-1]
                    else:
                        password = password[:-1]

                elif event.key == pygame.K_RETURN:
                    pass

                else:
                    if active_box == "username":
                        username += event.unicode
                    else:
                        password += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:

                if username_box.collidepoint(event.pos):
                    active_box = "username"

                elif password_box.collidepoint(event.pos):
                    active_box = "password"

                elif login_button.collidepoint(event.pos):
                    success, message = login(username, password)
                    if success:
                        return True

                elif create_button.collidepoint(event.pos):
                    success, message = create_account(username, password)

        if active_box == "username":
            username_color = (110, 110, 110)
            password_color = (70, 70, 70)
        else:
            username_color = (70, 70, 70)
            password_color = (110, 110, 110)

        pygame.draw.rect(screen, username_color, username_box)
        pygame.draw.rect(screen, password_color, password_box)

        pygame.draw.rect(screen, (100, 150, 250), login_button)
        pygame.draw.rect(screen, (100, 250, 150), create_button)

        username_text = label_font.render("Username:", True, (255, 255, 255))
        password_text = label_font.render("Password:", True, (255, 255, 255))
        signin_text = label_font.render("Sign In", True, (255, 255, 255))

        screen.blit(username_text, (60, 180))
        screen.blit(password_text, (60, 230))
        screen.blit(signin_text, (210, 120))

        user_surface = input_font.render(username, True, (255, 255, 255))
        hidden_password = "*" * len(password)
        pass_surface = input_font.render(hidden_password, True, (255, 255, 255))

        screen.blit(user_surface, (username_box.x + 8, username_box.y + 7))
        screen.blit(pass_surface, (password_box.x + 8, password_box.y + 7))

        login_text = button_font.render("Login", True, (0, 0, 0))
        create_text = button_font.render("Create", True, (0, 0, 0))

        login_text_x = login_button.x + (login_button.width - login_text.get_width()) // 2
        login_text_y = login_button.y + (login_button.height - login_text.get_height()) // 2

        create_text_x = create_button.x + (create_button.width - create_text.get_width()) // 2
        create_text_y = create_button.y + (create_button.height - create_text.get_height()) // 2

        screen.blit(login_text, (login_text_x, login_text_y))
        screen.blit(create_text, (create_text_x, create_text_y))

        msg_surface = message_font.render(message, True, (255, 100, 100))
        msg_x = (width - msg_surface.get_width()) // 2
        screen.blit(msg_surface, (msg_x, 160))

        pygame.display.update()