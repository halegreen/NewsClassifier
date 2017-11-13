# coding = utf-8
import threading
# import MySQLdb
import KindEntertain
import KindArt
import KindEconomic
import KindTech
import KindArmy
import KindSociety
import KindSports
import KindHistory
import KindGame
import KindInternation

def task1(cursor, conn):
    KindEntertain.catchEntertain(cursor, conn)
    KindArt.catchArt(cursor, conn)

def task2(cursor, conn):
    KindEconomic.catchEco(cursor, conn)
    KindTech.catchTech(cursor, conn)

def task3(cursor, conn):
    KindArmy.catchArmy(cursor, conn)
    # KindSociety.catchSociety(cursor, conn)

def task4(cursor, conn):
    KindSports.catchSports(cursor, conn)
    KindHistory.catchHistroy(cursor, conn)

def task5(cursor, conn):
    # KindInternation.catchInterNation(cursor, conn)
    KindGame.catchGames(cursor, conn)

conn = ''
cursor = ''
# conn = MySQLdb.connect(host="localhost", user='root',
#                        passwd='wxx19941114', db="LEETCODE", charset="utf8mb4")
# cursor = conn.cursor()

# create_t = "CREATE TABLE IF NOT EXISTS web_page (" + \
#             "article_id int NOT NULL AUTO_INCREMENT," + \
#             "article_class VARCHAR(255) NOT NULL," + \
#             "article_content longtext," + \
#             "PRIMARY KEY (article_id));"
#
# db_name = 'LEETCODE'
#
# cursor.execute(create_t)
# cursor.execute("ALTER DATABASE %s CHARACTER SET utf8mb4;" % db_name)
# cursor.execute("alter table web_page change article_class article_class "
#                "varchar(255) character set utf8 collate utf8_unicode_ci not null default '';  ")
# cursor.execute("alter table web_page change article_content article_content "
#                "LONGTEXT character set utf8 collate utf8_unicode_ci not null ;  ")

threads = []
# t1 = threading.Thread(target=task1(cursor, conn))
# t2 = threading.Thread(target=task2(cursor, conn))
t3 = threading.Thread(target=task3(cursor, conn))
# t4 = threading.Thread(target=task4(cursor, conn))
# t5 = threading.Thread(target=task5(cursor, conn))


#threads.append(t1)
#threads.append(t2)
threads.append(t3)
# threads.append(t4)
# threads.append(t5)


for t in threads:
    t.setDaemon(True)
    t.start()
    t.join()

# conn.commit()
# cursor.close()
# conn.close()
