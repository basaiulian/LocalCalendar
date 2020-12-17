import string
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


def custom(current_time, file_content, file_out, file_flag):
    if check_bad_custom_format(file_content):
        return

    custom_calendar = MyCalendar()
    if file_content[0].strip() == "<Calendar>":
        verificare_event_1, verificare_event_2, verificare_alarm_1, verificare_alarm_2 = 0, 0, 0, 0
        name, description, start_date, end_date, location = "", "", "", "", ""
        trigger, action, repeat = "", "", ""
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

                    elif line.find("Repeat") != -1:
                        equal_position = line.find("=")
                        repeat = line[equal_position + 1::].strip()

            if verificare_event_1 == 1 and verificare_event_2 == 1:
                ok_1 = 0
                my_custom_alarm = ""
                if verificare_alarm_1 == 1 and verificare_alarm_2 == 1:
                    ok_1 = 1
                    verificare_alarm_1, verificare_alarm_2 = 0, 0
                    my_custom_alarm = MyAlarm(trigger, repeat, action)
                verificare_event_1, verificare_event_2 = 0, 0
                my_custom_event = MyEvent(name, description, start_date, end_date, location)
                if ok_1 == 1:
                    my_custom_event.alarms.append(my_custom_alarm)
                    custom_calendar.events.append(my_custom_event)

    if file_content[-1].strip() == "</Calendar>":

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

                        if alarm_start_date <= current_time <= alarm_end_date:
                            if not file_flag:
                                print("[TXT_FILE => Upcoming event] New event ( " + str(
                                    event.name) + ") in " + str(
                                    alarm_end_date - current_time) + ".\n")
                            elif file_flag:
                                with open(file_out, "a") as file_o:
                                    file_o.writelines(
                                        "[TXT_FILE => Upcoming event] New event ( " + str(
                                            event.name) + ") in " + str(
                                            alarm_end_date - current_time) + ".\n")

                    else:
                        alarm_date = datetime(year, month, day, hour, minute, second)

                        if str(alarm_date)[0:-3] == str(current_time)[0:-10]:
                            if not file_flag:
                                print("[TXT_FILE => Ongoing event] You have an ongoing event(" + str(
                                    event.name) + ") right now.\n")
                            elif file_flag:
                                with open(file_out, "a") as file_o:
                                    file_o.write(
                                        "[TXT_FILE => Ongoing event] You have an ongoing event(" + str(
                                            event.name) + ") right now.\n")
                        elif alarm_date >= current_time:
                            if not file_flag:
                                print("[TXT_FILE => Upcoming event] New event( " + str(
                                    event.name) + ") in " + str(
                                    alarm_date - current_time) + ".\n")
                            elif file_flag:
                                with open(file_out, "a") as file_o:
                                    file_o.write(
                                        "[TXT_FILE => Upcoming event] New event( " + str(
                                            event.name) + ") in " + str(
                                            alarm_date - current_time) + ".\n")



def check_bad_custom_format(file_content):
    log_time = datetime.now()
    log_line = "[ERROR:::" + str(log_time.time()) + ":::] Bad custom file format.\n"
    content = ""
    content = content.join(file_content)
    if content.find("<Calendar>") == -1 or content.find("</Calendar>") == -1 or content.count(
            "<Event>") != content.count("</Event>") or content.count(
        "<Alarm>") != content.count("</Alarm>"):
        print("Bad custom file format.")
        with open("logs.txt", 'a') as logs:
            logs.writelines(log_line)
        return True
    return False


def check_bad_ics_format(file_content):
    log_time = datetime.now()
    log_line = "[ERROR:::" + str(log_time.time()) + ":::] Bad ics file format.\n"
    content = ""
    content = content.join(file_content)
    if content.find("BEGIN:VCALENDAR") == -1 or content.find("END:VCALENDAR") == -1 or content.count(
            "BEGIN:VEVENT") != content.count("END:VEVENT") or content.count(
        "BEGIN:VALARM") != content.count("END:VALARM"):
        print("Bad ics file format.")
        with open("logs.txt", 'a') as logs:
            logs.writelines(log_line)
        return True
    return False


def ics(current_time, file_content, file_out, file_flag):
    if check_bad_ics_format(file_content):
        return

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
                repeat = ""
                days_position = str(alarm.trigger).find("day")
                if days_position != -1:
                    days_before = str(alarm.trigger)[1:days_position - 1]
                    year = int(str(event.start_date)[0:4])
                    month = int(str(event.start_date)[5:7])
                    day = int(str(event.start_date)[8:10])
                    hour = int(str(event.start_date)[11:13])
                    minute = int(str(event.start_date)[14:16])
                    second = int(str(event.start_date)[17:19])

                    if str(alarm.repeat) != "None":
                        repeat = int(str(alarm.repeat))

                        if hour - int(repeat) <= 0:

                            difference = int(repeat) - hour
                            # print("diferenta zi trecuta: " + str(difference))
                            last_day = difference
                            # print("diferenta zi curenta: " + str(int(repeat) - difference))
                            current_day = int(repeat) - difference
                            repeat_start_date = datetime(year, month, day - 1, 24 - difference,
                                                         minute, second)

                            # print("Alarma se va repeta incepand cu: " + str(repeat_start_date))

                            start_date_event = datetime(year, month, day, hour,
                                                        minute, second)

                            while last_day != 0:
                                repeat_start_date = datetime(year, month, day - 1,
                                                             24 - last_day,
                                                             minute, second)
                                # print(repeat_start_date)
                                if current_time == repeat_start_date:
                                    if not file_flag:
                                        print(
                                            "[ICS_FILE => Upcoming event] New event( " + str(
                                                event.name) + ") in " + str(
                                                start_date_event - current_time) + ".\n")
                                    elif file_flag == True:
                                        with open(file_out, "a") as file_o:
                                            file_o.writelines("[ICS_FILE => Upcoming event] New event( " + str(
                                                event.name) + ") in " + str(
                                                start_date_event - current_time) + ".\n")

                                last_day -= 1
                            count = 0
                            while count <= current_day:

                                repeat_start_date = datetime(year, month, day,
                                                             0 + count,
                                                             minute, second)

                                # afisez fiecare datetime la care ar trebui sa sune alarma cu repeat
                                # print(repeat_start_date)

                                if current_time == repeat_start_date:
                                    if not file_flag:
                                        print(
                                            "[ICS_FILE => Upcoming event] New event( " + str(
                                                event.name) + ") in " + str(
                                                start_date_event - current_time) + ".\n")
                                    elif file_flag:
                                        with open(file_out, "a") as file_o:
                                            file_o.writelines("[ICS_FILE => Upcoming event] New event( " + str(
                                                event.name) + ") in " + str(
                                                start_date_event - current_time) + ".\n")

                                count += 1

                        else:
                            repeat_start_date = datetime(year, month, day, hour - int(repeat),
                                                         minute, second)
                            print(repeat_start_date)

                    alarm_start_date = datetime(year, month, day - int(days_before), hour,
                                                minute, second)
                    alarm_end_date = datetime(year, month, day, hour, minute,
                                              second)

                    if alarm_start_date <= current_time <= alarm_end_date:
                        if not file_flag:
                            print("[ICS_FILE => Upcoming event] New event (" + str(
                                event.name) + ") in " + str(
                                alarm_end_date - current_time) + ".\n")
                        elif file_flag:
                            with open(file_out, "a") as file_o:
                                file_o.writelines(
                                    "[ICS_FILE => Upcoming event] New event (" + str(
                                        event.name) + ") in " + str(
                                        alarm_end_date - current_time) + ".\n")

                else:
                    year = int(str(event.start_date)[0:4])
                    month = int(str(event.start_date)[5:7])
                    day = int(str(event.start_date)[8:10])
                    hour = int(str(event.start_date)[11:13])
                    minute = int(str(event.start_date)[14:16])
                    second = int(str(event.start_date)[17:19])
                    alarm_date = datetime(year, month, day, hour, minute, second)

                    if str(alarm_date)[0:-3] == str(current_time)[0:-10]:
                        if not file_flag:
                            print("[ICS_FILE => Ongoing event] You have an ongoing event(" + str(
                                event.name) + ") right now. \n")
                        elif file_flag:
                            with open(file_out, "a") as file_o:
                                file_o.write(
                                    "[ICS_FILE => Ongoing event] You have an ongoing event(" + str(
                                        event.name) + ") right now.\n")

                    elif alarm_date >= current_time:
                        if not file_flag:
                            print("[ICS_FILE => Upcoming event] New event( " + str(
                                event.name) + ") in " + str(
                                alarm_date - current_time) + ".\n")
                        elif file_flag:
                            with open(file_out, "a") as file_o:
                                file_o.write(
                                    "[ICS_FILE => Upcoming event] New event( " + str(
                                        event.name) + " ) in " + str(
                                        alarm_date - current_time) + ".\n")


with open("logs.txt", "w") as logs:
    logs.write("========================= LOGS =========================\n")


def __main__():
    now = datetime.now()
    # now = datetime(2020, 12, 17, 20, 50, 0)
    with open("event_alerts.txt", "w") as file_out:
        file_out.write("========================= ALERTS =========================\n")

    file_flag = ""

    while file_flag is not True and file_flag is not False:
        print("How do you want to get your alerts?")
        choice = input("Your choice[display or file]: ")
        if choice.strip().lower() == "display":
            file_flag = False
        elif choice.strip().lower() == "file":
            file_flag = True
        else:
            log_time = datetime.now()
            log_line = "[ERROR:::" + str(log_time.time()) + ":::] Bad choice. Try again!\n"
            with open("logs.txt", "a") as logs:
                logs.write(log_line)
            print("Bad choice. Try again!")

    message = ""
    while message.strip() != "1" or message.strip != "2":
        print("What format do you want to check?")
        print("[1] calendar_file.ics")
        print("[2] custom_calendar.txt")
        message = input("Enter 1 or 2: ")
        if message.strip() == "1":
            filename = "calendar_file.ics"
            with open(filename, "r") as file_in:
                file_content = file_in.read()
            ics(now, file_content, "event_alerts.txt", file_flag)
            break
        elif message.strip() == "2":
            filename = "custom_calendar.txt"
            with open(filename, "r") as custom_file_in:
                custom_file_content = custom_file_in.readlines()
            custom(now, custom_file_content, "event_alerts.txt", file_flag)
            break
        else:
            log_time = datetime.now()
            log_line = "[ERROR:::" + str(log_time.time()) + ":::] Wrong input. Try again!\n"
            with open("logs.txt", "a") as logs:
                logs.write(log_line)
            print("Wrong input. Try again!")


if __name__ == '__main__':
    __main__()
