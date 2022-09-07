# (どっちがピンチか: str = "default")


class CheckConditions():
    def __init__(self):
        print("init")
        self.icons_ranges = self.read_json()

    def read_json(self):
        print("json読みこみ")

    def check_conditons(self, pinch_team: str = "None") -> list:
        check_ranges = self.create_check_ranges(pinch_team)
        self.draw_icons(check_ranges)
        print("return sample -> [['ALIVE', 'ALIVE', 'ALIVE', 'ALIVE'], ['ALIVE', 'ALIVE', 'ALIVE', 'ALIVE']]")

    def decide_icons_range(self, pinch_team: str) -> list:
        print("アイコンの範囲を決定")
        # if文で条件分岐
        # return [[[]. []. []. []], [[], [], [], []]]の、3次元配列

    def create_check_ranges(self, pinch_team: str = "None") -> list:
        icons = self.decide_icons_range(pinch_team)
        print("4等分する")

    def draw_icons(self, check_ranges):
        print("iconの範囲を描画")
