"""
Spell checker.  Input validation is performed by auto_correct and input_words.

Routes:
GET /auto-correct/?link=<value>
POST /insert-words (with json)

"""

from flask import Flask, request, jsonify
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

    def query(self, word, min_dist=0, max_dist=MAX_DIST):
        similar_words = []
        for child in self.children:
            if (child[1] >= min_dist) and (child[1] <= max_dist):
                similar_words = similar_words + child[0].query(
                    word,
                    min_dist=child[1] - MAX_DIST,
                    max_dist=child[1] + MAX_DIST
                )
        if distance(self.word, word) <= MAX_DIST:
            return similar_words.append(self.word)
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

    # TODO: validate input

    input_list = input_json['links']
    return jsonify(closest_parent=insert_list(input_list, t))


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
