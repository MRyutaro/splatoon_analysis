# (どっちがピンチか: str = "default")

# initでread_jsonする。

class CheckConditions():
    def __init__(self):
        print("init")

    def read_json(self):
        print("json読みこみ")

    def check_conditons(self, pinch_team: str = "None"):
        icons = self.decide_icons_range()
        print(icons)

    def decide_icons_range(self):
        print("アイコンの範囲を決定")
