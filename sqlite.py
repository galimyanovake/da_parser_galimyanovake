import sqlite3
def initializedb():
    connection = sqlite3.connect('steamdata.db')
    cursor = connection.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS game
    ''')
    cursor.execute('''
        DROP TABLE IF EXISTS platform 
    ''')
    cursor.execute('''
        DROP TABLE IF EXISTS gameplatform 
    ''')
    cursor.execute('''
        CREATE TABLE game (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        pricenodiscount REAL NOT NULL,
        pricediscount REAL NOT NULL,
        rating REAL NOT NULL,
        reviews INTEGER NOT NULL,
        isdiscount INTEGER NOT NULL          
        )
    ''')
    cursor.execute('''
        CREATE TABLE platform (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL     
        )
    ''')
    cursor.execute('''
        CREATE TABLE gameplatform (
        gameid INTEGER,
        platformid INTEGER,
        FOREIGN KEY (gameid)  REFERENCES game (id),
        FOREIGN KEY (platformid)  REFERENCES platform (id)  
        )
    ''')
    connection.commit()
    connection.close()
def loadtosql(data):
    connection = sqlite3.connect('steamdata.db')
    cursor = connection.cursor()
    for platform in data["allplatforms"]:
        cursor.execute(f'''
            INSERT INTO platform (name) 
            VALUES (?)
            ''', [platform])
    connection.commit()
    for i in range(len(data["gameid"])):
        cursor.execute(f'''
        INSERT INTO game (id, title, pricenodiscount, pricediscount, rating, reviews, isdiscount) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (int(data["gameid"][i]), data["title"][i], float(str(data["pricenodiscount"][i]).replace(",", ".")), float(str(data["pricediscount"][i]).replace(",", ".")), float(data["rating"][i])/100, int(data["reviews"][i]), int(data["isdiscount"][i])))
        for platform in data["platforms"][i]:
            cursor.execute(f'SELECT id FROM platform WHERE name = ?', [platform])
            platformid = cursor.fetchall()
            cursor.execute(f'''
            INSERT INTO gameplatform (gameid, platformid) 
            VALUES (?,?)
            ''', (int(data["gameid"][i]), int(platformid[0][0])))
    connection.commit()
    connection.close()


def test():
    connection = sqlite3.connect('steamdata.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TEMP TABLE avg_price_per_platform AS
                    SELECT p.id, AVG(g.pricediscount) AS avg_price FROM gameplatform AS gp INNER JOIN game AS g ON gp.gameid = g.id INNER JOIN platform AS p ON gp.platformid = p.id GROUP BY p.name
                   ''')
    cursor.execute('SELECT * FROM avg_price_per_platform ')
    results = cursor.fetchall()
    print(results)

    cursor.execute('''CREATE TEMP TABLE avg_minus_price AS
                    SELECT * FROM gameplatform
                   ''')
    cursor.execute('ALTER TABLE avg_minus_price ADD COLUMN avg_price REAL')
    cursor.execute('ALTER TABLE avg_minus_price ADD COLUMN price REAL')
    cursor.execute('UPDATE avg_minus_price SET avg_price = (SELECT avg_price FROM avg_price_per_platform WHERE avg_minus_price.platformid = avg_price_per_platform.id)')
    cursor.execute('UPDATE avg_minus_price SET price = (SELECT pricediscount FROM game WHERE avg_minus_price.gameid = game.id)')
    cursor.execute('ALTER TABLE avg_minus_price ADD COLUMN difference REAL')
    cursor.execute('UPDATE avg_minus_price SET difference = avg_price-price')
    cursor.execute('SELECT gameid, platformid, difference FROM avg_minus_price ')
    results = cursor.fetchall()
    print(results)
    cursor.execute('DROP TABLE avg_price_per_platform')
    cursor.execute('DROP TABLE avg_minus_price')
    connection.close()

if __name__ == "__main__":
    test()

    