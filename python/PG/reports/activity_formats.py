import sqlite3

conn = sqlite3.connect('../test.sqlite3')
c = conn.cursor()
query = (
"""
SELECT strftime('%Y', PGDate) AS YEAR, ActivityFormatDesc, COUNT(*)
FROM Activities, ActivityFormats
WHERE Activities.ActivityFormatID = ActivityFormats.ActivityFormatID
GROUP BY YEAR, ActivityFormatDesc
"""
)
