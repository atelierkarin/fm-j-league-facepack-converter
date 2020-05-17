import datetime

def calc_age(dob, target_date):
  if not datetime.datetime.strptime(dob, '%Y/%m/%d'):
    raise ValueError("Incorrect data format, should be YYYY/MM/DD")
  if not datetime.datetime.strptime(target_date, '%Y/%m/%d'):
    raise ValueError("Incorrect data format, should be YYYY/MM/DD")

  today = datetime.datetime.today()
  d_dob = datetime.datetime.strptime(dob, '%Y/%m/%d')
  d_target_date = datetime.datetime.strptime(target_date, '%Y/%m/%d')
  this_year_birthday = datetime.datetime(today.year, d_dob.month, d_dob.day)

  return d_target_date.year - d_dob.year - (this_year_birthday >= d_target_date)