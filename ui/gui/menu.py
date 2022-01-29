import sys
import pygame

from bg import bg
import base64
from io import BytesIO
from PIL import Image

class GUI:

    def __init__(self, service):
        self.__width = 1280
        self.__height = 720
        self.__service = service

        pygame.init()
        pygame.display.set_caption('Connect 4')
        pygame.key.set_repeat(300, 30)
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__screen.fill((255, 255, 255))
        self.__clock = pygame.time.Clock()

        byte_data = base64.b64decode(bg)
        image_data = BytesIO(byte_data)
        image = Image.open(image_data)
        image = image.save("bg1.jpg")
        #self.__bg = pygame.image.fromstring(image, (1280, 720), "RGB")
        #self.__bg = pygame.image.load(image)
        self.__bg = pygame.image.load('bg1.jpg')
        pygame.display.flip()
        self.main_menu()

    @staticmethod
    def draw_text(text, font, color, surface, x=0, y=0, button=0):
        if button == 0:
            text_obj = font.render(text, 1, color)
            text_rect = text_obj.get_rect()
            text_rect.topleft = (x, y)
            surface.blit(text_obj, text_rect)
        else:
            text_obj = font.render(text, 1, color)
            text_rect = text_obj.get_rect()
            pos = button.center
            text_rect.center = button.center
            surface.blit(text_obj, text_rect)

    @property
    def rows(self):
        return 6

    @property
    def columns(self):
        return 7

    @property
    def square_size(self):
        return 100

    @property
    def row_border(self):
        return (self.__height - self.square_size * self.rows - self.square_size) // 2

    @property
    def column_border(self):
        return (self.__width - self.square_size * self.columns) // 2

    @property
    def white(self):
        return 255, 255, 255

    def main_menu(self):
        while True:

            font_title = pygame.font.Font(None, 70)
            self.__screen.fill((0, 0, 0))
            self.__screen.blit(self.__bg, (0, 0))
            title_x = int(self.__width / 2 - self.__width / 10)
            title_y = int(self.__height / 8)
            self.draw_text('Connect 4', font_title, self.white, self.__screen, x=title_x, y=title_y)

            mx, my = pygame.mouse.get_pos()

            button_width = int(0.3 * self.__width)
            button_height = int(0.1 * self.__height)
            button_x = int(self.__width / 2 - button_width / 2)
            button1_y = int(self.__height / 3)
            button2_y = int(button1_y + 2* button_height)
            button1 = pygame.Rect(button_x, button1_y, button_width, button_height)
            button2 = pygame.Rect(button_x, button2_y, button_width, button_height)
            button_surface = pygame.Surface((button_width, button_height)).convert_alpha()
            button_surface.fill((240, 50, 50, 100))

            button1_trans = button_surface.get_rect(bottomleft=button1.bottomleft)
            button2_trans = button_surface.get_rect(bottomleft=button2.bottomleft)

            if button1.collidepoint((mx, my)):
                if click:
                    self.__service.clear()
                    self.player_vs_player()
            if button2.collidepoint((mx, my)):
                if click:
                    self.__service.clear()
                    self.player_vs_ai()
            self.__screen.blit(button_surface, button1_trans)
            self.__screen.blit(button_surface, button2_trans)
            font_button = pygame.font.Font(None, 35)
            self.draw_text('Player vs Player', font_button, self.white, self.__screen, button=button1)
            self.draw_text('Player vs AI', font_button, self.white, self.__screen, button=button2)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.__clock.tick(60)

    def player_vs_player(self):
        turn = 0
        while True:
            self.__screen.fill((0, 0, 0))
            self.__screen.blit(self.__bg, (0, 0))
            self.draw_board(self.__service.get_board())

            x = max(self.column_border + self.square_size // 2, pygame.mouse.get_pos()[0])
            x = min(self.__width - self.column_border - self.square_size // 2, x)
            pos = (x, self.row_border + self.square_size // 2)

            if turn == 0:
                pygame.draw.circle(self.__screen, self.__service.player1_color, pos, self.square_size // 2 - 10)
            else:
                pygame.draw.circle(self.__screen, self.__service.player2_color, pos, self.square_size // 2 - 10)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0]
                    x -= self.column_border
                    if 0 < x <= self.square_size * self.columns:
                        column = x // self.square_size + 1
                        if turn == 0:
                            try:
                                self.__service.play_player1(column)
                                turn = 1
                            except ValueError:
                                pass

                            if self.__service.check_win_player1():
                                self.draw_board(self.__service.get_board())
                                pygame.display.update()
                                self.game_over('Player1 Wins!')
                                return

                        else:
                            try:
                                self.__service.play_player2(column)
                                turn = 0
                            except ValueError:
                                pass

                            if self.__service.check_win_player2():
                                self.draw_board(self.__service.get_board())
                                pygame.display.update()
                                self.game_over('Player2 Wins!')
                                return

                            if self.__service.played_chips == 42:
                                self.draw_board(self.__service.get_board())
                                pygame.display.update()
                                self.game_over('Draw!')
                                return
            pygame.display.update()
            self.__clock.tick(60)

    def player_vs_ai(self):
        while True:
            self.__screen.fill((0, 0, 0))
            self.__screen.blit(self.__bg, (0, 0))
            self.draw_board(self.__service.get_board())

            x = max(self.column_border + self.square_size // 2, pygame.mouse.get_pos()[0])
            x = min(self.__width - self.column_border - self.square_size // 2, x)
            pos = (x, self.row_border + self.square_size // 2)
            pygame.draw.circle(self.__screen, self.__service.player1_color, pos, self.square_size // 2 - 10)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0]
                    x -= self.column_border
                    if 0 < x <= self.square_size * self.columns:
                        column = x // self.square_size + 1
                        ok = False
                        try:
                            self.__service.play_player1(column)
                            ok = True
                        except ValueError:
                            pass

                        if ok:
                            if self.__service.check_win_player1():
                                self.draw_board(self.__service.get_board())
                                pygame.display.update()
                                self.game_over('Player1 Wins!')
                                return
                            self.draw_board(self.__service.get_board())
                            pygame.display.update()
                            self.__service.play_ai()

                            if self.__service.check_win_player2():
                                self.draw_board(self.__service.get_board())
                                pygame.display.update()
                                self.game_over('Computer Wins!')
                                return

                            if self.__service.played_chips == 42:
                                self.draw_board(self.__service.get_board())
                                pygame.display.update()
                                self.game_over('Draw!')
                                return
            pygame.display.update()
            self.__clock.tick(60)

    def draw_board(self, board):
        for row in range(self.rows):
            for column in range(self.columns):
                rect_size = (column * self.square_size + self.column_border,
                             row * self.square_size + self.square_size + self.row_border,
                             self.square_size,
                             self.square_size)
                pygame.draw.rect(self.__screen, (0, 0, 255), rect_size)
                circle_pos = (column * self.square_size + self.column_border + self.square_size // 2,
                              row * self.square_size + self.square_size + self.row_border + self.square_size // 2)
                rad = self.square_size // 2 - 10
                pygame.draw.circle(self.__screen, board[row][column].color, circle_pos, rad)

    def game_over(self, msg):
        while True:
            x = int(self.__width / 2 - self.__width / 10)
            y = int(self.__height / 20)
            font_over = pygame.font.SysFont(None, 70);
            self.draw_text(msg, font_over, self.white, self.__screen, x=x, y=y)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

            self.__clock.tick(60)
