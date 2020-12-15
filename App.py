from ics import Calendar

"""
Alarma se activeaza la timpul exact dat
TRIGGER;VALUE=DATE-TIME:20201220T133000Z

Alarma se activeaza cu 30 minute inainte de eveniment
TRIGGER:-PT30M

Alarma se activeaza cu 2 zile inainte de eveniment
TRIGGER:-P2D

!!! Cand am o alarma care se activeaza la un timp exact
        pot avea:
REPEAT: 23
Astfel, alarma se va repeta de 23 de ori la interval de 1 ora
"""


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


def __main__():
    with open("calendar_file.ics", "r") as file_in:
        file_content = file_in.read()

    # with open("event_alerts.txt", "w") as file_out:
    #     file_out.write("========================= ALERTS =========================")

    calendar = Calendar(file_content)

    events = list(calendar.events)

    my_calendar = MyCalendar()

    for event in events:
        my_event = MyEvent(event.name, event.description, event.begin, event.end, event.location)
        for alarm in event.alarms:
            my_alarm = MyAlarm(alarm.trigger, alarm.repeat, alarm.action)
            my_event.add_alarm(my_alarm)
        my_calendar.add_event(my_event)
    my_calendar.print_me()


if __name__ == '__main__':
    __main__()
