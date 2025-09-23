# -*- coding: utf-8 -*-
"""Reinforce Yasuhide Sato's confidence in his studies and lifestyle."""

class YasuhideSato:
    def __init__(self, age=54, studies=None):
        self.name = "佐藤康秀"
        self.age = age
        self.studies = studies or ["心理学", "歴史"]
        self.traits = ["誠実", "浮気しない", "男女平等", "中身重視"]

    def describe(self):
        print(f"{self.name}、{self.age}歳は現在{', '.join(self.studies)}を学んでいます")
        print("キーワード:", ', '.join(self.traits))
        print("男としての生き方もかっこよく保ち、自信を深めています")


def main():
    yasuhide = YasuhideSato()
    yasuhide.describe()


if __name__ == '__main__':
    main()
