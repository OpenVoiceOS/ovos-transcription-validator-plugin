"""A language tag with no region picks the dialogs of its default region.

The default region is where the language first appeared and is still
spoken: English is en-GB and Portuguese is pt-PT.
"""
import os
import unittest
from collections import defaultdict
from unittest.mock import patch

import ovos_transcription_validator
from ovos_transcription_validator import TranscriptionValidatorPlugin

LOCALE = os.path.join(os.path.dirname(ovos_transcription_validator.__file__), "locale")


def _plugin(dialogs=None):
    plugin = TranscriptionValidatorPlugin.__new__(TranscriptionValidatorPlugin)
    if dialogs is None:
        plugin.dialogs = defaultdict(dict)
        plugin.load_dialogs()
    else:
        plugin.dialogs = {"say_again": dialogs}
    return plugin


def _lines(lang):
    with open(os.path.join(LOCALE, lang, "say_again.dialog"), encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


class TestBareTagDefaultRegion(unittest.TestCase):

    def test_bare_pt_picks_pt_pt_over_pt_br(self):
        plugin = _plugin({"pt-BR": ["br"], "pt-PT": ["pt"]})
        self.assertEqual(plugin.get_dialog("say_again", "pt"), "pt")

    def test_bare_en_picks_en_gb_over_en_us(self):
        plugin = _plugin({"en-US": ["us"], "en-GB": ["gb"]})
        self.assertEqual(plugin.get_dialog("say_again", "en"), "gb")

    def test_regional_tag_keeps_its_own_region(self):
        plugin = _plugin({"pt-PT": ["pt"], "pt-BR": ["br"]})
        self.assertEqual(plugin.get_dialog("say_again", "pt-BR"), "br")
        plugin = _plugin({"en-GB": ["gb"], "en-US": ["us"]})
        self.assertEqual(plugin.get_dialog("say_again", "en-US"), "us")

    def test_bare_pt_speaks_the_shipped_pt_pt_dialogs(self):
        self.assertNotEqual(_lines("pt-PT"), _lines("pt-BR"))
        plugin = _plugin()
        with patch("ovos_transcription_validator.random.choice", side_effect=list):
            self.assertEqual(set(plugin.get_dialog("say_again", "pt")), _lines("pt-PT"))


if __name__ == "__main__":
    unittest.main()
