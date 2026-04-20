import pygame
from pathlib import Path
from auth_manager import create_account, login

def run_login_screen(screen=None, pet=None, game_clock=None):

    standalone = screen is None  # fallback if called without game context

    pygame.init()

    if standalone:
        width  = 500
        height = 500
        screen = pygame.display.set_mode((width, height))
    else:
        width  = screen.get_width()
        height = screen.get_height()

    font_path = Path(__file__).parent / "Fonts" / "Grand9K Pixel.ttf"

    label_font   = pygame.font.Font(font_path, 18)
    input_font   = pygame.font.Font(font_path, 18)
    button_font  = pygame.font.Font(font_path, 16)
    message_font = pygame.font.Font(font_path, 14)

    username   = ""
    password   = ""
    active_box = "username"
    message    = ""

    # Panel centered on screen
    panel_w, panel_h = width, height
    panel_x = 0
    panel_y = 0

    username_box  = pygame.Rect(width // 2 - 90,  height // 2 - 80, 180, 32)
    password_box  = pygame.Rect(width // 2 - 90,  height // 2 - 30, 180, 32)
    login_button  = pygame.Rect(width // 2 - 160, height // 2 + 60, 140, 40)
    create_button = pygame.Rect(width // 2 + 20,  height // 2 + 60, 150, 40)

    #transparent dark panel (created once, drawn every frame)
    panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel_surf.fill((20, 20, 20, 210))

    running = True

    while running:

        #tick and draw the live game behind the login overlay
        if not standalone and pet is not None and game_clock is not None:
            dt = game_clock.tick(60)
            pet.update(dt)
            screen.fill((255, 255, 255))
            pet.draw(screen)
        else:
            screen.fill((30, 30, 30))  # plain background in standalone mode

        #events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:
                    active_box = "password" if active_box == "username" else "username"

                elif event.key == pygame.K_BACKSPACE:
                    if active_box == "username":
                        username = username[:-1]
                    else:
                        password = password[:-1]

                elif event.key == pygame.K_RETURN:
                    success, message = login(username, password)
                    if success:
                        return True

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

        # Draw login panel overlay on top of the game

        screen.blit(panel_surf, (panel_x, panel_y))
        pygame.draw.rect(screen, (100, 100, 255), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=8)

        title_surf = label_font.render("Sign In", True, (255, 255, 255))
        screen.blit(title_surf, (panel_x + (panel_w - title_surf.get_width()) // 2, panel_y + 18))

        if active_box == "username":
            username_color = (110, 110, 110)
            password_color = (70,  70,  70)
        else:
            username_color = (70,  70,  70)
            password_color = (110, 110, 110)

        pygame.draw.rect(screen, username_color, username_box, border_radius=4)
        pygame.draw.rect(screen, password_color, password_box, border_radius=4)
        pygame.draw.rect(screen, (100, 150, 250), login_button,  border_radius=6)
        pygame.draw.rect(screen, (100, 250, 150), create_button, border_radius=6)

        screen.blit(label_font.render("Username:", True, (255, 255, 255)), (width // 2 - 200, height // 2 - 80))
        screen.blit(label_font.render("Password:", True, (255, 255, 255)), (width // 2 - 200, height // 2 - 30))
        
        screen.blit(input_font.render(username,             True, (255, 255, 255)), (username_box.x + 8, username_box.y + 7))
        screen.blit(input_font.render("*" * len(password), True, (255, 255, 255)), (password_box.x + 8, password_box.y + 7))

        login_lbl  = button_font.render("Login",  True, (0, 0, 0))
        create_lbl = button_font.render("Create", True, (0, 0, 0))
        screen.blit(login_lbl,  (login_button.x  + (login_button.width  - login_lbl.get_width())  // 2,
                                  login_button.y  + (login_button.height - login_lbl.get_height()) // 2))
        screen.blit(create_lbl, (create_button.x + (create_button.width  - create_lbl.get_width())  // 2,
                                  create_button.y + (create_button.height - create_lbl.get_height()) // 2))

        if message:
            msg_surf = message_font.render(message, True, (255, 100, 100))
            screen.blit(msg_surf, (panel_x + (panel_w - msg_surf.get_width()) // 2, panel_y + 145))

        pygame.display.update()