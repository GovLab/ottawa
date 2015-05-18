import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import session
from flask import jsonify
import json

import yaml

SKILLS = yaml.load(open('data/skills-demo.yaml'))
CONTENT = yaml.load(open('data/content.yaml'))

ALL_COUNTRIES = "Afghanistan,Algeria,Argentina,Australia,Austria,Bahamas,Bangladesh,Belgium,Belize,Benin,Bhutan,Brazil,Bulgaria,Burkina Faso,Burundi,Cambodia,Cameroon,Canada,Central African Rep,Chad,Chile,China,Colombia,Congo,Congo, The Democratic Rep,Connected!,Connecting to database,Costa Rica,Cuba,Czech Republic,Denmark,Djibouti,Dominican Republic,Ecuador,Egypt,El Salvador,Ethiopia,Fiji,Finland,France,Gambia,Georgia,Germany,Ghana,Guatemala,Guinea,Haiti,Hungary,India,Indonesia,Iran,Iraq,Ireland,Italy,Ivory Coast (Cote D'Ivoire),Jamaica,Japan,Jordan,Kenya,Korea, Republic Of,Kyrgyzstan,Lebanon,Liberia,Lithuania,Macedonia (Republic of),Madagascar,Malawi,Malaysia,Mali,Mauritania,Mexico,Moldova, Rep,Mongolia,Montenegro,Namibia,Nepal,Netherlands,New Zealand,Niger,Nigeria,Pakistan,Panama,Papua New Guinea,Paraguay,Peru,Philippines,Romania,Russian Federation,Rwanda,Samoa,Senegal,Serbia,Slovakia (Slovak Rep),Somalia,South Africa,Spain,Sri Lanka,Sudan,Sweden,Switzerland,Taiwan,Tajikistan,Tanzania,Thailand,Togo,Tonga,Trinidad & Tobago,Tunisia,Turkey,Uganda,Ukraine,United Kingdom,United States,Uruguay,Viet Nam,Yemen,Zambia".split(',')

app = Flask(__name__)
app.debug = True
app.secret_key = 'M\xb5\xc1\xa39t\x97\x88\x13A\xe8\t\x90\xc2\x04@\xe4\xdeM\xc8?\x05}j'

import test_db


def defaultList(the_list, default_value):
    if the_list == []:
        return [default_value]
    else:
        return the_list


@app.route("/main")
def main():
    print session
    return render_template('main.html', **{})


@app.route("/")
def main2():
    print session
    return render_template('main2.html', **{})


@app.route("/about")
def about():
    return render_template('about.html', **{})


@app.route("/me")
def me():
    return render_template('my-profile.html', **{})


@app.route('/user/<userid>')
def get_user(userid):
    cursor = test_db.getCursor()
    user = test_db.getUser(cursor, userid)
    return render_template('user-profile.html', **{'user': user, 'SKILLS': SKILLS})


@app.route("/my-expertises")
def my_expertises():
    return render_template('my-expertises.html', **{'OPENDATA': CONTENT['open-data'],'ANSWERS': CONTENT['answers'], 'QUESTIONS': CONTENT['questions']})


@app.route("/clear_session")
def clear_session():
    session.clear()
    return redirect(url_for("main2"))


@app.route("/session", methods=['POST'])
def manage_session():
    if request.method == 'POST':
        print "Receiving token from client"
        session['user-as-JSON']  = json.loads(request.form['user-as-JSON'])
        session['token'] = request.form['token']
        return jsonify({'result': 0})


@app.route("/search")
def search():
    location = request.args.get('location')
    langs = request.args.getlist('langs')
    skills = request.args.getlist('skills')
    cursor = test_db.getCursor()
    query = {'location': location, 'langs': langs, 'skills': skills}
    experts = test_db.findExpertsAsJSON(cursor, **query)
    return render_template('search-results.html', **{'title': 'Expertise search', 'results': experts, 'query': query})


@app.route("/match")
def match():
    location = request.args.get('location', 'United States')  # default = United States.
    langs = request.args.getlist('langs')
    skills = request.args.getlist('skills')
    cursor = test_db.getCursor()
    query = {'location': location, 'langs': langs, 'skills': skills}
    experts = test_db.findExpertsAsJSON(cursor, **query)
    return render_template('search-results.html', **{'title': 'Matching', 'results': experts, 'query': query})


@app.route("/search-ui")
def main_route():
    return render_template('search.html', **{'skills': SKILLS['opendata'], 'ALL_COUNTRIES': ALL_COUNTRIES})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
