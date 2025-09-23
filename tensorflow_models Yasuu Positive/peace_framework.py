"""Peace-focused framework for evaluating technology projects.

This module defines the :class:`PeaceFramework`, a lightweight helper that
captures a set of guiding principles aimed at ensuring technology remains
aligned with humanitarian goals.  The framework currently exposes two
capabilities:

* ``display_principles`` – prints the principles in a human friendly format.
* ``check_alignment`` – performs a keyword based screening of a project
  description to highlight potential militarised applications.

While the implementation is intentionally simple (it is effectively a
dictionary lookup followed by a keyword search), wrapping the behaviour inside
an object gives downstream users a structured entry point and keeps the door
open for richer logic in the future.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class PeaceFramework:
    """Container for peace promoting technology principles.

    The class stores a collection of high level principles and exposes helper
    methods for working with them.  ``principles`` can be overridden at
    instantiation time, enabling customisation in downstream projects.
    """

    principles: Dict[str, str] = field(default_factory=lambda: {
        "ethics": "Root all actions in humanity, fairness, and respect for life.",
        "transparency": "Ensure open, visible systems. No hidden militarization.",
        "repurpose": "Use technology for environment, health, and peace, not weapons.",
        "collaboration": "Build global cooperation, not arms races.",
        "education": "Teach technology as a tool for life, never destruction.",
    })

    def display_principles(self) -> None:
        """Prints the principles in a friendly, readable format."""

        print("\U0001F30D Peace Framework Principles:")
        for key, value in self.principles.items():
            print(f"- {key.capitalize()}: {value}")

    def check_alignment(self, project_description: str) -> str:
        """Flag potentially militarised projects via a keyword search.

        Args:
            project_description: A short natural language description of the
                project to evaluate.

        Returns:
            A user friendly message indicating whether the description triggered
            any of the keywords associated with military technology.
        """

        red_flags = ("weapon", "warfare", "missile", "combat", "military")
        lower_description = project_description.lower()
        for flag in red_flags:
            if flag in lower_description:
                return f"\u26a0\ufe0f Potential violation: project contains '{flag}'"
        return "\u2705 Project appears aligned with peace principles."


def main() -> None:
    """Demonstrate the :class:`PeaceFramework` in action."""

    framework = PeaceFramework()
    framework.display_principles()

    project1 = "AI system for renewable energy distribution"
    project2 = "Autonomous drone warfare system"

    print("\nChecking projects:")
    print("Project 1:", framework.check_alignment(project1))
    print("Project 2:", framework.check_alignment(project2))


if __name__ == "__main__":
    main()
