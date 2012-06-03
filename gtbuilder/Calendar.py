#
# Copyright (C) 2012 - Marcus Dillavou
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

from BaseObject import BaseObject

class Calendar(BaseObject):
    calendars = []
    calendar_id = 0

    def __init__(self, service_name, monday = 0,
                 tuesday = 0, wednesday = 0, thursday = 0,
                 friday = 0, saturday = 0, sunday = 0,
                 start_date = None, end_date = None):
        BaseObject.__init__(self)

        self.calendar_id = Calendar.new_id()
        self.name = service_name
        self.days = [monday, tuesday, wednesday,
                     thursday, friday, saturday,
                     sunday]
        #self.start_date = start_date or datetime.now()
        #self.end_date = end_date or datetime.now() + relativedelta(years=+1)
        self.start_date = start_date
        self.end_date = end_date

        # add us
        Calendar.calendars.append(self)

    def write(self, f):
        self._write(f, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n',
                    self.calendar_id,
                    self.days[0], self.days[1], self.days[2],
                    self.days[3], self.days[4], self.days[5], self.days[6],
                    self.start_date,
                    self.end_date)

    @classmethod
    def write_calendars(cls, directory = '.'):
        f = open(os.path.join(directory, 'calendar.txt'), 'w')
        # header
        f.write('service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n')
        for c in cls.calendars:
            c.write(f)
        f.close()

    @classmethod
    def get(cls, calendar_id):
        for c in cls.calendars:
            if c.calendar_id == calendar_id:
                return c
        return None

    @classmethod
    def new_id(cls):
        while True:
            cls.calendar_id += 1
            if cls.calendar_id not in [x.calendar_id for x in Calendar.calendars]:
                return cls.calendar_id
