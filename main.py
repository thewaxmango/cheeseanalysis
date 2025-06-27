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
import asyncio
import json
from time import time_ns
from functools import lru_cache

from utils import code_to_json
from sim import BLOCK_SHAPES

def log(file="log.txt", arg="helloe"):
    with open(file, "a") as f:
        f.write(str(time_ns()) + " " + arg + "\n")

BASE_COLORS = {
    "I": (0, 255, 255),
    "O": (255, 255, 0),
    "T": (160, 0, 240),
    "S": (0, 255, 0),
    "Z": (255, 0, 0),
    "J": (0, 0, 255),
    "L": (255, 165, 0),
    "G": (200, 200, 200),
}

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
                        asyncio.run(self.analyzing())
                    case "PRESENTING":
                        self.presenting()
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
        title_text = "enter jstris cheese replay code:"
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
        hints_text = "[up] sample | [ctrl+w] clear | [enter] submit | [esc] quit"
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
                    case "KEY_UP":
                        self.data_pipe["replay_code"] = "N4IgxiBcoG5QzAOngGhAZwPYDMAuARAJ0wAcBJAEygBY0BzAQwFsBTAZVwcNygEYA2avAAM1AKwB2McPjwJ9ZiwCiAOyqQBQ0ZLFjestOhYt1IEgCthTANYg0TPgE5+-YY7QAjdFHcYWUYTQKBm9IRwAONEIAgF8gqBAAQUT0AGk6RIB1JQyAGQBhakSAMQALAFVE-IB3AEtEgCEATSbktIzsgEVE3PwGxIBPazZ8zLYxJk6VVIBxFnQxfl5SgDkGgHlrAFlEzoBqACUAKTJrMSVyhgpMzIAbOgAPAA1EgDU6a0zCFTAACVeBuVfgAmJ6lBqZTorMTYawqfL5WrlACOqWsyOKLAArrgPPlSrhcOs9g9wsV+A9nkdEhRik9eI4niF1vhahI2NgAF7ImAkYp7azJax0NgHfCdJSdXAPA7CYrCJQUMADfJ0MjAsC3A5sFTVVJ7MCJAC8IBiQA"
                        self.status = "ANALYZING"
                    case _:
                        if key == '\x17':
                            active_text = ""
                            update_tb()
                        elif key.isprintable():
                            active_text += key
                            update_tb()

    async def analyzing(self):
        width, height = self.term.width, self.term.height
        self.draw_full_box()

        pb_width = min(60|(width&1), width-10-(width&1))
        pb_segs = pb_width - 2
        bar_x = (width - pb_width) // 2 + 1
        bar_y = height // 2
        self.draw_box(bar_x - 1, width - bar_x, height // 2 - 1, height // 2 + 1)

        pt_x2 = width - bar_x - 1

        progress = [0, 1]
        cancelled = False

        def update_progress(completed, total):
            progress[0] = completed
            progress[1] = total
            # text
            display_text = f"{completed}/{total} turns analyzed"
            display_progress(display_text)
            # bars
            bars_to_show = completed * pb_segs // total
            bars_text = '█'*bars_to_show
            self.write(self.term.move(bar_y, bar_x) + bars_text)

        def display_progress(display_text):
            text_x = pt_x2 + 1 - len(display_text)
            self.write(self.term.move(bar_y + 2, text_x) + display_text)

        display_progress("initializing...")

        def cancel_flag():
            return cancelled

        hints_text = "[esc] cancel"
        hints_x = (width - len(hints_text)) // 2
        hints_y = height - 2
        self.write(self.term.move(hints_y, hints_x) + self.term.dim + hints_text + self.term.normal)

        with self.term.hidden_cursor(), self.term.cbreak():
            analysis_task = asyncio.create_task(
                code_to_json(
                    self.data_pipe["replay_code"],
                    cancel_flag,
                    update_progress
                )
            )

            while not analysis_task.done():
                key = self.term.inkey(timeout=0.05)
                if key and key.name == "KEY_ESCAPE":
                    cancelled = True
                    self.status = "AWAITING_CODE"
                    analysis_task.cancel()
                    try:
                        await analysis_task
                    except asyncio.CancelledError:
                        pass
                    return
                await asyncio.sleep(0.05)

            try:
                self.data_pipe["analysis"] = await analysis_task
            except asyncio.CancelledError:
                return

            # with open("log.json", "w") as f:
            #     f.write(json.dumps(self.data_pipe["analysis"], indent=4, ensure_ascii=False))

            self.status = "PRESENTING"

    def presenting(self):
        width, height = self.term.width, self.term.height
        self.draw_full_box()
        center_x = width // 2
        center_y = height // 2

        # tetris board
        board_x = center_x - 38
        board_y = center_y - 11
        self.draw_tetris_box(board_x, board_y)

        # table
        table_x = center_x + 12
        table_y = board_y
        # cols: rank, score, current
        self.write(self.term.move(table_y + 1, table_x + 2) + "rank")
        self.write(self.term.move(table_y + 1, table_x + 9) + "score")
        self.write(self.term.move(table_y + 1, table_x + 17) + "current")

        # hints
        hints_text1 = "[left] prev turn | [right] next turn | [up] table up | [down] table down"
        hints_text2 = "[z] prev page | [x] next page | [c] toggle ghosts | [esc] new replay"
        hints_x1 = (width - len(hints_text1)) // 2
        hints_x2 = (width - len(hints_text2)) // 2
        hints_y1 = height - 3
        hints_y2 = height - 2
        self.write(self.term.move(hints_y1, hints_x1) + self.term.dim + hints_text1 + self.term.normal)
        self.write(self.term.move(hints_y2, hints_x2) + self.term.dim + hints_text2 + self.term.normal)

        # state
        show_ghosts = False
        data = self.data_pipe["analysis"]
        turn = 0
        turn_count = data["turn_count"]
        path = data["turns"][turn]["path_taken"]
        path_taken = data["turns"][turn]["path_taken"]
        path_count = data["turns"][turn]["path_count"]
        page = 0
        page_count = data["turns"][turn]["paths"][path]["page_count"]
        page_data = data["turns"][turn]["paths"][path]["pages"][page]

        def reset_page():
            nonlocal page, page_count, page_data
            page = 0
            page_count = data["turns"][turn]["paths"][path]["page_count"]
            page_data = data["turns"][turn]["paths"][path]["pages"][page]

        def reset_path():
            nonlocal path, path_taken, path_count
            path = data["turns"][turn]["path_taken"]
            path_taken = data["turns"][turn]["path_taken"]
            path_count = data["turns"][turn]["path_count"]
            reset_page()

        accuracy = data["accuracy"] * 100
        self.write(self.term.move(table_y - 1, table_x + 1) + f"total accuracy [{accuracy:.1f}%]")

        def update_board():
            self.update_tetris(board_x,
                               board_y,
                               page_data["active_piece"],
                               page_data["hold_piece"],
                               page_data["hold_available"],
                               page_data["queue"],
                               page_data["rows"],
                               show_ghosts=show_ghosts)

        def update_state_labels():
            # turn at top
            turn_text = f"    turn [{turn+1}/{turn_count}]    "
            turn_x = (width - len(turn_text)) // 2
            turn_y = 1
            self.write(self.term.move(turn_y, turn_x) + turn_text + self.term.normal)
            # page num above field
            page_text = f"  page [{page+1}/{page_count}]"
            self.write(self.term.move(board_y-1, board_x+32-len(page_text)) + page_text)
            # ghosts below field
            ghosts_text = f" ghosts [{'on' if show_ghosts else 'off'}]"
            self.write(self.term.move(board_y+22, board_x+32-len(ghosts_text)) + ghosts_text)
            # path indicator
            self.clear_box(table_x - 2, table_x - 1, table_y, height - 4)
            self.write(self.term.move(table_y + 3 + path, table_x - 2) + ">>")

        # table, based on state
        def update_path_table():
            self.clear_box(table_x, table_x + 25, table_y + 3, height - 4)
            self.draw_table([table_x, table_x + 7, table_x + 15, table_x + 25],
                            [table_y, table_y + 2, table_y + path_count + 3])
            for i in range(path_count):
                y = table_y + 3 + i
                rank_text = ('★ ' if i == path_taken else '') + str(i+1)
                self.write(self.term.move(y, table_x + 5 - len(rank_text)) + rank_text)
                score_text = str(data["turns"][turn]["paths"][i]["score"])
                self.write(self.term.move(y, table_x + 13 - len(score_text)) + score_text)
                current_text = str(data["turns"][turn]["paths"][i]["piece_loc"])
                self.write(self.term.move(y, table_x + 23 - len(current_text)) + current_text)

        def update_all():
            update_state_labels()
            update_path_table()
            update_board()

        update_all()

        with self.term.hidden_cursor(), self.term.cbreak():
            while self.status == "PRESENTING":
                key = self.term.inkey()
                match key.name:
                    case "KEY_LEFT":
                        if turn > 0:
                            turn -= 1
                            reset_path()
                            update_all()
                    case "KEY_RIGHT":
                        if turn < turn_count - 1:
                            turn += 1
                            reset_path()
                            update_all()
                    case "KEY_UP":
                        if path > 0:
                            path -= 1
                            reset_page()
                            update_state_labels()
                            update_board()
                    case "KEY_DOWN":
                        if path < path_count - 1:
                            path += 1
                            reset_page()
                            update_state_labels()
                            update_board()
                    case "KEY_ESCAPE":
                        self.status = "AWAITING_CODE"
                    case _:
                        if key == 'z':
                            if page > 0:
                                page -= 1
                                page_data = data["turns"][turn]["paths"][path]["pages"][page]
                                update_state_labels()
                                update_board()
                        elif key == 'x':
                            if page < page_count - 1:
                                page += 1
                                page_data = data["turns"][turn]["paths"][path]["pages"][page]
                                update_state_labels()
                                update_board()
                        elif key == 'c':
                            show_ghosts = not show_ghosts
                            update_state_labels()
                            update_board()

    def draw_tetris_box(self, x1, y1):
        # hold
        self.draw_box(x1, x1+11, y1, y1+5)
        # field
        self.draw_box(x1+11, x1+32, y1, y1+21)
        # next
        self.draw_box(x1+32, x1+43, y1, y1+17)
        # intersections
        self.write(self.term.move(y1, x1+11) + '┬')
        self.write(self.term.move(y1, x1+32) + '┬')
        self.write(self.term.move(y1+5, x1+11) + '┤')
        self.write(self.term.move(y1+17, x1+32) + '├')

    def update_tetris(self, x1, y1, active, hold, hold_available, queue, rows, show_ghosts=False):
        self.clear_box(x1+1, x1+10, y1+1, y1+4)
        self.clear_box(x1+12, x1+31, y1+1, y1+20)
        self.clear_box(x1+33, x1+42, y1+1, y1+16)
        self.clear_box(x1+12, x1+19, y1-2, y1-1)
        # hold
        if hold:
            hold_x = x1 + 1
            hold_y = y1 + 1
            self.draw_block(hold_x, hold_y, hold, gray=(not hold_available))
        # queue
        queue_x = x1 + 33
        queue_y_base = y1 + 1
        for i, block in enumerate(queue[:5]):
            self.draw_block(queue_x, queue_y_base + i * 3, block)
        # board
        board_x_base = x1 + 12
        board_y_base = y1 + 1
        for r, row in enumerate(rows):
            for c, mino in enumerate(row):
                ch = "█"
                shade = 0
                if mino == 'a':
                    mino = active
                    shade = 1
                elif mino.islower():
                    mino = mino.upper()
                    ch = "░" if show_ghosts else " "
                    shade = 2
                elif mino == "_":
                    ch = " "
                self.draw_mino(board_x_base + 2 * c, board_y_base + r, ch, mino, shade)
        # active
        self.draw_block(x1 + 12, y1-3, active, fill=1, shade=1, centered=False)

    # fill : [█, ▓, ▒, ░]
    # shade: 0 to 2
    def draw_block(self, x1, y1, block, centered=True, gray=False, fill=0, shade=0):
        if block == "_":
            return
        offsets = BLOCK_SHAPES[0][block]
        y2 = y1 + 2
        if centered:
            match block:
                case "I":
                    x1 += 1
                case "O":
                    x1 += 3
                case _:
                    x1 += 2
        ch = "█▓▒░ "[fill]
        for x_off, y_off in offsets:
            self.draw_mino(x1 + 2*x_off, y2 - y_off, ch, block, shade)

    def draw_mino(self, x, y, ch, block, shade):
        self.write(self.term.move(y, x) + self.get_color(block, shade) + ch*2 + self.term.normal)

    @lru_cache
    def get_color(self, block, shade):
        if block == "_":
            return self.term.normal
        color = BASE_COLORS[block]
        match shade:
            case 1:
                color = tuple(int(c * 0.7) for c in color)
            case 2:
                color = tuple(int(c * 0.4) for c in color)
        return self.term.color_rgb(*color)

    # inclusive on x2, y2
    # x1 < x2, y1 < y2
    def draw_box(self, x1, x2, y1, y2):
        width = x2 - x1 + 1
        self.write(self.term.move(y1, x1) + '╭' + '─'*(width-2) + '╮')
        for y in range(y1+1, y2):
            self.write(self.term.move(y, x1) + '│' + self.term.move(y, x2) + '│')
        self.write(self.term.move(y2, x1) + '╰' + '─'*(width-2) + '╯')

    def clear_box(self, x1, x2, y1, y2):
        for y in range(y1, y2+1):
            self.write(self.term.move(y, x1) + ' '*(x2-x1+1))

    def draw_full_box(self):
        self.draw_box(0, self.term.width-1, 0, self.term.height-1)

    def draw_table(self, xs, ys):
        self.draw_box(xs[0], xs[-1], ys[0], ys[-1])
        for x in xs[1:-1]:
            self.write(self.term.move(ys[0], x) + '┬')
            self.write(self.term.move(ys[-1], x) + '┴')
            for y in range(ys[0] + 1, ys[-1]):
                self.write(self.term.move(y, x) + '│')
        for y in ys[1:-1]:
            self.write(self.term.move(y, xs[0]) + '├' + '─'*(xs[-1]-xs[0]-1) + '┤')
            for x in xs[1:-1]:
                self.write(self.term.move(y, x) + '┼')

if __name__ == "__main__":
    CheeseAnalyzer()

