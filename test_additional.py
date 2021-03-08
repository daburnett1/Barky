# going to test some other things besides what has already been written
# will test delete from a database and also selecting from the database

import os
from datetime import datetime
import sqlite3

import pytest

from database import DatabaseManager

@pytest.fixture
def database_manager() -> DatabaseManager:

    filename = "test_additional.db"
    dbm = DatabaseManager(filename)
    yield dbm
    dbm.__del__()     # this is to release the database manager afterwards
    os.remove(filename)     # this does what it sounds like it does, removes the test file


def test_database_manager_del_bookmark(database_manager):

    # this is the arrange step, where we prepare everything for our test
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",     # sql for setting the id of the table and autoincrementing record numbers
            "title": "text not null",                      # sql for setting the title column and assigning it to text an no null values
            "url": "text not null",                        # pretty much the same as above
            "notes": "text",                               # again, but this time it can be empty
            "date_added": "text not null",                 # you get the picture
        },
    )

    data = {
        "title": "WTAMU_test",                    # populating the table with data
        "url": "http://www.wtamu.edu",
        "notes": "WTAMU students take notes",
        "date_added": datetime.utcnow().isoformat()
    }

    # first we list our data to ensure it populated properly
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bookmarks WHERE title = 'WTAMU_test' ''')
    cursor.fetchone()[0] == 1

    # act     now we test whether it does what it is supposed to do
    database_manager.delete("bookmarks", data)

    # assert     we verify that it actually deleted the data
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM bookmarks ''')    
    assert cursor.fetchone()[0] == 1

    # cleanup     we get rid of the table so no other test mistakenly uses the same data
    database_manager.drop_table("bookmarks")


def test_database_manager_select_bookmark(database_manager):

    # this is the arrange step, where we prepare everything for our test (just like above)
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",     # sql for setting the id of the table and autoincrementing record numbers
            "title": "text not null",                      # sql for setting the title column and assigning it to text an no null values
            "url": "text not null",                        # pretty much the same as above
            "notes": "text",                               # again, but this time it can be empty
            "date_added": "text not null",                 # you get the picture
        },
    )

    data = {
        "title": "ACTX_test",                    # populating the table with data, something different this time
        "url": "http://www.actx.edu",
        "notes": "Amarillo College students take notes",
        "date_added": datetime.utcnow().isoformat()
    }

    # act          we will verify that it selects as it should
    database_manager.select("bookmarks", data)

    #assert          we list the data to see if it selected properly
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM "bookmarks" ORDER BY "title" ''')    
    assert cursor.fetchone()[0] == 1