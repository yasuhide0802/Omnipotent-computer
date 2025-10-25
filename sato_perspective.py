# -*- coding: utf-8 -*-
"""View the world through Sato Yasuhide's golf-inspired lens."""

class SatoPerspective:
    def __init__(self, name="佐藤康秀"):
        self.name = name

    def beautiful_swing(self):
        """Imagine Seve Ballesteros's graceful strike."""
        print(f"{self.name}はセベ・バレステロスの美しいスイングを心に描きます")

    def smooth_power(self):
        """Channel Greg Norman's smooth power."""
        print(f"{self.name}はグレッグ・ノーマンのしなやかで力強いショットをイメージします")

    def short_game_mastery(self):
        """Recall Isao Aoki's deft short game."""
        print(f"{self.name}は青木功の小技を思い浮かべ、繊細なタッチを忘れません")

    def conclude_with_answer(self):
        """Arrive at a clear solution."""
        print(f"{self.name}は最終的に適切な答えを導き出します")


def main():
    viewer = SatoPerspective()
    viewer.beautiful_swing()
    viewer.smooth_power()
    viewer.short_game_mastery()
    viewer.conclude_with_answer()


if __name__ == "__main__":
    main()
