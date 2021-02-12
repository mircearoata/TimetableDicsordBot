from datetime import datetime, time, date, timedelta

def this_week(course, config):
  now = datetime.now()
  schoolStart = config.get('schoolStart', datetime.now())
  schoolWeek = (now - schoolStart).days // 7
  return schoolWeek % (course['gapWeeks'] + 1) == course['startWeek']

def get_day_courses(day: str, config):
  day = day.lower()
  allCourses = config.get('courses', {})
  dayCourses = []
  if day in allCourses:
    dayCourses = allCourses[day]
  dayCourses = [list(filter(lambda timeSlotCourse: this_week(timeSlotCourse, config), timeSlotCourses)) for timeSlotCourses in dayCourses]
  return dayCourses

def format_timedelta(timeDelta: timedelta):
  minutes, seconds = divmod(timeDelta.seconds, 60)
  if minutes > 0:
    return f'{minutes} minutes'
  return f'{seconds} seconds'
  
def time_diff(time1: time, time2: time):
  return datetime.combine(date.today(), time2) - datetime.combine(date.today(), time1)