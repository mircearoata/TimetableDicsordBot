def no_notify_migration(configs):
  for guild_id, config in configs.items():
    courses = config.get('courses', [])
    for day in courses:
      for timeSlotCourses in courses[day]:
        for course in timeSlotCourses:
          if 'noNotify' not in course:
            course['noNotify'] = False
    config.save('courses', courses)

def migrations(configs):
  no_notify_migration(configs)