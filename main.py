import sys

from helper import *

from game import Game
from button import Button


class Main:
    def __init__(self):
        """
        constructor
        """
        self.screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))  # màn hình chính
        pygame.display.set_caption('ULTIMATE TIC TAC TOE')  # gán tên cửa sổ
        self.status_screen = 0
        self.game = Game()

    def set_status_screen(self, type=0):
        """
        set status screen
        :param type: type of status
        :return:
        """
        self.status_screen = type
        """
        0 Main screen
        1 Type play screen
        2 Gui game screen
        3 Difficulty level play screen
        4 Play screen
        """

    def mainloop(self):
        pygame.mixer.init()
        music_background()
        while True:
            screen = self.screen
            self.screen.fill(BG_COLOR)

            mouse_pos = pygame.mouse.get_pos()

            # draw
            if self.status_screen == 0:
                self.main_screen(screen, mouse_pos)
            elif self.status_screen == 1:
                self.type_play(screen, mouse_pos)
            elif self.status_screen == 2:
                self.gui_game_screen(screen, mouse_pos)
            elif self.status_screen == 3:
                self.difficulty_level_play(screen, mouse_pos)
            elif self.status_screen == 4:
                self.play_screen(screen, mouse_pos)

            pygame.display.update()

    def main_screen(self, surface, mouse_pos):
        main_text = get_font(70).render("ULTIMATE TICTACTOE", True, "#545454")
        main_rect = main_text.get_rect(center=(WIDTH_WINDOW // 2, 80))
        surface.blit(main_text, main_rect)

        play_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 250),
                             text_input="CHƠI", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        guide_play_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 425),
                                   text_input="Hướng dẫn", font=get_font(60), base_color="#d7fcd4",
                                   hovering_color="White")
        quit_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 600),
                             text_input="Thoát", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        for button in [play_button, guide_play_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_click_mouse()

                if play_button.checkForInput(mouse_pos):
                    self.set_status_screen(1)
                if guide_play_button.checkForInput(mouse_pos):
                    self.set_status_screen(2)
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

    def gui_game_screen(self, surface, mouse_pos):
        main_text = get_font(70).render("ULTIMATE TICTACTOE", True, "#545454")
        main_rect = main_text.get_rect(center=(WIDTH_WINDOW // 2, 80))
        surface.blit(main_text, main_rect)
        size = 27
        texts = [get_font(size).render("Game sẽ gồm 9 bàn cờ nhỏ và 1 bàn cờ lớn bao phủ 9", True, "White"),
                 get_font(size).render("bàn cờ nhỏ. Người chơi sẽ chơi để chiến thắng tại", True, "White"),
                 get_font(size).render("các bàn cờ nhỏ để được quân tại bàn cờ đó. Cách", True, "White"),
                 get_font(size).render("chiến thắng là đạt được 3 ô liên tiếp (ngang, dọc,", True, "White"),
                 get_font(size).render("chéo) cũng như tại bàn cờ nhỏ, lớn. Nếu không thể", True, "White"),
                 get_font(size).render("đánh được ô nào hết thì sẽ hoà. Và bạn chỉ có thể", True, "White"),
                 get_font(size).render("đánh các ô tại bàn nhỏ phù hợp. bàn nhỏ phù hợp", True, "White"),
                 get_font(size).render("dựa vào nước đánh trước của đối thủ. Ví dụ tại bàn", True, "White"),
                 get_font(size).render("nhỏ này đánh tại vị trí trung tâm thì bạn chỉ có", True, "White"),
                 get_font(size).render("thể tại bàn nhỏ ở vị trí trung tâm của bàn cờ lớn", True, "White"),
                 get_font(size).render("và nếu bàn cờ nhỏ đó đã bị chiếm hoặc không còn", True, "White"),
                 get_font(size).render("chỗ để đánh thì có thể đánh bất kì chỗ nào.", True, "White"),
                 ]

        xpos = 27
        ypos = 130

        for text in texts:
            surface.blit(text, (xpos, ypos))
            ypos += 35

        back_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"),
                             pos=(WIDTH_WINDOW // 2, HEIGHT_WINDOW - 65),
                             text_input="Quay lại", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        for button in [back_button]:
            button.changeColor(mouse_pos)
            button.update(surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_click_mouse()

                if back_button.checkForInput(mouse_pos):
                    self.set_status_screen()

    def type_play(self, surface, mouse_pos):
        main_text = get_font(70).render("ULTIMATE TICTACTOE", True, "#545454")
        main_rect = main_text.get_rect(center=(WIDTH_WINDOW // 2, 80))
        surface.blit(main_text, main_rect)

        play_with_ai_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 180),
                                     text_input="Chơi với máy", font=get_font(48), base_color="#d7fcd4",
                                     hovering_color="White")
        play_with_player_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"),
                                         pos=(WIDTH_WINDOW // 2, 330),
                                         text_input="Chơi 2 người", font=get_font(48), base_color="#d7fcd4",
                                         hovering_color="White")
        ai_play_together_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"),
                                         pos=(WIDTH_WINDOW // 2, 480),
                                         text_input="Máy với máy", font=get_font(48), base_color="#d7fcd4",
                                         hovering_color="White")
        back_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 630),
                             text_input="Quay lại", font=get_font(48), base_color="#d7fcd4", hovering_color="White")

        for button in [play_with_ai_button, play_with_player_button, ai_play_together_button, back_button]:
            button.changeColor(mouse_pos)
            button.update(surface)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_click_mouse()

                if play_with_ai_button.checkForInput(mouse_pos):
                    self.set_status_screen(3)
                if play_with_player_button.checkForInput(mouse_pos):
                    self.game = Game()
                    self.set_status_screen(4)
                if ai_play_together_button.checkForInput(mouse_pos):
                    pass
                if back_button.checkForInput(mouse_pos):
                    self.set_status_screen()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def difficulty_level_play(self, surface, mouse_pos):
        main_text = get_font(70).render("ULTIMATE TICTACTOE", True, "#545454")
        main_rect = main_text.get_rect(center=(WIDTH_WINDOW // 2, 80))
        surface.blit(main_text, main_rect)

        level_easy_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 180),
                                   text_input="Dễ", font=get_font(48), base_color="#d7fcd4",
                                   hovering_color="White")
        level_normal_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 330),
                                     text_input="Bình thường", font=get_font(48), base_color="#d7fcd4",
                                     hovering_color="White")
        level_difficult_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"),
                                        pos=(WIDTH_WINDOW // 2, 480),
                                        text_input="Khó", font=get_font(48), base_color="#d7fcd4",
                                        hovering_color="White")
        back_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 630),
                             text_input="Quay lại", font=get_font(48), base_color="#d7fcd4",
                             hovering_color="White")

        for button in [level_easy_button, level_normal_button, level_difficult_button, back_button]:
            button.changeColor(mouse_pos)
            button.update(surface)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_click_mouse()

                if level_easy_button.checkForInput(mouse_pos):
                    self.game = Game(1, 0)
                    self.set_status_screen(4)
                if level_normal_button.checkForInput(mouse_pos):
                    self.game = Game(1, 1)
                    self.set_status_screen(4)
                if level_difficult_button.checkForInput(mouse_pos):
                    self.game = Game(1, 2)
                    self.set_status_screen(4)
                if back_button.checkForInput(mouse_pos):
                    self.set_status_screen(1)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def play_screen(self, surface, mouse_pos):
        game = self.game
        game.render_screen_game(surface)

        play_again_button = Button(image=None,
                                   pos=(self.game.board.dims.size + self.game.board.margin + 120, HEIGHT_WINDOW - 100),
                                   text_input="Chơi lại", font=get_font(30), base_color="#d7fcd4",
                                   hovering_color="White")
        back_button = Button(image=None,
                             pos=(self.game.board.dims.size + self.game.board.margin + 120, HEIGHT_WINDOW - 50),
                             text_input="Quay lại", font=get_font(30), base_color="#d7fcd4",
                             hovering_color="White")

        for button in [play_again_button, back_button]:
            button.changeColor(mouse_pos)
            button.update(surface)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_click_mouse()

                if play_again_button.checkForInput(mouse_pos):
                    self.game.restart()
                elif back_button.checkForInput(mouse_pos):
                    self.set_status_screen(1)
                elif game.playing and game.player_playing:
                    game.play_turn_click(mouse_pos[0], mouse_pos[1])

            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.run_ai()


if __name__ == '__main__':
    main = Main()
    main.mainloop()
