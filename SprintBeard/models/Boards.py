import MySQLdb
import uuid

ADMIN_PRIVILEGES = 0
EDITOR_PRIVILEGES = 1
VIEWER_PRIVILEGES = 2

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')
