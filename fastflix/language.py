# -*- coding: utf-8 -*-
"""
gettext is an antique that uses a horrid folder structure,
proprietary format, and requires checking in binary files to git.

So here is an easy stand-in that is better in ways I care about.
"""
import os
from functools import lru_cache
from pathlib import Path

from appdirs import user_data_dir
from box import Box
from iso639 import Lang

from fastflix.resources import language_file

__all__ = ["t", "translate"]

config = Path(user_data_dir("FastFlix", appauthor=False, roaming=True)) / "fastflix.yaml"

try:
    language = Box.from_yaml(filename=config).language
except Exception as err:
    if not str(err).endswith("does not exist"):
        print("WARNING: Could not get language from config file")
    language = "eng"

language_data = Box.from_yaml(filename=language_file, encoding="utf-8")

if language not in ("deu", "eng", "fra", "ita", "spa", "zho"):
    print(f"WARNING: {language} is not a supported language, defaulting to eng")
    language = "eng"


@lru_cache(maxsize=2048)  # This little trick makes re-calls 10x faster
def translate(text):
    if text in language_data:
        if language in language_data[text]:
            return language_data[text][language]
    else:
        if os.getenv("DEVMODE", "").lower() in ("1", "true"):
            print(f'Cannot find translation for: "{text}"')
    return text


t = translate
