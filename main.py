import sys

from helper import *

from game import Game
from button import Button

base_color = "#d7fcd4"
active = [[True, False] for _ in range(2)]


class Main:
    def __init__(self):
        """
        constructor
        """
        self.screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))  # main window
        pygame.display.set_caption('ULTIMATE TIC TAC TOE')  # caption
        pygame_icon = pygame.image.load('Resourse/Image/logo_ultimate_tictactoe.png')
        pygame.display.set_icon(pygame_icon)  # logo
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
        5 Pick AI screen
        """

    def mainloop(self):
        """
        main loop
        :return:
        """
        pygame.mixer.init()  # init mixer
        music_background()

        while True:
            screen = self.screen
            self.screen.fill(BG_COLOR)

            mouse_pos = pygame.mouse.get_pos()

            # switch screen
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
            elif self.status_screen == 5:
                self.pick_AI_screen(screen, mouse_pos)

            # update change
            pygame.display.update()

    def main_screen(self, surface, mouse_pos):
        """
        main screen (home)
        :param surface: current surface
        :param mouse_pos: current mouse position
        :return:
        """
        main_text = get_font(70).render("ULTIMATE TICTACTOE", True, "#545454")
        main_rect = main_text.get_rect(center=(WIDTH_WINDOW // 2, 80))
        surface.blit(main_text, main_rect)

        play_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 250),
                             text_input="CHƠI", font=get_font(60), base_color=base_color, hovering_color="White")
        guide_play_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 425),
                                   text_input="Hướng dẫn", font=get_font(60), base_color=base_color,
                                   hovering_color="White")
        quit_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 600),
                             text_input="Thoát", font=get_font(60), base_color=base_color, hovering_color="White")

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
        """
        gui game screen
        :param surface: current surface
        :param mouse_pos: current mouse position
        :return:
        """
        main_text = get_font(70).render("ULTIMATE TICTACTOE", True, "#545454")
        main_rect = main_text.get_rect(center=(WIDTH_WINDOW // 2, 80))
        surface.blit(main_text, main_rect)
        size = 27
        texts = [get_font(size).render("Game sẽ gồm 9 bàn cờ nhỏ và 1 bàn cờ lớn bao phủ 9 bàn", True, "White"),
                 get_font(size).render("cờ nhỏ. Người chơi sẽ chơi để chiến thắng tại các bàn", True, "White"),
                 get_font(size).render("cờ nhỏ để được quân tại bàn cờ đó. Cách chiến thắng là", True, "White"),
                 get_font(size).render("đạt được 3 ô liên tiếp (ngang, dọc, chéo) cũng như tại", True, "White"),
                 get_font(size).render("bàn cờ nhỏ, lớn. Nếu không thể đánh được ô nào hết thì", True, "White"),
                 get_font(size).render("sẽ hoà. Và bạn chỉ có thể đánh các ô tại bàn nhỏ phù", True, "White"),
                 get_font(size).render("hợp. Bàn nhỏ phù hợp dựa vào nước đánh trước của đối", True, "White"),
                 get_font(size).render("thủ. Ví dụ tại bàn nhỏ này đánh tại vị trí trung tâm", True, "White"),
                 get_font(size).render("thì bạn chỉ có thể tại bàn nhỏ ở vị trí trung tâm của", True, "White"),
                 get_font(size).render("bàn cờ lớn và nếu bàn cờ nhỏ đó đã bị chiếm hoặc không", True, "White"),
                 get_font(size).render("còn chỗ để đánh thì có thể đánh bất kì chỗ nào.", True, "White"),
                 ]

        xpos = 27
        ypos = 150

        for text in texts:
            surface.blit(text, (xpos, ypos))
            ypos += 35

        back_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"),
                             pos=(WIDTH_WINDOW // 2, HEIGHT_WINDOW - 65),
                             text_input="Quay lại", font=get_font(60), base_color=base_color, hovering_color="White")

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
        """
        type play screen
        :param surface: current surface
        :param mouse_pos: current mouse position
        :return:
        """
        main_text = get_font(70).render("ULTIMATE TICTACTOE", True, "#545454")
        main_rect = main_text.get_rect(center=(WIDTH_WINDOW // 2, 80))
        surface.blit(main_text, main_rect)

        play_with_ai_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 180),
                                     text_input="Chơi với máy", font=get_font(48), base_color=base_color,
                                     hovering_color="White")
        play_with_player_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"),
                                         pos=(WIDTH_WINDOW // 2, 330),
                                         text_input="Chơi 2 người", font=get_font(48), base_color=base_color,
                                         hovering_color="White")
        ai_play_together_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"),
                                         pos=(WIDTH_WINDOW // 2, 480),
                                         text_input="Máy với máy", font=get_font(48), base_color=base_color,
                                         hovering_color="White")
        back_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 630),
                             text_input="Quay lại", font=get_font(48), base_color=base_color, hovering_color="White")

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
                    self.set_status_screen(5)
                if back_button.checkForInput(mouse_pos):
                    self.set_status_screen()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def difficulty_level_play(self, surface, mouse_pos):
        """
        difficulty selection screen
        :param surface: current surface
        :param mouse_pos: current mouse position
        :return:
        """
        main_text = get_font(70).render("ULTIMATE TICTACTOE", True, "#545454")
        main_rect = main_text.get_rect(center=(WIDTH_WINDOW // 2, 80))
        surface.blit(main_text, main_rect)

        level_easy_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 180),
                                   text_input="Dễ", font=get_font(48), base_color=base_color,
                                   hovering_color="White")
        level_normal_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 330),
                                     text_input="Bình thường", font=get_font(48), base_color=base_color,
                                     hovering_color="White")
        level_difficult_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"),
                                        pos=(WIDTH_WINDOW // 2, 480),
                                        text_input="Khó", font=get_font(48), base_color=base_color,
                                        hovering_color="White")
        back_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 2, 630),
                             text_input="Quay lại", font=get_font(48), base_color=base_color,
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
        """
        play screen
        :param surface: current surface
        :param mouse_pos: current mouse position
        :return:
        """
        game = self.game
        game.render_screen_game(surface)

        play_again_button = Button(image=None,
                                   pos=(self.game.board.dims.size + self.game.board.margin + 160, HEIGHT_WINDOW - 100),
                                   text_input="Chơi lại", font=get_font(30), base_color=base_color,
                                   hovering_color="White")
        back_button = Button(image=None,
                             pos=(self.game.board.dims.size + self.game.board.margin + 160, HEIGHT_WINDOW - 50),
                             text_input="Quay lại", font=get_font(30), base_color=base_color,
                             hovering_color="White")

        for button in [play_again_button, back_button]:
            button.changeColor(mouse_pos)
            button.update(surface)

        game.run_ai()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_click_mouse()

                if play_again_button.checkForInput(mouse_pos):
                    self.game.restart()
                elif back_button.checkForInput(mouse_pos):
                    if game.game_mode == 0:
                        self.set_status_screen(1)
                    elif game.game_mode == 1:
                        self.set_status_screen(3)
                    elif game.game_mode == 2:
                        self.set_status_screen(5)
                elif game.playing and game.player_playing:
                    game.play_turn_click(mouse_pos[0], mouse_pos[1])

            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    def pick_AI_screen(self, surface, mouse_pos):
        """
        pick AI screen
        :param surface: current surface
        :param mouse_pos: current mouse position
        :return:
        """
        main_text = get_font(70).render("ULTIMATE TICTACTOE", True, "#545454")
        main_rect = main_text.get_rect(center=(WIDTH_WINDOW // 2, 80))
        surface.blit(main_text, main_rect)

        AI1_text = get_font(50).render("AI1", True, "#545454")
        AI1_rect = AI1_text.get_rect(center=(WIDTH_WINDOW // 2, 150))
        surface.blit(AI1_text, AI1_rect)

        AI2_text = get_font(50).render("AI2", True, "#545454")
        AI2_rect = AI2_text.get_rect(center=(WIDTH_WINDOW // 2, 350))
        surface.blit(AI2_text, AI2_rect)

        list_buttons = [
            [
                Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 4, 240),
                       text_input="minimax", font=get_font(48), base_color="Red" if active[0][0] else base_color,
                       hovering_color="Red"),
                Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW * 3 // 4, 240),
                       text_input="mcts", font=get_font(48), base_color="Red" if active[0][1] else base_color,
                       hovering_color="Red")
            ],
            [
                Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 4, 440),
                       text_input="minimax", font=get_font(48), base_color="Red" if active[1][0] else base_color,
                       hovering_color="Red"),
                Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW * 3 // 4, 440),
                       text_input="mcts", font=get_font(48), base_color="Red" if active[1][1] else base_color,
                       hovering_color="Red")
            ]
        ]

        back_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW // 4, 630),
                             text_input="Quay lại", font=get_font(48), base_color=base_color,
                             hovering_color="White")

        run_button = Button(image=pygame.image.load("Resourse/Image/Rect.png"), pos=(WIDTH_WINDOW * 3 // 4, 630),
                            text_input="Chơi", font=get_font(48), base_color=base_color,
                            hovering_color="White")

        for button in [back_button, run_button]:
            button.changeColor(mouse_pos)
            button.update(surface)

        for buttons in list_buttons:
            for button in buttons:
                button.changeColor(mouse_pos)
                button.update(surface)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sound_click_mouse()

                for idx_buttons in range(len(list_buttons)):
                    idx_changed = -1
                    buttons = list_buttons[idx_buttons]
                    for idx in range(len(buttons)):
                        button = buttons[idx]
                        if button.checkForInput(mouse_pos):
                            idx_changed = idx
                            break

                    if not idx_changed == -1:
                        for idx in range(len(buttons)):
                            active[idx_buttons][idx] = True if idx == idx_changed else False

                if run_button.checkForInput(mouse_pos):
                    activeAI = [0, 0]
                    for idx_AI in range(2):
                        for idx_type in range(len(active[idx_AI])):
                            if active[idx_AI][idx_type]:
                                activeAI[idx_AI] = idx_type
                    self.game = Game(2, activeAI[0] + 1, activeAI[1] + 1)
                    self.set_status_screen(4)

                if back_button.checkForInput(mouse_pos):
                    self.set_status_screen(1)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    # Main run
    main = Main()
    main.mainloop()
