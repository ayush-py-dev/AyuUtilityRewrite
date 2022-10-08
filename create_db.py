import sqlite3

db1 = sqlite3.connect('Database/afk.db')
cur = db1.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS afk (memid INTEGER, memname TEXT, memres TEXT, afktime INTEGER)')
db1.commit()
db1.close()

db2 = sqlite3.connect('Database/gaway.db')
cur = db2.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS main(
			hostid INTEGER,
			noofwin INTEGER,
			prize TEXT,
			ending INTEGER,
			gmsgid INTEGER,
			gmchid INTEGER)""")
db2.commit()
db2.close()

db3 = sqlite3.connect('Database/invites.db')
cur = db3.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS inv(
        memid INTEGER,
        invcot INTEGER
    )""")
db3.commit()
db3.close()

db4 = sqlite3.connect('Database/levels.db')
cur = db4.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS lvl(
	    "memid"	INTEGER,
	    "xp"	FLOAT,
	    "xpreq"	INTEGER,
	    "lev"	INTEGER,
	    "imgurl"	TEXT,
	    "primcol"	TEXT,
	    "seccol"	TEXT)
    """)
db4.commit()
db4.close()

db5 = sqlite3.connect('Database/reminder.db')
cur = db5.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS reminder (
            user_id INTEGER,
            message TEXT,
            time INTEGER,
            channel_id INTEGER,
            reminder_id INTEGER
        )""")
db5.commit()
db5.close()

db6 = sqlite3.connect('Database/todo.db')
cur = db6.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS todo (
            member_id INTEGER,
            todo TEXT,
            created_at INTEGER,
            todo_id TEXT
        )""")
db6.commit()
db6.close()

db7 = sqlite3.connect('Database/warns.db')
cur = db7.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS warn(
        memid INTEGER,
        reason TEXT,
        mod INTEGER,
        time INTEGER,
        wid TEXT
    )""")
db7.commit()
db7.close()

db8 = sqlite3.connect('Database/Economy/mprice.db')
cur = db8.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS market(
            cname TEXT,
            vale INTEGER
        )""")
db8.commit()
db8.close()

db9 = sqlite3.connect('Database/Economy/users.db')
cur = db9.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS bank(
            memid TEXT,
            coins INTEGER,
            ich INTEGER,
            wsi INTEGER,
            soc INTEGER,
            gzi INTEGER,
            fsp INTEGER
        )""")
db9.commit()
db9.close()

db10 = sqlite3.connect('Database/staff.db')
cur = db10.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS staff(
            memid INTEGER,          
            strike INTEGER
        )""")
db10.commit()
db10.close()

print("Created all Database files.")
