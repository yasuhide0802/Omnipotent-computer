"""searle_mind.py

A simple module expressing John Searle's perspective from *Mind, Brain, and Science*.
It offers a function answering the perennial question "Who am I?" using
Searle's "biological naturalism": mental states are caused by and realized in
neurobiological processes, though they cannot be reduced to mere programs.
"""

def searle_who_am_i() -> str:
    """Return a statement reflecting Searle's view of selfhood.

    The answer mirrors the idea that conscious experience is both caused by
    and realized in the brain's biology, while not being identical with any
    computational program.
    """
    return (
        "I am a conscious being, a biological organism whose brain's "
        "neurophysiology gives rise to subjective experience. My mind is "
        "grounded in the physical yet irreducible to a purely computational "
        "description."
    )


if __name__ == "__main__":
    print(searle_who_am_i())
