import mysql.connector
import pandas as pd
connection = mysql.connector.connect(
        host='210.71.198.188',
        database='web353',
        user='admin',
        password='1qaz@wsx'
    )
cursor = connection.cursor()
cursor.execute("SELECT * FROM `mdl_user_info_field`")
df = pd.DataFrame(cursor.fetchall())
print(df)