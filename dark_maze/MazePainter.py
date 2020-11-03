import math
import os

from PIL import Image


class MazePainter:
    def __init__(self):
        self.init = False
        pass

    def do_init(self):
        self.RES = os.path.dirname(__file__) + "/res"
        self.GPS = Image.open(self.RES + "/gps.png").convert("RGBA")
        self.PRINCESS = Image.open(self.RES + "/princess.png").convert("RGBA")
        self.WARRIOR = Image.open(self.RES + "/warrior.png").convert("RGBA")
        self.TILES = {
            0b0000: Image.open(self.RES + "/0000.png").convert("RGBA"),
            0b0001: Image.open(self.RES + "/0001.png").convert("RGBA"),
            0b0010: Image.open(self.RES + "/0010.png").convert("RGBA"),
            0b0011: Image.open(self.RES + "/0011.png").convert("RGBA"),
            0b0100: Image.open(self.RES + "/0100.png").convert("RGBA"),
            0b0101: Image.open(self.RES + "/0101.png").convert("RGBA"),
            0b0110: Image.open(self.RES + "/0110.png").convert("RGBA"),
            0b0111: Image.open(self.RES + "/0111.png").convert("RGBA"),
            0b1000: Image.open(self.RES + "/1000.png").convert("RGBA"),
            0b1001: Image.open(self.RES + "/1001.png").convert("RGBA"),
            0b1010: Image.open(self.RES + "/1010.png").convert("RGBA"),
            0b1011: Image.open(self.RES + "/1011.png").convert("RGBA"),
            0b1100: Image.open(self.RES + "/1100.png").convert("RGBA"),
            0b1101: Image.open(self.RES + "/1101.png").convert("RGBA"),
            0b1110: Image.open(self.RES + "/1110.png").convert("RGBA"),
            0b1111: Image.open(self.RES + "/1111.png").convert("RGBA"),
        }
        self.TILES_W = 72
        self.TILES_H = 72
        self.TILES_OFFSET = 28
        self.init = True

    def draw_maze(self, maze_data, horizon=2, row_size=14, col_size=14):
        if not self.init:
            self.do_init()
        map_data = maze_data["map"]
        player = maze_data["player"]
        location = player["location"]
        map_w = col_size * self.TILES_W
        map_h = row_size * self.TILES_H + self.TILES_OFFSET
        image_bg = Image.new("RGBA", (map_w, map_h), 255)
        for row in range(len(map_data)):
            for col in range(len(map_data[row])):
                col_data = map_data[row][col]
                key = col_data[0] << 3
                key += col_data[1] << 2
                key += col_data[2] << 1
                key += col_data[3]
                image_bg.paste(
                    self.TILES[key],
                    (col * self.TILES_W, row * self.TILES_H),
                    self.TILES[key]
                )
                if location[0] == row and location[1] == col:
                    # 绘制玩家
                    image_bg.paste(
                        self.WARRIOR,
                        (col * self.TILES_W, row * self.TILES_H),
                        self.WARRIOR
                    )

        # 绘制终点地标
        image_bg.paste(
            self.PRINCESS,
            ((col_size - 1) * self.TILES_W, (row_size - 1) * self.TILES_H),
            self.PRINCESS
        )

        # 根据镜头剪裁
        y = location[0]
        x = location[1]
        if x < horizon:
            x = horizon
        elif x >= col_size - 1 - horizon:
            x = col_size - 1 - horizon
        if y < horizon:
            y = horizon
        elif y >= row_size - 1 - horizon:
            y = row_size - 1 - horizon
        x1 = (x - horizon) * self.TILES_W
        y1 = (y - horizon) * self.TILES_H - self.TILES_OFFSET
        x2 = (x + 1 + horizon) * self.TILES_W
        y2 = (y + 1 + horizon) * self.TILES_H + self.TILES_OFFSET
        image_bg = image_bg.crop((x1, y1, x2, y2))

        # 绘制导航箭头
        if location[0] < row_size - horizon or location[1] < col_size - horizon:
            gps_radian = math.atan2(
                col_size - location[1], row_size - location[0])
            gps_rotate = 90 - gps_radian * 180 / math.pi
            gps = self.GPS.rotate(0 - gps_rotate)
            image_bg.paste(gps, (0, 0), gps)

        return image_bg


maze_painter = MazePainter()
