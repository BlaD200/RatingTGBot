import os
from json import load

from bot.localization.map import Map


def get_localize(lang: str) -> Map:
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


def get_localization_list(key):
    with open("localization/strings.json", encoding='utf-8') as f:
        strings_dict = load(f)

    res = []
    for k, v in strings_dict.items():
        if k == key:
            if type(v) is dict:
                for val in v.values():
                    res.append(val)
                return res.copy()
    raise ValueError("Given key '{key}' could not be found.".format(key=key))


if __name__ == '__main__':
    strings = get_localize("ukr")
    print(strings.edit)
    print()
    print(get_localization_list('back'))
    print(get_localization_list('exit'))
