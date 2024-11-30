# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import cgi, sqlite3, hashlib
from base64 import b64encode

form = cgi.FieldStorage()
text1 = form.getfirst('login', 'Имя?')
connection = sqlite3.connect('E:\\Osipov_Michael_20150/pythonProject/University_progs/isu_database.sqlite3')
cursor = connection.cursor()
cursor.execute('SELECT photo FROM isu_list WHERE id=?', (text1,))
text3 = cursor.fetchall()[0][0]

base64_encoded_data = b64encode(text3)
base64_message = base64_encoded_data.decode('utf-8')

text2 = form.getfirst('passw', 'Пароль?')
if hashlib.sha256(text2.encode()).hexdigest() == cursor.execute('SELECT password FROM isu_list WHERE id=?', (text1,)).fetchall()[0][0]:
    print('Content-type: text/html\n')
    print('''<!DOCTYPE HTML>
    <html>
    <head>
        <meta charset='windows-1251'>
        <title>Обработка данных форм</title>
    </head>
    ''')
    print('<h1>Обработка данных форм</h1>')
    print('<p>Логин: {}</p>'.format(text1))
    print('<p>Пароль: {}</p>'.format(text2))

    print("<img src='data:image/png;base64,{}'>".format(base64_message))
    print('''</body>
            </html>''')