"""Peace Framework module.

This module defines a :class:`PeaceFramework` that encapsulates guiding
principles focused on ethical, transparent, and collaborative
applications of technology. It also provides a convenience function to
check whether a textual project description raises potential red flags
that suggest militarisation.

Running the module as a script prints the principles and optionally
checks user supplied project descriptions from the command line.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Dict, Iterable, List


@dataclass
class PeaceFramework:
    """Container for peace-first technology principles.

    Attributes
    ----------
    principles:
        Mapping of principle names to their descriptions. The defaults
        promote ethical, transparent, and collaborative uses of
        technology that benefit humanity.
    red_flags:
        Collection of keywords that indicate a project may contain
        militaristic or violent intent. The list can be customised if
        the calling code wishes to extend or relax the heuristic.
    """

    principles: Dict[str, str] = field(default_factory=lambda: {
        "ethics": "Root all actions in humanity, fairness, and respect for life.",
        "transparency": "Ensure open, visible systems. No hidden militarization.",
        "repurpose": "Use technology for environment, health, and peace, not weapons.",
        "collaboration": "Build global cooperation, not arms races.",
        "education": "Teach technology as a tool for life, never destruction.",
    })
    red_flags: Iterable[str] = (
        "weapon",
        "warfare",
        "missile",
        "combat",
        "military",
    )

    def display_principles(self) -> List[str]:
        """Return the formatted principles as a list of lines.

        Returning the lines instead of printing makes the function easier
        to re-use in other contexts, while the script entry-point can
        still print them for interactive users.
        """

        lines = ["🌍 Peace Framework Principles:"]
        for key, value in self.principles.items():
            lines.append(f"- {key.capitalize()}: {value}")
        return lines

    def check_alignment(self, project_description: str) -> str:
        """Assess whether a project description conflicts with the principles.

        The current implementation is intentionally simple: it performs a
        case-insensitive keyword search for any of the entries in
        :attr:`red_flags`. It can be replaced with a more sophisticated
        natural language processing model if required.
        """

        project_lower = project_description.lower()
        for flag in self.red_flags:
            if flag in project_lower:
                return f"⚠️ Potential violation: project contains '{flag}'"
        return "✅ Project appears aligned with peace principles."


def parse_arguments(args: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the peace framework script."""

    parser = argparse.ArgumentParser(
        description=(
            "Display the Peace Framework principles and optionally check "
            "project descriptions for potential militarisation."
        )
    )
    parser.add_argument(
        "projects",
        nargs="*",
        metavar="DESCRIPTION",
        help="Project description(s) to evaluate."
    )
    return parser.parse_args(args)


def main(cli_args: Iterable[str] | None = None) -> None:
    """Entry point for command-line execution."""

    args = parse_arguments(cli_args)
    framework = PeaceFramework()

    for line in framework.display_principles():
        print(line)

    if args.projects:
        print("\nChecking projects:")
        for description in args.projects:
            verdict = framework.check_alignment(description)
            print(f"- {description}: {verdict}")


if __name__ == "__main__":
    main()
