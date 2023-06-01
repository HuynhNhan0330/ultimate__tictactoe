class Button():
    """
    Class button
    """

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        constructor
        :param image: image
        :param pos: position of the button
        :param text_input: text input
        :param font: font
        :param base_color: base color
        :param hovering_color: hovering color
        """
        self.image = image
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.xpos, self.ypos))
        self.text_rect = self.text.get_rect(center=(self.xpos, self.ypos))

    def update(self, screen):
        """
        Update button
        :param screen: current screen
        :return:
        """

        if self.image is not None:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """
        check input click
        :param position: position clicked
        :return:
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """
        change color maybe when hovering
        :param position: current position
        :return:
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
