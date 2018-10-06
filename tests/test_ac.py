from ac import ac


def test_given():
    with ac.app.test_client() as c:
        rv = c.post('/insert-words', json={
            'links': ['cuair', 'fair', 'plane', 'place', 'cuair']
        })
        assert rv.get_json()['closest_parent'] == [
            'none', 'cuair', 'cuair', 'plane', 'not_inserted'
        ]

        rv = c.get('/auto-correct/?link=playne')
        assert set(rv.get_json()['links']) == set(['plane', 'place'])
        rv = c.get('/auto-correct/?link=definitelynotaplane')
        assert rv.get_json()['links'] == []


def test_already_inserted():
    with ac.app.test_client() as c:
        c.post('/insert-words', json={
            'links': ['cuair', 'fair', 'plane', 'place', 'cuair']
        })
        rv = c.post('/insert-words', json={
            'links': ['cuair', 'fair', 'plane', 'place', 'cuair']
        })
        assert rv.get_json()['closest_parent'] == [
            'not_inserted', 'not_inserted', 'not_inserted',
            'not_inserted', 'not_inserted'
        ]


def test_add_more():
    with ac.app.test_client() as c:
        rv = c.post('/insert-words', json={
            'links': ['cuair', 'fair', 'plane', 'place', 'cuair']
        })
        rv = c.post('/insert-words', json={
            'links': ['cubair', ' 234 /你好', 'CUAIR']
        })
        assert rv.get_json()['closest_parent'] == [
            'cuair', 'cuair', 'cuair'
        ]
        rv = c.get('/auto-correct/?link= 234 /')
        assert rv.get_json()['links'] == [' 234 /你好']
        rv = c.get('/auto-correct/?link=cuAir')
        assert set(rv.get_json()['links']) == set(['cuair', 'cubair'])


def test_invalid_input():
    with ac.app.test_client() as c:
        rv = c.post('/insert-words', json={
            'idk_lol': 123
        })
        assert rv.status_code == 400
        rv = c.post('/insert-words', json={
            'links': 123
        })
        assert rv.status_code == 400
        rv = c.post('/insert-words', json={
            'links': 'hello'
        })
        assert rv.status_code == 400
        """ Actually I think empty input is fine
        rv = c.post('/insert-words', json={
            'links': []
        })
        """
        assert rv.status_code == 400
        rv = c.post('/insert-words', json={
            'links': ['hello', ['hello']]
        })
        assert rv.status_code == 400
        rv = c.post('/insert-words', json={
            'links': ['hello'],
            'idk': ['hi']
        })
        assert rv.status_code == 400
        rv = c.post('/insert-words')
        assert rv.status_code == 400
