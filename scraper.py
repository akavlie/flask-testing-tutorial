from flask import Flask, jsonify

import requests
from lxml import html


app = Flask(__name__)


@app.route('/')
def index():
    page = requests.get('https://news.ycombinator.com')
    root = html.fromstring(page.text)

    stories = []
    entry = {}
    for row in root.cssselect('center table table tr'):
        # add entry to list on spacer row
        if row.get('style') == 'height:5px' and entry:
            stories.append(entry)
            entry = {}

        # first row: title
        titles = row.cssselect('.title')
        if titles and len(titles) > 1:
            entry.update({
                'title': titles[1].cssselect('a')[0].text,
                'url': titles[1].cssselect('a')[0].get('href'),
            })
            # this is an HN post
            if entry['url'].startswith('item?'):
                entry['url'] = 'https://news.ycombinator.com/' + entry['url']
        # 2nd row: points, time and comments
        elif row.cssselect('.subtext span'):
            entry.update({
                'points': int(row.cssselect('.subtext span')[0].text.split()[0]),
                'submitter': row.cssselect('.subtext a')[0].text,
                'time_submitted': row.cssselect('.subtext a')[0].tail.split('|')[0].strip(),
                'comments_url': ('https://news.ycombinator.com/' +
                             row.cssselect('.subtext a')[-1].get('href'))
            })
            if row.cssselect('.subtext a')[-1].text == 'discuss':
                entry['comments'] = 0
            else:
                app.logger.info(row.cssselect('.subtext a')[-1].text.split()[0])
                entry['comments'] = \
                    int(row.cssselect('.subtext a')[-1].text.split()[0])

    return jsonify({'stories': stories})


if __name__ == '__main__':
    app.run(debug=True)
