#!/usr/bin/python
import psycopg2
import sys


def test_query(cursor):
    print >> sys.stdout, "Testing query."
    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()
    for record in records:
        print record


def test_insert(cursor, user):
    cursor.execute("""INSERT INTO users(id, fname, lname, location, skills, lang) VALUES
        ('%(id)s', '%(fname)s', '%(lname)s', '%(location)s', '%(skills)s', '%(lang)s')""" % user)
    cursor.connection.commit()
    print "INSERT done."


def getCursor():
    conn_string = "host='localhost' dbname='noi' user='postgres' password='ottawa6491' port='5433'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    print "Connected!\n"
    cursor = conn.cursor()
    return cursor


def findExperts(cursor, location, langs, skills):
    SQL = """SELECT * FROM
        (
        SELECT fname, lname, lang, plv8_score(skills, %s) AS score, id, location
        FROM users
        WHERE ( (location=%s) OR (%s='') ) AND
        ( (lang::jsonb ?| %s) OR (%s='{}') )
        ) AS T1 WHERE score >= 0
    ORDER BY score DESC LIMIT 10"""
    data = (skills, location, location, langs, langs)
    print cursor.mogrify(SQL, data)
    cursor.execute(SQL, data)
    records = cursor.fetchall()
    return records


def getUser(cursor, userid):
    SQL = """SELECT row_to_json(users) FROM users WHERE id = %s"""
    data = (userid,)
    print cursor.mogrify(SQL, data)
    cursor.execute(SQL, data)
    record = cursor.fetchone()
    if record:
        return record[0]
    else:
        record


def findExpertsAsJSON(cursor, location, langs, skills):
    SQL = """SELECT row_to_json(T1) FROM
        (
        SELECT *, plv8_score(skills, %s) AS score
        FROM users
        WHERE ( (location=%s) OR (%s='') ) AND
        ( (lang::jsonb ?| %s) OR (%s='{}') )
        ) AS T1 WHERE score >= 0
    ORDER BY score DESC LIMIT 10"""
    data = (skills, location, location, langs, langs)
    print cursor.mogrify(SQL, data)
    cursor.execute(SQL, data)
    records = cursor.fetchall()
    return map(lambda x:x[0], records)

def main():
    cursor = getCursor()

    #test_query(cursor)
    user = { 'id': 'google:sahuguet',
        'fname': 'Arnaud',
        'lname': 'Sahuguet',
        'location': 'US',
        'skills': '{  "opendata": {"scraping":3, "machine-readable":3, "standards": 3, "publishing-infrastructure": 3, "pii": 2, "quality": 0}, "prizes": { "legal": 0, "incentives": 3 } }',
        'lang': '["fr", "en", "es"]'
           }
    #test_insert(cursor, user)
    records = findExperts(cursor, 'United States', ['fr', 'ar'], ['scraping', 'standards'])
    for record in records:
        print record

if __name__ == "__main__":
    main()

