def textFormater(text):
    level = 0
    text1 = ""
    type = "Main"
    _color = ""

    result = ""
    mode = 0
    translator = {"level": 0, "text": "", "class": "", "parametr": ""}
    colorita = {"level": 0, "text": "", "class": "", "parametr": ""}
    r = 0
    for s in text.splitlines():
        ii = -1
        for i in s:
            ii += 1
            if mode == 0:
                if "|" == i:
                    if r == 0:
                        print(s[ii + 1])
                        if s[ii + 1] == "|":
                            r = 1
                        else:
                            mode = 1
                            translator["level"] = 0
                    else:
                        r = 0
                        result += "||"

                elif "[" == i:
                    _color = ""
                    mode = 2
                else:
                    result += i
            if mode == 1:
                if "|" == i:

                    if translator["level"] == 0:
                        translator["level"] = 1
                        translator["class"] = "Main"
                        translator["parametr"] = ""
                    else:
                        if translator["class"] in self.LanguageDictFile["LanguageDict"]:
                            if translator["parametr"] in self.LanguageDictFile["LanguageDict"][translator["class"]]:
                                if self.saveDataFile["Settings"]["Language"] in \
                                        self.LanguageDictFile["LanguageDict"][translator["class"]][
                                            translator["parametr"]]:
                                    result += \
                                        self.LanguageDictFile["LanguageDict"][translator["class"]][
                                            translator["parametr"]][
                                            self.saveDataFile["Settings"]["Language"]]
                                    translator["level"] = 0
                        if translator["level"] != 0:
                            result += translator["parametr"]
                            translator["level"] = 0

                        translator["class"] = "Main"
                        translator["parametr"] = ""
                        mode = 0

                elif translator["level"] == 1:
                    if translator["parametr"] == "" and i == " ":
                        result += "| "
                        translator["level"] = 0
                    elif "." == i:
                        translator["level"] = 2
                        translator["class"] = translator["parametr"]
                        translator["parametr"] = ""
                    else:
                        translator["parametr"] += i
                elif translator["level"] == 2:
                    translator["parametr"] += i
            elif mode == 2:
                if i != "[" and i != "]":
                    _color += i
                if i == "[":
                    result += '<font color="'
                if i == "]":
                    if _color.upper()[:3] == "UI.":
                        if _color.upper()[3:] in self.MindustryColors["UI"]:
                            result += self.MindustryColors["UI"][_color.upper()[3:]]
                        else:
                            result += _color
                    elif _color.upper() in self.MindustryColors["ARC"]:
                        result += self.MindustryColors["ARC"][_color.upper()]
                    else:
                        result += _color
                    result += '">'
                    mode = 0

        result += "<br>"

    return result[:-4]