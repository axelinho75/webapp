import pytest
from main import app
from bs4 import BeautifulSoup

@pytest.fixture
def client():
    return app.test_client()


@pytest.mark.parametrize("nb, expected",[(12,12), (10,10), ('a',0), (-10,0), (0,0), (1,1)])
def test_page_b_parameter(client):
    response = client.get("/pagesb?nb=12")
    soup = BeautifulSoup(response.data.decode("utf-8"), 'html.parser')
    actual = len(soup.find_all("a"))
    assert actual == expected, f'Got {actual} wheras {excepted} a items'