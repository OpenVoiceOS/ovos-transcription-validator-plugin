"""The installed package names its version and its plugin entry point, and
ships its locale dialogs."""
import unittest
from importlib.metadata import entry_points, version
from importlib.resources import files

from ovos_transcription_validator import TranscriptionValidatorPlugin
from ovos_transcription_validator import version as version_module


class TestPackaging(unittest.TestCase):

    def test_version_comes_from_the_version_block(self):
        block = (version_module.VERSION_MAJOR, version_module.VERSION_MINOR,
                 version_module.VERSION_BUILD, version_module.VERSION_ALPHA)
        expected = "{}.{}.{}".format(*block[:3]) + (f"a{block[3]}" if block[3] else "")
        self.assertEqual(expected, version_module.__version__)
        self.assertEqual(expected, version("ovos-transcription-validator-plugin"))

    def test_entry_point_loads_the_plugin(self):
        found = [ep for ep in entry_points(group="neon.plugin.text")
                 if ep.name == "ovos-transcription-validator-plugin"]
        self.assertEqual(1, len(found))
        self.assertIs(TranscriptionValidatorPlugin, found[0].load())

    def test_the_package_ships_the_locale_dialogs(self):
        # The setup.py wheel shipped one say_again.dialog in each of 24
        # locale directories. Run against an installed wheel, this fails when
        # the wheel leaves the package data out.
        locale = files("ovos_transcription_validator") / "locale"
        self.assertTrue(locale.is_dir())
        dialogs = [lang for lang in locale.iterdir()
                   if (lang / "say_again.dialog").is_file()]
        self.assertEqual(24, len(dialogs))


if __name__ == "__main__":
    unittest.main()
