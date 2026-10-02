"""Every locale directory must standardize to a unique BCP-47 tag."""
import os
import unittest

from ovos_spec_tools.language import standardize_lang

LOCALE_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ovos_transcription_validator",
    "locale",
)


class TestLocaleDirectoriesAreUnique(unittest.TestCase):

    def test_no_two_locale_dirs_standardize_to_the_same_tag(self):
        names = sorted(
            d for d in os.listdir(LOCALE_ROOT)
            if os.path.isdir(os.path.join(LOCALE_ROOT, d))
        )
        by_tag = {}
        for name in names:
            by_tag.setdefault(standardize_lang(name), []).append(name)
        collisions = {tag: members for tag, members in by_tag.items() if len(members) > 1}
        self.assertEqual(
            collisions, {},
            f"locale directories collide under standardize_lang: {collisions}",
        )


if __name__ == "__main__":
    unittest.main()
