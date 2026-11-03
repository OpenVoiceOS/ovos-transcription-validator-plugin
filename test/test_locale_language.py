"""Each Spanish and Basque say_again line is written in its locale's language."""
import json
import re
import unittest
from importlib.resources import files
from pathlib import Path

# Common function words and the words these prompts use, by language. The
# two sets share no word.
SPANISH = {"lo", "la", "no", "de", "por", "favor", "siento", "puedes",
           "podrías", "repetir", "repetirlo", "pregunta", "eso", "para",
           "una", "más", "me", "te", "tu", "disculpa", "perdón", "capté"}
BASQUE = {"ez", "dut", "dezakezu", "barkatu", "errepika", "mesedez",
          "berriro", "hartu", "galdera", "esan", "zure", "ulertu", "galdu"}

LOCALES = {"es-ES": SPANISH, "es-es": SPANISH, "eu-ES": BASQUE, "eu-es": BASQUE}
TRANSLATIONS = {"es-es": SPANISH, "eu-es": BASQUE}


def _language_of(line: str) -> str:
    words = set(re.findall(r"\w+", line.lower()))
    spanish, basque = len(words & SPANISH), len(words & BASQUE)
    if spanish > basque:
        return "es"
    if basque > spanish:
        return "eu"
    return "unknown"


def _expected(markers: set) -> str:
    return "es" if markers is SPANISH else "eu"


class TestSayAgainLanguage(unittest.TestCase):

    def test_word_lists_are_disjoint(self):
        self.assertEqual(set(), SPANISH & BASQUE)

    def test_shipped_dialog_lines_match_the_locale(self):
        locale = files("ovos_transcription_validator") / "locale"
        for lang, markers in LOCALES.items():
            lines = (locale / lang / "say_again.dialog").read_text(
                encoding="utf-8").splitlines()
            self.assertTrue(lines)
            for line in lines:
                with self.subTest(lang=lang, line=line):
                    self.assertEqual(_expected(markers), _language_of(line))

    def test_translation_lines_match_the_locale(self):
        root = Path(__file__).resolve().parents[1] / "translations"
        for lang, markers in TRANSLATIONS.items():
            data = json.loads((root / lang / "dialogs.json").read_text(encoding="utf-8"))
            lines = data["say_again.dialog"]
            self.assertTrue(lines)
            for line in lines:
                with self.subTest(lang=lang, line=line):
                    self.assertEqual(_expected(markers), _language_of(line))


if __name__ == "__main__":
    unittest.main()
