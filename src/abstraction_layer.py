import sqlite3, time, xlwt, datetime

class AL:
  def __init__(self):
    self.dbc = sqlite3.connect("runners.db")
    self.cursor = self.dbc.cursor()
    self.create_tables()

  def db_res_to_dic(self, db_res):
    return {"id": db_res[0], "name": db_res[1], "class": db_res[2], "level": db_res[3], "start_time": db_res[4], "stop_time": db_res[5], "group_id": db_res[6]}

  def create_tables(self):
    try:
      self.cursor.execute("CREATE TABLE runners (id integer primary key autoincrement, name text, class text, level text, start_time integer, stop_time integer, group_id integer)")
      self.dbc.commit()
    except:
      pass

  def remove_all_runners_from_db(self):
    self.cursor.execute("DELETE FROM runners")
    self.dbc.commit()

  def last_group_id(self):
    last_finished_runner = self.last_finished_runners(1)
    if len(last_finished_runner) > 0:
      return last_finished_runner[0]['group_id']
    return 0

  def next_group_id(self):
    return self.last_group_id()+1

  def start_runner(self, name, school_class, level, group_id):
    self.cursor.execute("INSERT INTO runners (name, class, level, start_time, stop_time, group_id) VALUES('%s', '%s', '%s', %i, 0, %i)" % (name, school_class, level, int(time.time()), group_id))
    self.dbc.commit()

  def stop_runner(self, runner_id):
    self.cursor.execute("UPDATE runners SET stop_time = %i WHERE id = %i" % (int(time.time()), runner_id))
    self.dbc.commit()

  def running_runners(self):
    runners = []
    self.cursor.execute("SELECT * FROM runners WHERE stop_time = 0")
    for runner in self.cursor.fetchall():
      runners.append(self.db_res_to_dic(runner))
    return runners

  def finished_runners(self):
    runners = []
    self.cursor.execute("SELECT * FROM runners WHERE stop_time != 0")
    for runner in self.cursor.fetchall():
      runners.append(self.db_res_to_dic(runner))
    return runners

  def last_finished_runners(self, number_of_runners):
    self.cursor.execute("SELECT * FROM runners WHERE stop_time != 0 ORDER BY id DESC LIMIT %i" % number_of_runners)
    runners = []
    for runner in self.cursor.fetchall():
      runners.append(self.db_res_to_dic(runner))
    return runners

  def export_db(self):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet("Runners")
    sheet.write(0,0, "Namn")
    sheet.write(0,1, "Klass")
    sheet.write(0,2, "Bana")
    sheet.write(0,3, "Start tid")
    sheet.write(0,4, "Stop tid")
    sheet.write(0,5, "Total tid (h:m:s)")
    row_num = 1
    for runner in self.finished_runners():
      sheet.write(row_num, 0, runner['name'])
      sheet.write(row_num, 1, runner['class'])
      sheet.write(row_num, 2, runner['level'])
      sheet.write(row_num, 3, datetime.datetime.fromtimestamp(runner['start_time']).strftime('%Y-%m-%d %H:%M:%S'))
      sheet.write(row_num, 4, datetime.datetime.fromtimestamp(runner['stop_time']).strftime('%Y-%m-%d %H:%M:%S'))
      sheet.write(row_num, 5, str(datetime.timedelta(seconds=(runner['stop_time'] - runner['start_time']))))
      row_num += 1

    wbk.save("db_export.xls")
