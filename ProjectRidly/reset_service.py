import sqlite3
##########Check for sensor param db
print "initing"
try:
    conn = sqlite3.connect("/home/root/Ridley/ProjectRidly/unified.db")
    c = conn.cursor()
    c.execute('''DELETE FROM stack;''')
    conn.commit()
    conn.close()
except Exception, e:
        print e
        