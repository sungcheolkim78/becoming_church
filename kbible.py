import pandas as pd
import yaml


def read_bible(version_name):
    """ read bible text and return panda database """

    filename="raw_bible_text/" + version_name + ".txt"
    with open(filename, "r") as f:
        lines = f.readlines()

    # prepare data container
    books = []
    chapters = []
    verses = []
    texts = []

    for line in lines:
        line = line.strip('\n\r')

        # check comment line
        if len(line) == 0:
            continue
        if line[0] == "#":
            continue

        # find header
        hp = line.find(' ')
        if hp > 1 and hp < 10:
            header = line[:hp]
            text = line[hp+1:]

            # find book, chapter, verse, text
            tmp = header.split(':')[0]
            chapter = ''.join(filter(str.isdigit, tmp))
            verse = header.split(':')[1]
            book = ''.join(filter(str.isalpha, tmp))

            # convert data
            try:
                verse = int(verse)
                chapter = int(chapter)
            except:
                print("... parser error! - {}".format(line))

            # collect
            books.append(book)
            chapters.append(chapter)
            verses.append(verse)
            texts.append(text)
        else:
            print("... parser error! - {}".format(line))

    df_bible = {'book':books, 'chapter':chapters, 'verse':verses, 'text':texts}
    idx = range(len(books))
    bible = pd.DataFrame(data=df_bible, index=idx)

    return bible


def read_full_bible(version_name, save=False):
    """ read bible version """

    try:
        full_bible = pd.read_csv("raw_bible_text/"+version_name+".csv.gz", index_col=0, compression = "gzip")
        return full_bible
    except FileNotFoundError:
        print('... generate bible database')

    bible = read_bible(version_name)
    table = pd.read_csv("raw_bible_text/목록표.csv", index_col=0)

    full_bible = pd.merge(bible1, table, on='book', how='left')

    if save:
        full_bible.to_csv("raw_bible_text/{}.csv.gz".format(version_name), compression='gzip')

    return full_bible

def find_id(bible, book=[], chapter=[], verse=[], verb=False):
    """ find index on full bible database """

    # check books
    books = set(bible['book'])
    books_long = set(bible['book_long'])

    if len(book) == 0:
        book = books[0]
    if isinstance(book, str):
        book = [book]

    if verb: print('... search book:{}'.format(book))
    result = bible.loc[bible.book.isin(book) | bible.book_long.isin(book)]

    # check chapter
    if isinstance(chapter, int):
        chapter = [chapter]
    if len(chapter) == 0:
        return result

    if verb: print('... search chapter: {}'.format(chapter))
    result = result.loc[bible.chapter.isin(chapter)]

    # check verse
    if isinstance(verse, int):
        verse = [verse]
    if len(verse) == 0:
        return result

    if verb: print('... search verse: {}'.format(verse))
    result = result.loc[bible.verse.isin(verse)]

    if len(result) > 0:
        return result
    else:
        print("... not found: {}, {}, {}".format(book, chapter, verse))
        return []


def extract_bystr(bible, sstr, form="pd"):
    """ extract verse by short search string
    sstr: "창3:16", "고후5:3", '요일1:1'
    - no space
    - one separator
    """

    # remove all spaces
    sstr = sstr.replace(" ", "")

    # find components
    verses = sstr.split(':')[1]
    head = sstr.split(':')[0]

    book = ''.join(filter(str.isalpha, head))
    chapter = ''.join(filter(str.isdigit, head))
    chapter = int(chapter)

    # check , in verse
    if verses.find(',') > 0:
        verses = verses.split(',')
    # check - in verse
    elif verses.find('-') > 0:
        start = verses.split('-')[0]
        end = verses.split('-')[1]
        try:
            verses = list(range(int(start), int(end)+1))
        except:
            print('... wrong format: {}'.format(sstr))
            return 0

    verses = [int(v) for v in verses]

    #print(book, chapter, verses)

    # return verses
    res = find_id(bible, book=book, chapter=chapter, verse=verses)
    if len(res) == 0:
        return []

    if form == "pd":
        return res
    if form == "string":
        return '. '.join(res['text'].values)
    if form == "md":
        msg = "`{}` ".format(sstr)
        return msg + '. '.join(res['text'].values)


def make_mdpage(bible, day_info, save=False):
    """ print all verses in list using markdown format """

    # check day_info.yml file
    if isinstance(day_info, str):
        try:
            with open(day_info, "r") as f:
                day_info = yaml.load(f, yaml.BaseLoader)
        except:
            print("... file: {} parser error!".format(day_info))
            return 0

    bible_version = ""
    # check bible version
    if isinstance(bible, str):
        try:
            bible_version = "-" + bible
            bible = read_full_bible(bible)
        except:
            print("... read error: {}".format(bible_version[1:]))
            return 0

    msg = "# {}일차 - {}\n\n".format(day_info["day"],day_info["title"])
    msg = msg + "찬양 : {}\n\n".format(day_info["song"])
    msg = msg + "기도 : {}\n\n".format(day_info["prayer"])
    msg = msg + "요약 : {}\n\n".format(day_info["summary"])
    msg = msg + "성경 버전 : {}\n\n".format(bible_version[1:])

    for v in day_info["verses"]:
        msg = msg + '- {}\n\n'.format(extract_bystr(bible, v, form="md"))

    msg = msg + "### info\n\n"
    msg = msg + "- 성경 구절 갯수 : {}".format(len(day_info["verses"]))

    if save:
        filename = 'mpages/day{}-{}{}.md'.format(day_info["day"], day_info["title"].replace(" ", ""), bible_version)
        with open(filename, "w") as f:
            f.write(msg)
        print('... save to {}'.format(filename))

    return msg
