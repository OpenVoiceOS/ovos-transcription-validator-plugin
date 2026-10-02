"""this script should run in every PR originated from @gitlocalize-app
TODO - before PR merge
"""

import json
from os.path import dirname
import os
from ovos_utils.bracket_expansion import expand_template
from ovos_utils.list_utils import flatten_list, deduplicate_list

locale = f"{dirname(dirname(__file__))}/ovos_transcription_validator/locale"
tx = f"{dirname(dirname(__file__))}/translations"


def resolve_lang_dir(lang):
    """Map a lowercase translations key to its locale directory.

    `translations/<lang>` keys are always lowercase. Writing to
    `locale/<lang.lower()>` unconditionally creates a case-variant sibling of
    an existing, canonically-cased directory (`ca-ES` vs `ca-es`) on every
    sync. Match the existing directory case-insensitively first, and fall
    back to a canonical BCP-47 form only for a language the locale tree does
    not carry yet.
    """
    existing = {d.lower(): d for d in os.listdir(locale)} if os.path.isdir(locale) else {}
    if lang in existing:
        return existing[lang]
    base, _, region = lang.partition("-")
    return f"{base}-{region.upper()}" if region else base


for lang in os.listdir(tx):
    lang_dir = resolve_lang_dir(lang)
    intents = f"{tx}/{lang}/intents.json"
    dialogs = f"{tx}/{lang}/dialogs.json"
    vocs = f"{tx}/{lang}/vocabs.json"
    regexes = f"{tx}/{lang}/regexes.json"

    if os.path.isfile(intents):
        with open(intents) as f:
            data = json.load(f)
        for fid, samples in data.items():
            if samples:
                samples = deduplicate_list(flatten_list([expand_template(s.strip())
                                                         for s in samples
                                                         if s and s.strip() != "[UNUSED]"]))  # s may be None
                if fid.startswith("/"):
                    p = f"{locale}/{lang_dir}{fid}"
                else:
                    p = f"{locale}/{lang_dir}/{fid}"
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(f"{locale}/{lang_dir}/{fid}", "w") as f:
                    f.write("\n".join(sorted(samples)))

    if os.path.isfile(dialogs):
        with open(dialogs) as f:
            data = json.load(f)
        for fid, samples in data.items():
            if samples:
                samples = deduplicate_list(flatten_list([expand_template(s.strip())
                                                         for s in samples
                                                         if s and s.strip() != "[UNUSED]"]))  # s may be None
                if fid.startswith("/"):
                    p = f"{locale}/{lang_dir}{fid}"
                else:
                    p = f"{locale}/{lang_dir}/{fid}"
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(f"{locale}/{lang_dir}/{fid}", "w") as f:
                    f.write("\n".join(sorted(samples)))

    if os.path.isfile(vocs):
        with open(vocs) as f:
            data = json.load(f)
        for fid, samples in data.items():
            if samples:
                samples = deduplicate_list(flatten_list([expand_template(s.strip())
                                                         for s in samples
                                                         if s and s.strip() != "[UNUSED]"]))  # s may be None
                if fid.startswith("/"):
                    p = f"{locale}/{lang_dir}{fid}"
                else:
                    p = f"{locale}/{lang_dir}/{fid}"
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(f"{locale}/{lang_dir}/{fid}", "w") as f:
                    f.write("\n".join(sorted(samples)))

