import config

def no_notify_migration():
  courses = config.get('courses', [])
  for day in courses:
    for timeSlotCourses in courses[day]:
      for course in timeSlotCourses:
        if 'noNotify' not in course:
          course['noNotify'] = False
  config.save('courses', courses)

def migrations():
  no_notify_migration()