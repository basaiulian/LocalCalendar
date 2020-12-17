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


def custom(current_time, file_content, file_out):
    custom_calendar = MyCalendar()
    if file_content[0].strip() == "<Calendar>":
        verificare_event_1 = 0
        verificare_event_2 = 0
        verificare_alarm_1 = 0
        verificare_alarm_2 = 0
        name, description, start_date, end_date, location = "", "", "", "", ""
        trigger, action = "", ""
        my_custom_alarms_list = list()
        for (_, line) in enumerate(file_content):
            if line.strip() == "<Event>":
                verificare_event_1 = 1
            if line.strip() == "</Event>":
                verificare_event_2 = 1
            if verificare_event_1 == 1:
                if line.find("Name") != -1:
                    equal_position = line.find("=")
                    name = line[equal_position + 1::].strip()
                elif line.find("Description") != -1:
                    equal_position = line.find("=")
                    description = line[equal_position + 1::].strip()
                elif line.find("Start_Date") != -1:
                    equal_position = line.find("=")
                    start_date = line[equal_position + 1::].strip()
                elif line.find("End_Date") != -1:
                    equal_position = line.find("=")
                    end_date = line[equal_position + 1::].strip()
                elif line.find("Location") != -1:
                    equal_position = line.find("=")
                    location = line[equal_position + 1::].strip()
                elif line.strip() == "<Alarm>":
                    verificare_alarm_1 = 1
                elif line.strip() == "</Alarm>":
                    verificare_alarm_2 = 1
                elif verificare_alarm_1 == 1:
                    if line.find("Trigger") != -1:
                        equal_position = line.find("=")
                        trigger = line[equal_position + 1::].strip()

                    elif line.find("Action") != -1:
                        equal_position = line.find("=")
                        action = line[equal_position + 1::].strip()


            if verificare_event_1 == 1 and verificare_event_2 == 1:
                ok_1 = 0
                my_custom_alarm = ""
                if verificare_alarm_1 == 1 and verificare_alarm_2 == 1:
                    ok_1 = 1
                    verificare_alarm_1, verificare_alarm_2 = 0, 0
                    repeat = "None"
                    my_custom_alarm = MyAlarm(trigger, repeat, action)
                    # my_custom_alarm.print_me()
                verificare_event_1, verificare_event_2 = 0, 0
                my_custom_event = MyEvent(name, description, start_date, end_date, location)
                if ok_1 == 1:
                    my_custom_event.alarms.append(my_custom_alarm)
                    custom_calendar.events.append(my_custom_event)
                # my_custom_event.print_me()
    if file_content[-1].strip() == "</Calendar>":
        # custom_calendar.print_me()

        ########################################################################################

        for event in custom_calendar.events:
            year = int(str(event.start_date)[0:4])
            month = int(str(event.start_date)[4:6])
            day = int(str(event.start_date)[6:8])
            hour = int(str(event.start_date)[9:11])
            minute = int(str(event.start_date)[11:13])
            second = int(str(event.start_date)[13:15])
            if len(event.alarms) != 0:
                for alarm in event.alarms:

                    days_position = str(alarm.trigger).find("day")
                    days_before = str(alarm.trigger)[1:days_position - 1]
                    if days_position != -1:

                        alarm_start_date = datetime(year, month, day - int(days_before), hour,
                                                    minute, second)
                        alarm_end_date = datetime(year, month, day, hour, minute,
                                                  second)

                        # print("-------")
                        # print("start" + str(alarm_start_date))
                        # print("now" + str(current_time))
                        # print("end" + str(alarm_end_date))
                        # print("-------")
                        if alarm_start_date <= current_time <= alarm_end_date:
                            with open(file_out, "a") as file_o:
                                print("[TXT_FILE => Eveniment ce urmeaza in cateva zile] Urmeaza un eveniment( " + str(
                                    event.name) + " ) in " + str(
                                    alarm_end_date - current_time) + "\n")
                                file_o.writelines(
                                    "[TXT_FILE => Eveniment ce urmeaza in cateva zile] Urmeaza un eveniment( " + str(
                                        event.name) + " ) in " + str(
                                        alarm_end_date - current_time) + "\n")

                    else:
                        alarm_date = datetime(year, month, day, hour, minute, second)

                        if str(alarm_date)[0:-3] == str(current_time)[0:-10]:
                            print("[TXT_FILE => Date si timp exacte] Ai evenimentul " + str(
                                event.name) + " chiar acum \n")
                            with open(file_out, "a") as file_o:
                                file_o.write(
                                    "[TXT_FILE => Date si timp exacte] Ai evenimentul " + str(
                                        event.name) + " chiar acum \n")
                        elif alarm_date >= current_time:
                            print("[TXT_FILE => Eveniment ce urmeaza] Urmeaza un eveniment( " + str(
                                event.name) + " ) in " + str(
                                alarm_date - current_time) + "\n")
                            with open(file_out, "a") as file_o:
                                file_o.write(
                                    "[TXT_FILE => Eveniment ce urmeaza] Urmeaza un eveniment( " + str(
                                        event.name) + " ) in " + str(
                                        alarm_date - current_time) + "\n")


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
    print("[2] custom_calendar.txt")
    message = input("Introdu 1 sau 2: ")
    if message == "1":
        filename = "calendar_file.ics"
        with open(filename, "r") as file_in:
            file_content = file_in.read()
        ics(now, file_content, "event_alerts.txt")
    elif message == "2":
        filename = "custom_calendar.txt"
        with open(filename, "r") as custom_file_in:
            custom_file_content = custom_file_in.readlines()
        custom(now, custom_file_content, "event_alerts.txt")
    else:
        print("Input gresit.")


if __name__ == '__main__':
    __main__()
