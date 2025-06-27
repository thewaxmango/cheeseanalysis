# states:   AWAITING_CODE, ANALYZING, PRESENTING, QUIT
# data:     AWAITING_CODE = {}
#           ANALYZING = {
#               completed_turns: int,
#               total_turns: int
#           }
#           PRESENTING = {
#               turn: int,
#               path: int,
#               page: int,
#               show_ghosts: bool
#           }

import blessed
from math import floor

class CheeseAnalyzer():
    term = blessed.Terminal()
    status = "AWAITING_CODE"
    data_pipe = {}

    def __init__(self):
        self.main()

    def main(self):
        with self.term.fullscreen():
            while self.status != "QUIT":
                print(self.term.enter_fullscreen, end='', flush=True)
                match self.status:
                    case "AWAITING_CODE":
                        self.awaiting_code()
                    case "ANALYZING":
                        self.analyzing()
                    case "PRESENTING":
                        return
                    case "ERROR":
                        return
                    case "QUIT":
                        return

    def write(self, arg):
        print(arg, end='', flush=True)

    def awaiting_code(self):
        width, height = self.term.width, self.term.height
        self.draw_full_box()

        # title
        title_text = "Enter Jstris replay code:"
        title_x = (width - len(title_text)) // 2
        title_y = height // 2 - 3
        self.write(self.term.move(title_y, title_x) + self.term.bold + title_text + self.term.normal)

        # text box
        tb_width = min(60|(width&1), width-10-(width&1))
        input_width = tb_width - 2
        input_x = (width - tb_width) // 2 + 1
        input_y = height // 2
        self.draw_box(input_x - 1, width - input_x, height // 2 - 1, height // 2 + 1)

        # hints
        hints_text = "[Ctrl+W] clear | [Enter] submit | [Esc] quit"
        hints_x = (width - len(hints_text)) // 2
        hints_y = height - 2
        self.write(self.term.move(hints_y, hints_x) + self.term.dim + hints_text + self.term.normal)

        active_text = ""

        def update_tb():
            self.write(self.term.move(input_y, input_x) + ' '*input_width)
            display_text = active_text
            if len(display_text) > input_width - 1:
                display_text = display_text[-input_width+1:]
            self.write(self.term.move(input_y, input_x) + display_text)
            self.write(self.term.move(input_y, input_x + min(len(display_text), input_width-1)))

        update_tb()

        with self.term.cbreak():
            while self.status == "AWAITING_CODE":
                key = self.term.inkey()
                match key.name:
                    case "KEY_ENTER":
                        if active_text.strip():
                            self.data_pipe["replay_code"] = active_text
                            self.status = "ANALYZING"
                    case "KEY_ESCAPE":
                        self.status = "QUIT"
                    case "KEY_BACKSPACE":
                        active_text = active_text[:-1]
                        update_tb()
                    case _:
                        if key == '\x17':
                            active_text = ""
                            update_tb()
                        elif key.isprintable():
                            active_text += key
                            update_tb()

    def analyzing(self):
        width, height = self.term.width, self.term.height
        self.draw_full_box()

        # progress bar 
        pb_width = min(60|(width&1), width-10-(width&1))
        pb_segs = pb_width - 2
        bar_x = (width - pb_width) // 2 + 1
        bar_y = height // 2
        self.draw_box(bar_x - 1, width - bar_x, height // 2 - 1, height // 2 + 1)

        # progress text
        pt_x2 = width - bar_x - 1

        def update_progress(completed, total):
            tasks_completed = completed
            tasks_total = total
            
            # text
            display_text = f"{completed}/{total} turns analyzed"
            text_x = pt_x2 + 1 - len(display_text)
            self.write(self.term.move(bar_y + 2, text_x) + display_text)

            # bars
            bars_to_show = completed * pb_segs // total
            bars_text = '█'*bars_to_show
            self.write(self.term.move(bar_y, bar_x) + bars_text)

        # hints
        hints_text = "[Esc] quit"
        hints_x = (width - len(hints_text)) // 2
        hints_y = height - 2
        self.write(self.term.move(hints_y, hints_x) + self.term.dim + hints_text + self.term.normal)

        update_progress(10, 32)

        # with self.term.cbreak():
        #     while self.status == "ANALYZING":


        self.term.inkey()
        self.status = "QUIT"

    # inclusive on x2, y2
    # x1 < x2, y1 < y2
    def draw_box(self, x1, x2, y1, y2):
        width = x2 - x1 + 1
        height = y2 - y1 + 1
        self.write(self.term.move(y1, x1) + '╭' + '─'*(width-2) + '╮')
        for y in range(y1+1, y2):
            self.write(self.term.move(y, x1) + '│' + self.term.move(y, x2) + '│')
        self.write(self.term.move(y2, x1) + '╰' + '─'*(width-2) + '╯')

    def draw_full_box(self):
        self.draw_box(0, self.term.width-1, 0, self.term.height-1)

if __name__ == "__main__":
    CheeseAnalyzer()

