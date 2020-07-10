import MySQLdb
import datetime
import os
import sys
import pandas as pd

def main():
    # fetch_db_newest()
    pass

def fetch_db_newest():
   '''
   fetch db the newest data for data confirm
   :return: db_neswest_data
   '''

   # fetch key_word
   key_word = pd.read_csv(r'{}/key_word.csv'.format(os.getcwd()))
   print(key_word)

   try:
      # connect database
      db = MySQLdb.connect(host = str(key_word.loc[0, 'host']),
                           user = str(key_word.loc[0, 'user']),
                           passwd = str(key_word.loc[0, "passwd"]),
                           db = str(key_word.loc[0, "db"]),
                           port = int(key_word.loc[0, "port"]),
                           charset=str(key_word.loc[0, "charset"]))

      sql_str = "SELECT web_name, publish_time, title, url FROM fruveg.Daniel_news_test where related = 1 order by publish_time desc limit 10;"
      db_neswest_data_df = pd.read_sql(sql=sql_str, con=db)

   except Exception as err:
      msg = "01.Unable to fetch data from db. Program stop!! {}".format(err)
      write_log(msg)
      print(err)
      sys.exit(0)

   db.close()
   print(db_neswest_data_df)

   # # init db_neswest_data dict
   # db_neswest_data = {}
   # # store db newest data to dict
   # db_neswest_data['web_name'] = str(db_neswest_data_df.loc[0,'web_name'])
   # db_neswest_data['publish_time'] = datetime.datetime.strptime(str(db_neswest_data_df.loc[0,'publish_time']),
   #                                                              "%Y-%m-%d %H:%M:%S")
   # # db_neswest_data['web_class'] = str(db_neswest_data_df.loc[0,'web_class'])
   # db_neswest_data['title'] = str(db_neswest_data_df.loc[0,'title'])
   # db_neswest_data['url'] = str(db_neswest_data_df.loc[0,'url'])

   # return db_neswest_data (dict format)
   x = []

   for i in range(db_neswest_data_df.shape[0]):
       t=[]
       t.append(db_neswest_data_df.loc[i,"web_name"])
       t.append(db_neswest_data_df.loc[i,"publish_time"])
       t.append(db_neswest_data_df.loc[i,"title"])
       t.append(db_neswest_data_df.loc[i,"url"])
       x.append(t)

   return x

def write_log(log):
   '''
   write log to log file
   :param log: log message
   '''

   now = datetime.datetime.now()
   today = datetime.date.today()

   # Standard output to log file
   print("{}, {}".format(now, log))
   # print("{}, {}".format(now, log), file=open("{}/log_folder/log_{}.txt".format(os.getcwd(),today), "a"))

if __name__ == "__main__":
   '''
   main function
   '''
   main()