from datetime import datetime

from ics import Calendar


class MyAlarm:
    def __init__(self, trigger, repeat, action):
        self.trigger = trigger
        self.action = action
        if repeat == "":
            self.repeat = "None"
        else:
            self.repeat = repeat

    def print_me(self):
        print("Trigger: " + str(self.trigger))
        print("Repeat: " + str(self.repeat))
        print("Action: " + str(self.action))


class MyEvent:
    def __init__(self, name, description, start_date, end_date, location):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.alarms = list()

    def add_alarm(self, alarm):
        self.alarms.append(alarm)

    def print_me(self):
        print("Name: " + str(self.name))
        print("Description: " + str(self.description))
        print("Start Date: " + str(self.start_date))
        print("End Date: " + str(self.end_date))
        print("Location: " + str(self.location))
        if len(self.alarms) != 0:
            print("Alarms: ")
            for alarm in self.alarms:
                print("--------------Alarm--------------")
                alarm.print_me()
        else:
            print("Alarms: None")


class MyCalendar:
    def __init__(self):
        self.events = list()

    def add_event(self, event):
        self.events.append(event)

    def print_me(self):
        for event in self.events:
            print("===============Event===============")
            event.print_me()
     
 
def ics(current_time, file_content, file_out):
    calendar = Calendar(file_content)

    events = list(calendar.events)

    my_calendar = MyCalendar()

    for event in events:
        my_event = MyEvent(event.name, event.description, event.begin, event.end, event.location)
        for alarm in event.alarms:
            my_alarm = MyAlarm(alarm.trigger, alarm.repeat, alarm.action)
            my_event.add_alarm(my_alarm)
        my_calendar.add_event(my_event)

    for event in my_calendar.events:
        if len(event.alarms) != 0:
            for alarm in event.alarms:
                days_position = str(alarm.trigger).find("day")
                if days_position != -1:
                    days_before = str(alarm.trigger)[1:days_position - 1]
                    start_year = int(str(event.start_date)[0:4])
                    start_month = int(str(event.start_date)[5:7])
                    start_day = int(str(event.start_date)[8:10])
                    start_hour = int(str(event.start_date)[11:13])
                    start_minute = int(str(event.start_date)[14:16])
                    start_second = int(str(event.start_date)[17:19])

                    alarm_start_date = datetime(start_year, start_month, start_day - int(days_before), start_hour,
                                                start_minute, start_second)
                    alarm_end_date = datetime(start_year, start_month, start_day, start_hour, start_minute,
                                              start_second)

                    # print("-------")
                    # print("start" + str(alarm_start_date))
                    # print("now" + str(now))
                    # print("end" + str(alarm_end_date))
                    # print("-------")
                    if alarm_start_date <= current_time <= alarm_end_date:
                        with open("event_alerts.txt", "a") as file_out:
                            print("[ICS_FILE => Eveniment ce urmeaza in cateva zile] Urmeaza un eveniment( " + str(
                                event.name) + " ) in " + str(
                                alarm_end_date - current_time) + "\n")
                            file_out.writelines(
                                "[ICS_FILE => Eveniment ce urmeaza in cateva zile] Urmeaza un eveniment( " + str(
                                    event.name) + " ) in " + str(
                                    alarm_end_date - current_time) + "\n")

                else:
                    year = int(str(alarm.trigger)[0:4])
                    month = int(str(alarm.trigger)[5:7])
                    day = int(str(alarm.trigger)[8:10])
                    hour = int(str(alarm.trigger)[11:13])
                    minute = int(str(alarm.trigger)[14:16])
                    second = int(str(alarm.trigger)[17:19])
                    alarm_date = datetime(year, month, day, hour, minute, second)

                    if str(alarm_date)[0:-3] == str(current_time)[0:-10]:
                        print("[ICS_FILE => Date si timp exacte] Ai evenimentul " + str(
                            event.name) + " chiar acum \n")
                        with open(file_out, "a") as file_out:
                            file_o.write(
                                "[ICS_FILE => Date si timp exacte] Ai evenimentul " + str(
                                    event.name) + " chiar acum \n")

                    elif alarm_date >= current_time:
                        print("[ICS_FILE => Eveniment ce urmeaza] Urmeaza un eveniment( " + str(
                            event.name) + " ) in " + str(
                            alarm_date - current_time) + "\n")
                        with open("event_alerts.txt", "a") as file_o:
                            file_o.write(
                                "[ICS_FILE => Eveniment ce urmeaza] Urmeaza un eveniment( " + str(
                                    event.name) + " ) in " + str(
                                    alarm_date - current_time) + "\n")


def __main__():
    now = datetime.now()

    with open("event_alerts.txt", "w") as file_out:
        file_out.write("========================= ALERTS =========================\n")

    print("[1] calendar_file.ics")
    message = input("Introdu 1 sau 2: ") # 2 neimplementat
    if message == "1":
        filename = "calendar_file.ics"
        with open(filename, "r") as file_in:
            file_content = file_in.read()
        ics(now, file_content, "event_alerts.txt")
    else:
        print("Input gresit.")


if __name__ == '__main__':
    __main__()