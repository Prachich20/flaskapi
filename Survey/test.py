import app


def test_results():
    client = app.app.test_client()
    url = '/results'
    response = client.get(url, query_string={"id": 1})
    assert response.status_code == 200


def test_post_stat():
    client = app.app.test_client()
    url = 'stat/2/'
    response = client.post(url, json={"value": 5.5, 'frequency': 5})
    assert response.status_code == 200


def test_get_stat():
    client = app.app.test_client()
    url = 'stat/2/'
    response = client.get(url)
    assert response.status_code == 200


def test_delete_stat():
    client = app.app.test_client()
    url = 'stat/1/'
    response = client.delete(url)
    assert response.status_code == 200


def test_put_stat():
    client = app.app.test_client()
    url = 'stat/2/'
    response = client.put(url, json={"value": 5.5, 'frequency': 5})
    assert response.status_code == 200

# COMMENTING THE DELETE TESTCASE TO AVOID DELETION FROM DB
# def test_removesurvey():
#     client = app.app.test_client()
#     response = client.delete('/survey/1/')
#     assert response.status_code == 200


def test_addsurvey():
    client = app.app.test_client()
    response = client.post('/survey/', json={'name': 'test'})
    assert response.status_code == 200
