"""Unit tests for :mod:`peace_framework`."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

import unittest

from peace_framework import PeaceFramework


class PeaceFrameworkTest(unittest.TestCase):
    """Tests covering the behaviour of :class:`PeaceFramework`."""

    def setUp(self) -> None:
        self.framework = PeaceFramework()

    def test_principles_are_present(self) -> None:
        expected_keys = {"ethics", "transparency", "repurpose", "collaboration", "education"}
        self.assertEqual(expected_keys, set(self.framework.principles))

    def test_check_alignment_flags_military_terms(self) -> None:
        message = self.framework.check_alignment("Project with military drones")
        self.assertIn("Potential violation", message)
        self.assertIn("military", message)

    def test_check_alignment_passes_peaceful_project(self) -> None:
        message = self.framework.check_alignment("Solar microgrid for rural clinics")
        self.assertEqual("\u2705 Project appears aligned with peace principles.", message)

    def test_display_principles_prints_expected_output(self) -> None:
        with io.StringIO() as buffer, redirect_stdout(buffer):
            self.framework.display_principles()
            output = buffer.getvalue()

        self.assertIn("Peace Framework Principles", output)
        for key in self.framework.principles:
            self.assertIn(key.capitalize(), output)


if __name__ == "__main__":
    unittest.main()
