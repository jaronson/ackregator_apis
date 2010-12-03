import psycopg2
import ConfigParser

class Model:
  config = ConfigParser.RawConfigParser()
  config.read("../config/application.conf")

  dbname    = config.get("Database", "name")
  user      = config.get("Database", "user")
  password  = config.get("Database", "password")
  

  def __init__(self):
    self.cursor = None
    self.connection = None
    self.__connect()
  
  def __del__(self):
    self.__disconnect()

  def insertListing(self, source, data):
    self.execute("INSERT INTO listings (source, xml_data) VALUES (%s, %s)", ( source, data ))

  def execute(self, statement, params=None):
    if not params:
      self.cursor.execute(statement)
    else:
      self.cursor.execute(statement, params)
    self.connection.commit()
 
  def __connect(self):
    self.connection = psycopg2.connect("dbname=%s user=%s password=%s" % ( Model.dbname, Model.user, Model.password))
    self.cursor = self.connection.cursor()

  def __disconnect(self):
    if self.cursor:
      self.cursor.close()

    if self.connection:
      self.connection.close()
