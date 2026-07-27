import cv2


class Dropdown:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        options: list[str],
        selected_index: int = 0,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.selected_index = selected_index
        self.is_open = False

    def handle_click(self, mouse_x: int, mouse_y: int) -> None:
        inside_header = (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

        if inside_header:
            self.is_open = not self.is_open
            return

        if self.is_open:
            for index in range(len(self.options)):
                option_y = self.y + self.height * (index + 1)

                inside_option = (
                    self.x <= mouse_x <= self.x + self.width
                    and option_y <= mouse_y <= option_y + self.height
                )

                if inside_option:
                    self.selected_index = index
                    self.is_open = False
                    return

        self.is_open = False

    def draw(self, frame, label: str) -> None:
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(
            frame,
            label,
            (self.x, self.y - 8),
            font,
            0.6,
            (255, 255, 255),
            2,
        )

        cv2.rectangle(
            frame,
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            (35, 35, 35),
            -1,
        )

        cv2.rectangle(
            frame,
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            (255, 255, 255),
            2,
        )

        selected_text = self.options[self.selected_index]

        cv2.putText(
            frame,
            selected_text,
            (self.x + 10, self.y + 28),
            font,
            0.7,
            (255, 255, 255),
            2,
        )

        arrow_x = self.x + self.width - 20
        arrow_y = self.y + self.height // 2

        cv2.line(
            frame,
            (arrow_x - 5, arrow_y - 3),
            (arrow_x, arrow_y + 3),
            (255, 255, 255),
            2,
        )
        cv2.line(
            frame,
            (arrow_x, arrow_y + 3),
            (arrow_x + 5, arrow_y - 3),
            (255, 255, 255),
            2,
        )

        if not self.is_open:
            return

        for index, option in enumerate(self.options):
            option_y = self.y + self.height * (index + 1)

            if index == self.selected_index:
                background = (70, 100, 70)
            else:
                background = (35, 35, 35)

            cv2.rectangle(
                frame,
                (self.x, option_y),
                (self.x + self.width, option_y + self.height),
                background,
                -1,
            )

            cv2.rectangle(
                frame,
                (self.x, option_y),
                (self.x + self.width, option_y + self.height),
                (255, 255, 255),
                1,
            )

            cv2.putText(
                frame,
                option,
                (self.x + 10, option_y + 28),
                font,
                0.7,
                (255, 255, 255),
                2,
            )