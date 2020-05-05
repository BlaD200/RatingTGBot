import os
from json import load

from bot.localization.map import Map


def get_localize(lang: str):
    """
    Return dict with values localized for the given language if exist else raises :code:`ValueError`

    :param str lang: language for localizing. "ukr" for Ukrainian and "eng" for English
    :return: : Map object. dict accessible by dot notation
    :rtype: Map
    """
    with open("localization/strings.json", encoding='utf-8') as f:
        strings_dict = load(f)

    def get_dict(d):
        local_strings = {}
        for k, v in d.items():
            if type(v) is dict:
                if get_dict(v):
                    d[k] = v[lang]
                    local_strings[k] = v[lang]
                continue
            return True
        return

    get_dict(strings_dict)
    return Map(strings_dict)


if __name__ == '__main__':
    strings = get_localize("ukr")
    print(strings.edit)
