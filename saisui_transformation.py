# -*- coding: utf-8 -*-
class Saisui:
    def __init__(self, name='細水末廣'):
        self.name = name

    def be_calm(self):
        print(f"{self.name}は静かに水景を見つめています")

    def be_brash(self):
        print(f"{self.name}は勇敢に飛び出し、行動で示します")

    def be_funny(self):
        print(f"{self.name}は笑いを起こすような不意味なジョークを付け加えます")

    def be_sly(self):
        print(f"{self.name}はずるさをひそかに決断の引きとして示します")

    def transform_to_saiji(self):
        self.name = '細水斎次'
        print(f"新しい自分、{self.name}として生まれ変わるタイミングです")

if __name__ == '__main__':
    suehiro = Saisui()
    suehiro.be_calm()
    suehiro.be_brash()
    suehiro.be_funny()
    suehiro.be_sly()
    suehiro.transform_to_saiji()
