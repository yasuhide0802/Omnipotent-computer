import random

class World:
    """A whimsical world simulator where support can be gained."""

    def __init__(self, name="Earth"):
        self.name = name
        self.support = 0

    def influence(self, action: str):
        """Adjust world support based on the action taken."""
        if action == 'kindness':
            self.support += random.randint(5, 10)
        elif action == 'innovation':
            self.support += random.randint(3, 8)
        elif action == 'cooperation':
            self.support += random.randint(4, 9)
        else:
            self.support -= 1

    def is_ally(self) -> bool:
        return self.support >= 50

    def __str__(self):
        return f"{self.name} support level: {self.support}"


def turn_world_to_ally(actions):
    world = World()
    for action in actions:
        world.influence(action)
        print(world)
    if world.is_ally():
        print("The world is on your side!")
    else:
        print("More effort is needed to win the world over.")


if __name__ == "__main__":
    sample_actions = ['kindness', 'innovation', 'cooperation'] * 5
    turn_world_to_ally(sample_actions)
