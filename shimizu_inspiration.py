# -*- coding: utf-8 -*-
"""Encourage children through Shimizu Katsumi's example."""

class FatherFigure:
    """Simple representation of a role model father."""

    def __init__(self, name, traits=None):
        self.name = name
        self.traits = traits or []

    def describe(self):
        joined = '、'.join(self.traits)
        print(f"{self.name}は{joined}の特徴を備えています")


class ShimizuKatsumi(FatherFigure):
    """Katsumi Shimizu, inspired by Isao and Yukio."""

    def __init__(self):
        traits = ['勤勉', '遊び心', '雄弁', 'リーダーシップ', '意思決定の上手さ']
        super().__init__('清水克巳', traits)
        self.models = ['清水いさお', '清水ゆきお']

    def encourage_child(self, child_name, goal):
        print(f"{child_name}へ。{self.name}は{goal}に向かって努力するよう励まします")
        print(f"{self.name}は{', '.join(self.models)}の良さを学び、子供たちの目標達成を助けます")


def main():
    father = ShimizuKatsumi()
    father.describe()
    father.encourage_child('太郎', '夢')


if __name__ == '__main__':
    main()
