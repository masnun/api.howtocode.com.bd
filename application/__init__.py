import json, urllib2
from flask import Flask, render_template, redirect
from google.appengine.api import memcache

app = Flask(__name__)


@app.route("/")
def home():
    return redirect("http://howtocode.com.bd")


@app.route('/contrib/<repo>')
def contrib(repo):
    try:
        url = "https://api.github.com/repos/howtocode-com-bd/%s.howtocode.com.bd/contributors" % repo
        data = json.loads(urllib2.urlopen(url).read())
        memcache.set(repo, data)
    except Exception as ex:
        data = memcache.get(repo)
        if data is None:
            return ""

    for id, author in enumerate(data):
        data[id]['badge_login'] = author['login'].replace("-", "--")
        data[id][
            'commits_url'] = "https://github.com/howtocode-com-bd/%s.howtocode.com.bd/commits/master?author=%s" % (
            repo, author['login'])
    return render_template('contrib.html', data=data)


if __name__ == '__main__':
    app.run()
