import pytest

from scrapers.woolies import jsonify


def test_get_data():
    pass


def load_page():
    pass


def test_jsonify():
    """convert string to json"""
    assert jsonify("""
    {
    "store": "SuperMart",
    "location": "Downtown",
    "products": [
        {
            "name": "apple",
            "price": 1.5,
            "quantity": 100
        },
        {
            "name": "banana",
            "price": 0.75,
            "quantity": 150
        },
        {
            "name": "orange",
            "price": 1.2,
            "quantity": 80
        }
    ]
}
    """) == {
        "store": "SuperMart",
        "location": "Downtown",
        "products": [
            {"name": "apple", "price": 1.5, "quantity": 100},
            {"name": "banana", "price": 0.75, "quantity": 150},
            {"name": "orange", "price": 1.2, "quantity": 80},
        ],
    }


def test_jsonify_bad():
    """convert string to json and removed bad characters"""
    assert jsonify("""
    HEHEHEHEH<?D><SA>D<?SAD<SA?>DS<ADSAA{
    "store": "SuperMart",
    "location": "Downtown",
    "products": [
        {
            "name": "apple",
            "price": 1.5,
            "quantity": 100
        },
        {
            "name": "banana",
            "price": 0.75,
            "quantity": 150
        },
        {
            "name": "orange",
            "price": 1.2,
            "quantity": 80
        }
    ]
}?>DSA>D?>SAD?>SA?D>SA?>DF?WA>F?WAS?DS>A
    """) == {
        "store": "SuperMart",
        "location": "Downtown",
        "products": [
            {"name": "apple", "price": 1.5, "quantity": 100},
            {"name": "banana", "price": 0.75, "quantity": 150},
            {"name": "orange", "price": 1.2, "quantity": 80},
        ],
    }
