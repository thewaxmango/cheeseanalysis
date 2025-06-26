SPAWN_POS = {
    "I": (3, 19),
    "O": (4, 19),
    "T": (3, 19),
    "S": (3, 19),
    "Z": (3, 19),
    "J": (3, 19),
    "L": (3, 19)
}

# BLOCK_WIDTHS[ROTATION][BLOCK]
BLOCK_WIDTHS = (
    {"I": 4, "O": 2, "T": 3, "S": 3, "Z": 3, "J": 3, "L": 3},
    {"I": 1, "O": 2, "T": 2, "S": 2, "Z": 2, "J": 2, "L": 2},
    {"I": 4, "O": 2, "T": 3, "S": 3, "Z": 3, "J": 3, "L": 3},
    {"I": 1, "O": 2, "T": 2, "S": 2, "Z": 2, "J": 2, "L": 2},
)

# BLOCK_SHAPES[ROTATION][BLOCK] -> list of (x, y) offsets relative to bottom left of bounding box
BLOCK_SHAPES = (
    { # 0
        "I": ((0, 0), (1, 0), (2, 0), (3, 0)),
        "O": ((0, 0), (0, 1), (1, 0), (1, 1)),
        "T": ((0, 0), (1, 0), (1, 1), (2, 0)),
        "S": ((0, 0), (1, 0), (1, 1), (2, 1)),
        "Z": ((0, 1), (1, 0), (1, 1), (2, 0)),
        "J": ((0, 0), (0, 1), (1, 0), (2, 0)),
        "L": ((0, 0), (1, 0), (2, 0), (2, 1))
    },
    { # R
        "I": ((0, 0), (0, 1), (0, 2), (0, 3)),
        "O": ((0, 0), (0, 1), (1, 0), (1, 1)),
        "T": ((0, 0), (0, 1), (0, 2), (1, 1)),
        "S": ((0, 1), (0, 2), (1, 0), (1, 1)),
        "Z": ((0, 0), (0, 1), (1, 1), (1, 2)),
        "J": ((0, 0), (0, 1), (0, 2), (1, 2)),
        "L": ((0, 0), (0, 1), (0, 2), (1, 0))
    },
    { # 180
        "I": ((0, 0), (1, 0), (2, 0), (3, 0)),
        "O": ((0, 0), (0, 1), (1, 0), (1, 1)),
        "T": ((0, 1), (1, 0), (1, 1), (2, 1)),
        "S": ((0, 0), (1, 0), (1, 1), (2, 1)),
        "Z": ((0, 1), (1, 0), (1, 1), (2, 0)),
        "J": ((0, 1), (1, 1), (2, 0), (2, 1)),
        "L": ((0, 0), (0, 1), (1, 1), (2, 1))
    },
    { # L
        "I": ((0, 0), (0, 1), (0, 2), (0, 3)),
        "O": ((0, 0), (0, 1), (1, 0), (1, 1)),
        "T": ((0, 1), (1, 0), (1, 1), (1, 2)),
        "S": ((0, 1), (0, 2), (1, 0), (1, 1)),
        "Z": ((0, 0), (0, 1), (1, 1), (1, 2)),
        "J": ((0, 0), (1, 0), (1, 1), (1, 2)),
        "L": ((0, 2), (1, 0), (1, 1), (1, 2))
    },
)

__SPIN_EMPTY = ()
__SPIN_ZERO = ((0, 0))
__SPIN_ZLSJ_01 = ((1, -1), (0, -1), (0, 0), (1, -3), (0, -3))
__SPIN_T_01 = ((1, -1), (0, -1), (0, 0), (0, -3))
__SPIN_ZLSJ_03 = ((0, -1), (1, -1), (1, 0), (0, -3), (1, -3))
__SPIN_T_03 = ((0, -1), (1, -1), (1, 0), (1, -3))
__SPIN_ZLSJT_10 = ((-1, 1), (0, 1), (0, 0), (-1, 3), (0, 3))
__SPIN_ZLSJT_12 = ((-1, 0), (0, 0), (0, -1), (-1, 2), (0, 2))
__SPIN_ZLSJ_21 = ((1, 0), (0, 0), (0, 1), (1, -2), (0, -2))
__SPIN_T_21 = ((1, 0), (0, 0), (1, -2), (0, -2))
__SPIN_ZLSJ_23 = ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2))
__SPIN_T_23 = ((0, 0), (1, 0), (0, -2), (1, -2))
__SPIN_ZLSJT_30 = ((0, 1), (-1, 1), (-1, 0), (0, 3), (-1, 3))
__SPIN_ZLSJT_32 = ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2))
__SPIN_I_01 = ((2, -2), (0, -2), (3, -2), (0, -3), (3, 0))
__SPIN_I_03 = ((1, -2), (0, -2), (3, -2), (0, 0), (3, -3))
__SPIN_I_10 = ((-2, 2), (0, 2), (-3, 2), (0, 3), (-3, 0))
__SPIN_I_12 = ((-2, 1), (-3, 1), (0, 1), (-3, 3), (0, 0))
__SPIN_I_21 = ((2, -1), (3, -1), (0, -1), (3, -3), (0, 0))
__SPIN_I_23 = ((1, -1), (3, -1), (0, -1), (3, 0), (0, -3))
__SPIN_I_30 = ((-1, 2), (0, 2), (-3, 2), (0, 0), (-3, 3))
__SPIN_I_32 = ((-1, 1), (-3, 1), (0, 1), (-3, 0), (0, 3))
__SPIN_01 = {
    "I": __SPIN_I_01,
    "O": __SPIN_ZERO,
    "T": __SPIN_T_01,
    "S": __SPIN_ZLSJ_01,
    "Z": __SPIN_ZLSJ_01,
    "J": __SPIN_ZLSJ_01,
    "L": __SPIN_ZLSJ_01
}
__SPIN_03 = {
    "I": __SPIN_I_03,
    "O": __SPIN_ZERO,
    "T": __SPIN_T_03,
    "S": __SPIN_ZLSJ_03,
    "Z": __SPIN_ZLSJ_03,
    "J": __SPIN_ZLSJ_03,
    "L": __SPIN_ZLSJ_03
}
__SPIN_10 = {
    "I": __SPIN_I_10,
    "O": __SPIN_ZERO,
    "T": __SPIN_ZLSJT_10,
    "S": __SPIN_ZLSJT_10,
    "Z": __SPIN_ZLSJT_10,
    "J": __SPIN_ZLSJT_10,
    "L": __SPIN_ZLSJT_10
}
__SPIN_12 = {
    "I": __SPIN_I_12,
    "O": __SPIN_ZERO,
    "T": __SPIN_ZLSJT_12,
    "S": __SPIN_ZLSJT_12,
    "Z": __SPIN_ZLSJT_12,
    "J": __SPIN_ZLSJT_12,
    "L": __SPIN_ZLSJT_12
}
__SPIN_21 = {
    "I": __SPIN_I_21,
    "O": __SPIN_ZERO,
    "T": __SPIN_T_21,
    "S": __SPIN_ZLSJ_21,
    "Z": __SPIN_ZLSJ_21,
    "J": __SPIN_ZLSJ_21,
    "L": __SPIN_ZLSJ_21
}
__SPIN_23 = {
    "I": __SPIN_I_23,
    "O": __SPIN_ZERO,
    "T": __SPIN_T_23,
    "S": __SPIN_ZLSJ_23,
    "Z": __SPIN_ZLSJ_23,
    "J": __SPIN_ZLSJ_23,
    "L": __SPIN_ZLSJ_23
}
__SPIN_30 = {
    "I": __SPIN_I_30,
    "O": __SPIN_ZERO,
    "T": __SPIN_ZLSJT_30,
    "S": __SPIN_ZLSJT_30,
    "Z": __SPIN_ZLSJT_30,
    "J": __SPIN_ZLSJT_30,
    "L": __SPIN_ZLSJT_30
}
__SPIN_32 = {
    "I": __SPIN_I_32,
    "O": __SPIN_ZERO,
    "T": __SPIN_ZLSJT_32,
    "S": __SPIN_ZLSJT_32,
    "Z": __SPIN_ZLSJT_32,
    "J": __SPIN_ZLSJT_32,
    "L": __SPIN_ZLSJT_32
}
# KICKS[FROM][TO][BLOCK] -> list of kick offsets
KICKS = (
    (__SPIN_EMPTY, __SPIN_01, __SPIN_EMPTY, __SPIN_03),
    (__SPIN_10, __SPIN_EMPTY, __SPIN_12, __SPIN_EMPTY),
    (__SPIN_EMPTY, __SPIN_21, __SPIN_EMPTY, __SPIN_23),
    (__SPIN_30, __SPIN_EMPTY, __SPIN_32, __SPIN_EMPTY),
)

class TetSim():
    def __init__(self, fumen_field, active, hold, queue):
        # field[y][x] (upside down when printed)
        self.field = [list(row) for row in fumen_field] + [list("__________") for _ in range(25 - len(fumen_field))]
        self.active_piece = active
        self.active_pos = SPAWN_POS[active]
        self.active_rot = 0
        self.hold_piece = hold
        self.hold_available = True
        self.queue = list(queue)

    def __str__(self):
        field_str = "\n".join("".join(row) for row in self.field[19::-1])
        return (f"Active Piece: {self.active_piece} at {self.active_pos} (rot {self.active_rot})\n"
                f"Hold Piece: {self.hold_piece}\n"
                f"Queue: {self.queue}\n"
                f"Field:\n{field_str}")

    def export_pages(self, fumen_field, active_piece, hold_piece, queue, moves):
        # print(moves)
        # print(self)
        self.__init__(fumen_field, active_piece, hold_piece, queue)
        first_placement = None
        piece_loc = None
        # List[(piece, rot, x, y, hold, hold_available, queue, cleared_lines)]
        reconstruct_data = []
        for move in moves:
            # print(move)
            match move:
                case "hold":
                    self.hold()
                case "left":
                    self.left()
                case "right":
                    self.right()
                case "cw":
                    self.cw()
                case "ccw":
                    self.ccw()
                case "180":
                    raise Exception("Should not encounter 180 spins in blockfish analysis.")
                case "sd":
                    self.sd()
                case "hd":
                    self.sd()
                    if first_placement is None:
                        first_placement, piece_loc = self.handle_first_placement()
                    data = self.place_piece()
                    reconstruct_data.append(data)
                    # print(self)
        return first_placement, piece_loc, self.reconstruct_pages(reconstruct_data)

    def reconstruct_pages(self, data):
        pages = []
        field_temp = [row.copy() for row in self.field][:20]
        # use final field and reconstruction data
        for piece, rot, x, y, hold, hold_av, queue, cleared_lines in data[::-1]:
            # insert cleared lines
            for line_y, line in cleared_lines[19::-1]:
                field_temp.insert(line_y, line)
                field_temp.pop()
            # place ghost piece "a"
            mino_locs = BLOCK_SHAPES[rot][piece]
            for x_offset, y_offset in mino_locs:
                field_y = y + y_offset
                field_x = x + x_offset
                if field_y < 0 or field_x < 0 or field_x >= 10:
                    raise Exception(f"Invalid piece placement during reconstruction.\nLog:\n{str(self)}")
                field_temp[field_y][field_x] = 'a'
            # add page
            pages.append({
                "active_piece": piece,
                "hold_piece": hold,
                "hold_available": hold_av,
                "queue": queue,
                "rows": ["".join(row) for row in field_temp][::-1],
            })
            # place correct ghost piece
            for x_offset, y_offset in mino_locs:
                field_y = y + y_offset
                field_x = x + x_offset
                if field_y < 0 or field_x < 0 or field_x >= 10:
                    raise Exception(f"Invalid piece placement during reconstruction.\nLog:\n{str(self)}")
                    field_temp[field_y][field_x] = piece.lower()
        return pages[::-1]

    # true if collides or out of bounds
    def check_collision(self, field, block, new_pos, new_rot):
        mino_locs = BLOCK_SHAPES[new_rot][block]
        if new_pos[0] < 0 or new_pos[0] + BLOCK_WIDTHS[new_rot][block] > 10 or new_pos[1] < 0:
            return True
        for x, y in mino_locs:
            if field[new_pos[1] + y][new_pos[0] + x] != "_":
                return True
        return False

    def handle_first_placement(self):
        cols = "".join(list(map(str, range(self.active_pos[0],
                                           self.active_pos[0] + BLOCK_WIDTHS[self.active_rot][self.active_piece]))))
        return ((self.active_piece, self.active_rot, self.active_pos[0], self.active_pos[1]),
                f"{self.active_piece}-{cols}")

    def place_piece(self):
        piece, rot, x, y = self.active_piece, self.active_rot, self.active_pos[0], self.active_pos[1]
        hold, hold_av, queue = self.hold_piece, self.hold_available, "".join(self.queue)
        # place piece
        mino_locs = BLOCK_SHAPES[rot][piece]
        for x_offset, y_offset in mino_locs:
            field_y = y + y_offset
            field_x = x + x_offset
            if field_y < 0 or field_x < 0 or field_x >= 10:
                raise Exception(f"Invalid piece placement.\nLog:\n{str(self)}")
            self.field[field_y][field_x] = piece
        # move queue & update active piece
        if self.queue:
            self.active_piece = self.queue.pop(0)
            self.active_pos = SPAWN_POS[self.active_piece]
            self.active_rot = 0
        else:
            self.active_piece = None
        # reset hold availability
        self.hold_available = True
        cleared_lines = self.handle_clear_lines()
        return (piece, rot, x, y, hold, hold_av, queue, cleared_lines)

    def handle_clear_lines(self):
        cleared_lines = []
        for y in range(24, -1, -1):
            if all(cell != "_" for cell in self.field[y]):
                cleared_lines.append((y, self.field[y].copy()))
                self.field.pop(y)
                self.field.append(["_"]*10)
                y -= 1
        return cleared_lines

    def hold(self):
        if not self.hold_available:
            return False
        if self.hold_piece is None:
            self.hold_piece = self.active_piece
            if not self.queue:
                raise Exception(f"No more pieces in queue to hold.\nLog:\n{str(self)}")
            self.active_piece = self.queue.pop(0)
        else:
            self.active_piece, self.hold_piece = self.hold_piece, self.active_piece
        self.hold_available = False
        self.active_pos = SPAWN_POS[self.active_piece]
        self.active_rot = 0
        return True

    def left(self):
        new_pos = (self.active_pos[0] - 1, self.active_pos[1])
        if not self.check_collision(self.field, self.active_piece, new_pos, self.active_rot):
            self.active_pos = new_pos
            return True
        return False

    def right(self):
        new_pos = (self.active_pos[0] + 1, self.active_pos[1])
        if not self.check_collision(self.field, self.active_piece, new_pos, self.active_rot):
            self.active_pos = new_pos
            return True
        return False

    def cw(self):
        new_rot = (self.active_rot + 1) % 4
        # apply kick offsets
        kick_offsets = KICKS[self.active_rot][new_rot][self.active_piece]
        for kick in kick_offsets:
            new_pos = (self.active_pos[0] + kick[0], self.active_pos[1] + kick[1])
            if not self.check_collision(self.field, self.active_piece, new_pos, new_rot):
                self.active_pos = new_pos
                self.active_rot = new_rot
                return True
        return False

    def ccw(self):
        new_rot = (self.active_rot - 1) % 4
        # apply kick offsets
        kick_offsets = KICKS[self.active_rot][new_rot][self.active_piece]
        for kick in kick_offsets:
            new_pos = (self.active_pos[0] + kick[0], self.active_pos[1] + kick[1])
            if not self.check_collision(self.field, self.active_piece, new_pos, new_rot):
                self.active_pos = new_pos
                self.active_rot = new_rot
                return True
        return False

    def down(self):
        new_pos = (self.active_pos[0], self.active_pos[1] - 1)
        if not self.check_collision(self.field, self.active_piece, new_pos, self.active_rot):
            self.active_pos = new_pos
            return True
        return False

    def sd(self):
        while self.down():
            pass
        return True
