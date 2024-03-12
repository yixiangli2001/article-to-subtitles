import sys
from opencc import OpenCC
import re

hardPuncs = ["。", "！", "？", "；", "……", "：", "～"]  # replace with "\n"
softPuncs = ["，", "、"]  # replace with " "
removePatterns = [
    r'（[^）]*）',
    r'【[^】]*】',
    r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._,\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%,_\+.~#?&//=]*)'

]

cc = OpenCC('s2tw')


def main():
    try:
        with open("article.txt", "r") as file:
            article = file.read()
            article = cc.convert(article)  # convert to traditional chinese

            for p in removePatterns:
                article = deletePatterns(article, p)

            sentences = article.splitlines()  # split with "\n"

            # split by punctuations
            for punc in hardPuncs:
                sentences = hardSplitBy(sentences, punc)

            for punc in softPuncs:
                sentences = softSplitBy(sentences, punc)

            lines = cleanList(sentences)

    except FileNotFoundError:
        sys.exit("File Not Found")

    with open("subtitles.txt", "w") as fileAfter:
        for l in lines:
            fileAfter.write(l + "\n")


def cleanList(l: list) -> list:
    if isinstance(l, list):
        return list(filter(None, l))


def deletePatterns(s: str, p: str) -> str:
    if isinstance(s, str):
        return re.sub(p, "", s)


def hardSplitBy(li: list, punc: str) -> list:
    lines = []
    for s in li:
        temp = s.split(punc)
        for t in temp:
            lines.append(t)
    return cleanList(lines)


def softSplitBy(li: list, punc: str) -> list:
    finalList = []
    for l in li:
        linesSplitByComma = l.split(punc)

        newList = []
        currentStr = ""
        for line in linesSplitByComma:
            line = line.strip()
            if len(currentStr) + len(line) < 22:
                currentStr += " " + line
                currentStr = currentStr.strip()
            else:
                newList.append(currentStr)
                currentStr = line
        newList.append(currentStr)

        for i in newList:
            finalList.append(i)

    return cleanList(finalList)


if __name__ == "__main__":
    main()
