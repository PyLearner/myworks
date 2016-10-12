import sqlite3 as db
import os
import argparse
import datetime
import time
from avocado.core import data_dir

__version__ = 'draft'

"""

Scan our avocado results when the test is still running, avocado provides
the plugin "journal" helping us to achieve this.

../plugins/journal.py

SCHEMA = {'job_info': 'CREATE TABLE job_info (unique_id TEXT UNIQUE)',
          'test_journal': ("CREATE TABLE test_journal ("
                           "tag TEXT, "
                           "time TEXT, "
                           "action TEXT, "
                           "status TEXT, "
                           "flushed BOOLEAN DEFAULT 0)")}
"""

class DbHandle:

    def __init__(self, db_filepath):
        self.db_filepath = db_filepath

    def get_table_name(self, sql_cmd):
        conn = db.connect(self.db_filepath)
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        table_name = cursor.fetchall()[-1]
        conn.close()

        return table_name

    def get_table_content(self, sql_cmd):
        conn = db.connect(self.db_filepath)
        conn.row_factory = db.Row
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
        table_content = cursor.fetchall()
        conn.close()

        return table_content

def nice_results(max_width, casename, status, seconds):
    print_format = '%%-%ds    %%-6s  %%-6s' % max_width
    print print_format % (casename, status, seconds)

def isoformat2seconds(isoformattime):
    tmpstr = isoformattime.rsplit(".")[0].replace("T", " ")
    d = datetime.datetime.strptime(tmpstr,"%Y-%m-%d %H:%M:%S")
    return time.mktime(d.timetuple())


def parse_result(table_content):

    max_width = 0
    starttime = ""
    endtime = ""
    for i in table_content:
        max_width = max(max_width,len(i['tag']))

    nice_results(0, "Test", "Status", "Time")
    nice_results(0, "----", "------", "-------")
    for i in table_content:
        if i['action'] == 'STARTED':
            starttime = isoformat2seconds(i['time'])
            continue
        if i['action'] == "ENDED":
            endtime = isoformat2seconds(i['time'])
            nice_results(max_width, i['tag'], i['status'], int(endtime - starttime))
            continue

if __name__ == '__main__':

  db_file = ".journal.sqlite"
  log_dir = data_dir.get_logs_dir()
  # default file path
  db_file_path = os.path.join(log_dir, "latest/", db_file)
  get_table_name_cmd = "SELECT name FROM sqlite_master WHERE type='table';"

  parser_a = argparse.ArgumentParser(description="show avocado results.")
  parser_a.add_argument('-f', '--filepath',
                          help='path of the results file results.json',
                          dest='filepath', action='store')
  arguments = parser_a.parse_args()

  if arguments.filepath is not None and os.path.exists(os.path.join(arguments.filepath,
                                                                    db_file)):
      db_handle_file = DbHandle(os.path.join(arguments.filepath, db_file))
      get_test_journal_content_cmd = "select * from %s" % \
                                     db_handle_file.get_table_name(get_table_name_cmd)
      parse_result(db_handle_file.get_table_content(get_test_journal_content_cmd))

  elif arguments.filepath is None and os.path.exists(db_file_path):
      db_handle_file = DbHandle(db_file_path)
      get_test_journal_content_cmd = "select * from %s" % \
                                     db_handle_file.get_table_name(get_table_name_cmd)
      parse_result(db_handle_file.get_table_content(get_test_journal_content_cmd))

  else:
      print "File doesn't exist."
      exit(0)