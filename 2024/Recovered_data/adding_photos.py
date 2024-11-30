import os
import sqlite3

conn = sqlite3.connect('E:\\Osipov_Michael_20150/pythonProject/University_progs/isu_database.sqlite3')
cursor = conn.cursor()
# cursor.execute("ALTER TABLE isu_list ADD COLUMN photo text")
#
# for item in os.listdir(path := 'E:\\Osipov_Michael_20150/pythonProject/University_progs/Photos'):
#     os.chdir(path)
#     photo_img = open(item, 'rb').read()
#     cursor.execute('UPDATE isu_list SET photo=? WHERE id=?', (photo_img, item[1:-4]))
#
# # cursor.execute('INSERT INTO isu_list photo VALUE=? WHERE id=?', (photos_b, ids))
# conn.commit()

for line in cursor.execute('SELECT photo FROM isu_list').fetchall():
    print(line)
cursor.close()