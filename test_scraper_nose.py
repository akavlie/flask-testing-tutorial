import json
import unittest
import scraper
import requests
from mock import MagicMock
from nose.tools import assert_equal


def get_stub(*args, **kwargs):
    response = requests.get.return_value
    with open('hn_front_page.html', 'r') as f:
        response.text = f.read()
        return response

requests.get = MagicMock(side_effect=get_stub)

app = scraper.app.test_client()


def test_entry():
    # correct values
    # expected = {
    #     "comments": 118, 
    #     "comments_url": "https://news.ycombinator.com/item?id=6804440", 
    #     "points": 216, 
    #     "submitter": "citricsquid", 
    #     "time_submitted": "8 hours ago", 
    #     "title": "I Am Not Satoshi", 
    #     "url": "http://blog.dustintrammell.com/2013/11/26/i-am-not-satoshi/"
    # }

    # 3 failures -- as seen in blog post
    expected = {
        "comments": 105, 
        "comments_url": "https://news.ycombinator.com/item?id=6804440", 
        "points": 210, 
        "submitter": "citricsquid", 
        "time_submitted": "6 hours ago", 
        "title": "I Am Not Satoshi", 
        "url": "http://blog.dustintrammell.com/2013/11/26/i-am-not-satoshi/"
    }

    rv = app.get('/')
    # assert_equal(json.loads(rv.data)['stories'][1], expected)
    story = json.loads(rv.data)['stories'][1]

    def check_equal(key, val):
        assert_equal(story[key], val)
        
    for key, val in expected.iteritems():
        yield check_equal, key, val
