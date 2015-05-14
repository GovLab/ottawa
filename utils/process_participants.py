import csv
import psycopg2
from psycopg2.extras import Json


def getCursor():
    conn_string = "host='localhost' dbname='noi' user='postgres' password='ottawa6491' port=5433"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    print "Connected!\n"
    cursor = conn.cursor()
    return cursor


import yaml
import random
import json

SKILLS = yaml.load(open('data/skills-demo.yaml'))
LEVELS = ['n/a', 'I can refer', 'I can teach', 'I can do']
LANGS = ['fr', 'en', 'es', 'ar', 'pt', 'de']


def makeRandomSkills():
    all_skills = {}
    for s in SKILLS:
        if random.random() > 0.5:
            how_many_items = int(random.gauss(len(SKILLS[s]), 1)) % len(SKILLS[s])
            skills = random.sample(SKILLS[s], how_many_items)
            all_skills[s] = {x: random.randint(0, len(LEVELS)-1) for x in skills}
    return all_skills

#print makeRandomSkills()

def insertUser(cursor, user):
    try:
        SQL = "INSERT INTO users(id, fname, lname, location, city, org, title, skills, lang) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (user['id'], user['fname'], user['lname'], user['location'], user['city'], user['org'], user['title'], user['skills'], user['lang'], )
        cursor.execute(SQL, data)
        cursor.connection.commit()
        print "INSERT done."
    except Exception, e:
        print e
        print "Error insert %s" % user

cursor = getCursor()
with open('ottawa-list.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for item in reader:
        (uid, lname, org, country, email, title, registration_type, fname, city) = item
        skills = makeRandomSkills()
        langs = [random.choice(LANGS), random.choice(LANGS)]
        #print skills

        user = {'id': uid, 'fname': fname, 'lname': lname, 'location': country, 'city': city, 'org': org, 'title': title, 'skills': Json(skills), 'lang': Json(langs)}
        insertUser(cursor, user)
