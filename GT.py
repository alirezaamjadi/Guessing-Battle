import pygame, sys, random

# ----------------- تنظیمات اولیه -----------------
pygame.init()
pygame.display.set_caption("Guessing Battle")
INFO_OBJECT = pygame.display.Info()
WIDTH, HEIGHT = INFO_OBJECT.current_w, INFO_OBJECT.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60

# ----------------- رنگ‌ها -----------------
BG_COLOR = (135, 206, 250)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (255, 182, 193)
BUTTON_HOVER = (255, 105, 180)
SCORE_COLOR = (255, 255, 0)
WIN_BG = (173, 216, 230)
WIN_TEXT = (255, 69, 0)
INPUT_BG = (255, 228, 181)

# ----------------- فونت‌ها -----------------
FONT_LARGE = pygame.font.SysFont("Comic Sans MS", 80, bold=True)
FONT_MEDIUM = pygame.font.SysFont("Comic Sans MS", 50, bold=True)
FONT_SMALL = pygame.font.SysFont("Comic Sans MS", 35)

# ----------------- کلاس دکمه -----------------
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=25)
        txt = FONT_MEDIUM.render(self.text, True, (0,0,0))
        surface.blit(txt, txt.get_rect(center=self.rect.center))

# ----------------- رسم متن -----------------
def draw_text(text, color, y, large=False, center=True, x=None):
    font = FONT_LARGE if large else FONT_MEDIUM
    txt_surface = font.render(text, True, color)
    if center:
        rect = txt_surface.get_rect(center=(WIDTH//2, y))
    else:
        rect = txt_surface.get_rect(topleft=(x, y))
    screen.blit(txt_surface, rect)

# ----------------- نمایش امتیاز -----------------
def draw_scores(scores):
    y_offset = 50
    for player, score in scores.items():
        txt = FONT_SMALL.render(f"{player}: {score}", True, SCORE_COLOR)
        screen.blit(txt, (WIDTH-300, y_offset))
        y_offset += 50

# ----------------- دریافت ورودی -----------------
def get_input(prompt):
    input_text = ""
    active = True
    while active:
        screen.fill(BG_COLOR)
        draw_text(prompt, (255,255,0), HEIGHT//3, large=True)
        input_rect = pygame.Rect(WIDTH//2-220, HEIGHT//2+50, 440, 90)
        pygame.draw.rect(screen, INPUT_BG, input_rect, border_radius=20)

        txt_surface = FONT_MEDIUM.render(input_text, True, TEXT_COLOR)
        screen.blit(txt_surface, txt_surface.get_rect(center=input_rect.center))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None  # برگشت به منو
                elif event.key == pygame.K_RETURN and input_text.strip() != "":
                    return input_text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

# ----------------- حلقه بازی -----------------
def game_loop(player1, player2):
    scores = {player1:0, player2:0}
    turn = 0
    max_score = 5
    max_guesses = 10
    running = True

    while running:
        guesses_left = max_guesses
        target = random.randint(1, 100)
        current_player = player1 if turn %2 ==0 else player2

        while guesses_left > 0:
            screen.fill(BG_COLOR)
            draw_text(f"{current_player}'s Turn", TEXT_COLOR, HEIGHT//6, large=True)
            draw_text(f"Guesses left: {guesses_left}", TEXT_COLOR, HEIGHT//3)
            draw_text("Enter your guess (1-100):", TEXT_COLOR, HEIGHT//2 -120)
            draw_scores(scores)

            input_rect = pygame.Rect(WIDTH//2-220, HEIGHT//2+50, 440, 90)
            pygame.draw.rect(screen, INPUT_BG, input_rect, border_radius=20)
            pygame.display.flip()

            guess = None
            input_text = ""
            active_input = True
            while active_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return  # ESC → منو
                        elif event.key == pygame.K_RETURN and input_text.isdigit():
                            guess = int(input_text)
                            active_input = False
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            input_text += event.unicode

                screen.fill(BG_COLOR)
                draw_text(f"{current_player}'s Turn", TEXT_COLOR, HEIGHT//6, large=True)
                draw_text(f"Guesses left: {guesses_left}", TEXT_COLOR, HEIGHT//3)
                draw_text("Enter your guess (1-100):", TEXT_COLOR, HEIGHT//2 -120)

                pygame.draw.rect(screen, INPUT_BG, input_rect, border_radius=20)
                txt_surface = FONT_MEDIUM.render(input_text, True, TEXT_COLOR)
                screen.blit(txt_surface, txt_surface.get_rect(center=input_rect.center))

                draw_scores(scores)
                pygame.display.flip()
                clock.tick(FPS)

            guesses_left -=1
            if guess == target:
                scores[current_player] +=1
                break
            elif guess < target:
                info = "Too low!"
            else:
                info = "Too high!"

            screen.fill(BG_COLOR)
            draw_text(info, WIN_TEXT, HEIGHT//2)
            draw_scores(scores)
            pygame.display.flip()
            pygame.time.wait(900)

        for p,s in scores.items():
            if s>=max_score:
                winner_screen(p, target)
                return
        turn +=1

# ----------------- صفحه برنده -----------------
def winner_screen(winner, number):
    waiting = True
    btn = Button("Menu", WIDTH//2-150, HEIGHT//2 +180, 300, 70)
    while waiting:
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, WIN_BG, (WIDTH//2-380, HEIGHT//2-180, 760, 360), border_radius=35)
        draw_text(f"{winner} WINS! 🏆", WIN_TEXT, HEIGHT//2 -60, large=True)
        draw_text(f"The correct number was: {number}", (0,0,0), HEIGHT//2 +40)
        btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # ESC → منو
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    waiting = False

# ----------------- About Game Screen -----------------
def about_screen():
    waiting = True
    btn = Button("Menu", WIDTH//2-150, HEIGHT-120, 300, 70)
    while waiting:
        screen.fill(BG_COLOR)

        # Creator info
        draw_text("About Game", (255,215,0), 100, large=True)
        draw_text("Creator: Haj Alireza Amjadi", (0,0,0), 200)
        draw_text("Year: 2025", (0,0,0), 260)
        draw_text("Development Tool: VS Code", (0,0,0), 320)
        draw_text("Language: Python", (0,0,0), 380)

        # Game instructions
        draw_text("How to Play:", (0,128,0), 480)
        draw_text("1. Two-player game.", (0,0,0), 540)
        draw_text("2. Each player takes turns guessing a number from 1 to 100.", (0,0,0), 600)
        draw_text("3. Correct guess earns a point.", (0,0,0), 660)
        draw_text("4. Each player has 10 guesses per turn.", (0,0,0), 720)
        draw_text("5. First to reach 5 points wins.", (0,0,0), 780)
        draw_text("6. Press ESC to return to the main menu.", (0,0,0), 840)

        btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # ESC → Back to Menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    waiting = False



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # ESC → منو
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    waiting = False

# ----------------- منو اصلی -----------------
def main_menu():
    global WIDTH, HEIGHT, screen
    buttons = [
        Button("Start Game", WIDTH//2-200, HEIGHT//3, 400, 80),
        Button("About Game", WIDTH//2-200, HEIGHT//3 +120, 400, 80),
        Button("Full Screen", WIDTH//2-200, HEIGHT//3 +240, 400, 80),
        Button("Exit", WIDTH//2-200, HEIGHT//3 +360, 400, 80)
    ]
    fullscreen = True

    while True:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()  # ESC تو منو = خروج
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].rect.collidepoint(mouse_pos):
                    p1 = get_input("Enter Player 1 Name:")
                    if not p1: continue
                    p2 = get_input("Enter Player 2 Name:")
                    if not p2: continue
                    game_loop(p1,p2)
                elif buttons[1].rect.collidepoint(mouse_pos):
                    about_screen()
                elif buttons[2].rect.collidepoint(mouse_pos):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((1280,720))
                    WIDTH, HEIGHT = screen.get_size()
                    buttons = [
                        Button("Start Game", WIDTH//2-200, HEIGHT//3, 400, 80),
                        Button("About Game", WIDTH//2-200, HEIGHT//3 +120, 400, 80),
                        Button("Full Screen", WIDTH//2-200, HEIGHT//3 +240, 400, 80),
                        Button("Exit", WIDTH//2-200, HEIGHT//3 +360, 400, 80)
                    ]
                elif buttons[3].rect.collidepoint(mouse_pos):
                    pygame.quit(); sys.exit()
        clock.tick(FPS)

# ----------------- شروع -----------------
main_menu()
