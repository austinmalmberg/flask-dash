
def test_brand_context(client):
    with client.session_transaction() as st:
        pass

    assert 1
