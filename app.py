from flask import Flask, request, jsonify

t = SpellTree()
app = Flask(__name__)


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


@app.route('/insert-words', methods=['POST', 'GET'])
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
    return jsonify(closest_parent=insert_json(input_json, t))


def find_neighbors(word, tree):
    """Returns list of strings containing all words in tree of distance <= 2
    from query word.

    :param word: query word
    :param tree: SpellTree containing all possible words

    :returns: list of nearby words

    :rtype: string list
    """


def insert_json(json, tree):
    """Inserts strings in 'links' list in input json into tree.  Returns list
    of closest parents as specifed in insert_words.

    :param json: contains entry 'list' which has list of words
    :param tree: SpellTree to insert to

    :returns: list of strings corresponding to closest parents of insert words

    :rtype: string list
    """


class SpellTree(object):
    def __init__(self, word):
        self.word = word
        self.children = []
        self.distance = []

    def insert(self, word):
        raise Exception('Unimplemented')

    def query(self, word):
        raise Exception('Unimplemented')
