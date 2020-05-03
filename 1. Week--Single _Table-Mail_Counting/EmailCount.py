import sqlite3

conn = sqlite3.connect('myEmailCount.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

dictOfElems = {}

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
	
    # #cur.execute('SELECT count FROM Counts WHERE email = ? ', (email,))
    # row = cur.fetchone()
    # # if row is None:
        # # cur.execute('''INSERT INTO Counts (email, count)
                # # VALUES (?, 1)''', (email,))
    # # else:
        # # cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?',
                    # # (email,))
    # conn.commit()
    org= email.split("@")[1]
    if org in dictOfElems:
        dictOfElems[org] += 1
    else:
        dictOfElems[org] = 1

for key in dictOfElems:
    print(str(key) + ":::" + str(dictOfElems[key]))
    cur.execute('''INSERT INTO Counts (org, count) VALUES (?, ?)''', (key, dictOfElems[key]))
    cur.execute('SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10')
    conn.commit()
# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
cur.execute(sqlstr)


cur.close()