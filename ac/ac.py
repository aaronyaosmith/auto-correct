"""
Spell checker.  Input validation is performed by auto_correct and input_words.

Levenshtein distance computation is performed by a third-party library called
python-Levenshtein.  It's available as a pip package!

Routes: GET /auto-correct/?link=<value> POST /insert-words (with json)
"""

from flask import Flask, request, jsonify, abort
from Levenshtein import distance

MAX_DIST = 2  # Words within this Levenshtein distance are defined as similar
app = Flask(__name__)


class SpellTree(object):
    """A tree that stores words.

    Can query for a list of words at a specified Levenshtein distance.
    """

    def __init__(self, word=None):
        self.word = word
        # children are (SpellTree, int) where the int is LS distance
        self.children = []

    def insert(self, word):
        """Returns parent of new node."""
        if self.word is None:
            self.word = word
            return 'none'
        if self.word == word:
            return 'not_inserted'
        else:
            dist = distance(word, self.word)
            for child in self.children:
                if child[1] == dist:
                    return child[0].insert(word)

            self.children.append((SpellTree(word), dist))
            return self.word

    def query(self, word):
        similar_words = []
        dist = distance(self.word, word)
        for child in self.children:
            if (child[1] >= dist - MAX_DIST) and (child[1] <= dist + MAX_DIST):
                similar_words = similar_words + child[0].query(word)
        if dist <= MAX_DIST:
            similar_words.append(self.word)
            return similar_words
        else:
            return similar_words


t = SpellTree()


@app.route('/auto-correct/', methods=['GET'])
def auto_correct():
    """GET /auto-correct/?link=<value> route.

    Takes query parameter 'link' and responds with JSON object containing all
    words <= 2 Levenshtein distance away from query in format:

    { "links": [“cuauv”,“chair”,...] }

    :returns: Flask JSON response (status=200, mimetype='application/json')

    :rtype: Flask.Response
    """
    global t

    link = request.args.get('link', '')

    return jsonify(links=find_neighbors(link, t))


@app.route('/insert-words', methods=['POST'])
def insert_words():
    """POST /insert-words route.

    Takes POST JSON request, inserts 'links' list of strings into our
    SpellTree, returns a JSON containing a list of parent nodes to the inserted
    words.  If word was not inserted, output string is 'not_inserted'.  If word
    does not have a parent, output string is 'none'.  Format:

    { “closest_parent”: [“none”,“cuair”,“cuair”,“plane”,“not_inserted”...] }

    :returns: Flask JSON response (status=200, mimetype='application/json')

    :rtype: Flask.Response
    """
    global t

    input_json = request.get_json()

    if valid_links(input_json) is False:
        return abort(400)

    input_list = input_json['links']
    return jsonify(closest_parent=insert_list(input_list, t))


@app.route('/')
def home():
    return "hi, you've reached Aaron Yao-Smith's project. Welcome!!"


def find_neighbors(word, tree):
    """Returns list of strings containing all words in tree of distance <= 2
    from query word.

    :param word: query word
    :param tree: SpellTree containing all possible words

    :returns: list of nearby words

    :rtype: string list
    """
    return tree.query(word)


def insert_list(lst, tree):
    """Inserts words into tree.  Returns list of closest parents as specifed in
    insert_words.

    :param lst: list of input words
    :param tree: SpellTree to insert to

    :returns: list of strings corresponding to closest parents of insert words

    :rtype: string list
    """
    output = []
    for word in lst:
        output.append(tree.insert(word))

    return output


def valid_links(links):
    """Determines validity of input link JSON.

    JSON must have a single entry 'links' which contains a list of strings.

    :param links: Dictionary representing input JSON
    :returns: True if valid, False if not
    :rtype: boolean

    """
    if type(links) is not dict:
        return False
    if len(links) is not 1:
        return False
    if 'links' not in links:
        return False
    if type(links['links']) is not list:
        return False
    if not list or not all(isinstance(s, str) for s in links['links']):
        return False
    return True
