from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDTextButton
from functools import partial
from kivymd.uix.picker import MDTimePicker, MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from typing import NamedTuple
import pandas as pd


class Task_reminder(NamedTuple):
    name: str
    time_begin: str
    time_end: str
    date: str


class Event(NamedTuple):
    title: str
    description: str
    date: str
    time_begin: str
    time_end: str


class MainScreen(Screen):
    pass


class AccountScreen(Screen):
    pass


class AddingTaskScreen(Screen):
    pass


class CalendarScreen(Screen):
    pass


class EventsScreen(Screen):
    pass


class EventsListScreen(Screen):
    pass


class EventDetailsScreen(Screen):
    pass


class AddingEventScreen(Screen):
    pass


class MyApp(MDApp):
    avatar_source = "images/avatar.png"
    recreation_event_img = "images/recreation_events.PNG"
    concerts_event_img = "images/concerts_events.PNG"
    sports_event_img = "images/sport_events.PNG"
    user_name = "Наталья\nПень"
    email = "example@gmail.com"
    password = "********"
    cities = ["city_1", "city_2", "city_3", "city_4", "city_5", "city_6", "city_7", "city_8"]
    dates_of_events = "31.01-03.03"
    event_layout_width = 840
    events_recreation = ["Фестиваль \"большие огурцы\"", "Цирк клоунов", "Парад кринжа"]
    events_sport = ["Кубок большого кубка", "Большой теннис", "Защита деревни", "Спорт спорт"]
    events_concerts = ["Концерт ГРОБ", "Концерт Цоя", "Концерт Дайте танк(!)"]
    events_concerts_details = ["test grob", "test tsoi", "test tank"]
    events_sport_details = ["test Кубок большого кубка", "test Большой теннис", "test Защита деревни",
                            "test Спорт спорт"]
    events_recreation_details = ["test большие огурцы", "test Цирк клоунов", "test Парад кринжа"]
    tasks_reminders = []
    date_of_list = str(pd.datetime.now().date()).replace(",", "-")
    paid_subscriber = True
    add_task_icon = "images/add_task_icon.PNG"
    calendar_icon = "images/calendar.PNG"
    timer_icon = "images/timer_icon.PNG"
    menu_icon = "images/menu_icon.PNG"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=NoTransition())
        self.screen = Builder.load_file("kivymd.kv")

    def set_events_in_list(self, event_list_sec, event_details_list):
        app = MDApp.get_running_app()
        event_list = app.root.get_screen('eventlist')
        event_list.ids.events_list_layout.clear_widgets()
        for i in range(len(event_list_sec)):
            ev_box = MDCard(elevation=10,
                            size_hint=(1, None),
                            height=100,
                            radius=10,
                            padding=10,
                            orientation="horizontal")
            ev_box.add_widget(MDLabel(text=event_list_sec[i]))
            ev_box.add_widget(MDFillRoundFlatButton(text="подробнее..."))
            buttoncallback = partial(self.show_event_details, [event_list_sec[i], event_details_list[i]])
            ev_box.bind(on_release=buttoncallback)
            event_list.ids.events_list_layout.add_widget(ev_box)

    def show_event_details(self, detail_text_header, instance):
        self.sm.current = "eventdetails"
        app = MDApp.get_running_app()
        event_details = app.root.get_screen('eventdetails')
        event_details.ids.event_image.source = "images/kokun.png"
        event_details.ids.event_header.text = detail_text_header[0]
        event_details.ids.event_label.text = detail_text_header[1]

    def time_picker(self, arg):
        time_dialog = MDTimePicker()
        if arg == "from":
            time_dialog.bind(on_save=self.set_begining_time)
        elif arg == "to":
            time_dialog.bind(on_save=self.set_ending_time)
        time_dialog.open()

    def set_begining_time(self, instance, time):
        app = MDApp.get_running_app()
        addingtask = app.root.get_screen('addingtask')
        self.begining_time = str(time)[:5]
        addingtask.ids.from_button.text = f'c {self.begining_time[:5]}'

    def set_ending_time(self, instance, time):
        app = MDApp.get_running_app()
        addingtask = app.root.get_screen('addingtask')
        self.ending_time = str(time)[:5]
        addingtask.ids.to_button.text = f'до {self.ending_time}'

    def reset_time(self):
        self.begining_time = ""
        self.ending_time = ""
        app = MDApp.get_running_app()
        addingtask = app.root.get_screen('addingtask')
        addingtask.ids.from_button.text = f'c'
        addingtask.ids.to_button.text = f'до'
        addingtask.ids.task_input.text = ""

    def create_task(self):
        app = MDApp.get_running_app()
        addingtask = app.root.get_screen('addingtask')
        mainscreen = app.root.get_screen('main')
        addingtask.ids.from_button.text = f'c'
        addingtask.ids.to_button.text = f'до'
        self.tasks_reminders.append(
            Task_reminder(addingtask.ids.task_input.text, self.begining_time, self.ending_time, self.date_of_list))
        self.sort_tasks()
        self.begining_time = ""
        self.ending_time = ""
        addingtask.ids.task_input.text = ""
        mainscreen.ids.task_bar.clear_widgets()
        for task in self.tasks_reminders:
            if task.date == self.date_of_list:
                task_card = MDCard(elevation=10,
                                   size_hint=(1, None),
                                   height=100,
                                   radius=10,
                                   padding=10,
                                   orientation="horizontal")
                task_card.add_widget(MDLabel(text=task.name))
                task_card.add_widget(MDLabel(text=f"{task.time_begin}-{task.time_end}",
                                             halign="right",
                                             size_hint=(None, 1),
                                             width=100))
                task_card.add_widget(MDCheckbox(size_hint=(None, None),
                                                size=(50, 50),
                                                pos_hint={"center_y": .5}))
                mainscreen.ids.task_bar.add_widget(task_card)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Amber"

        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(AccountScreen(name="account"))
        self.sm.add_widget(CalendarScreen(name="calendar"))
        self.sm.add_widget(EventsScreen(name="events"))
        self.sm.add_widget(EventsListScreen(name="eventlist"))
        self.sm.add_widget(EventDetailsScreen(name="eventdetails"))
        self.sm.add_widget(AddingTaskScreen(name="addingtask"))
        self.sm.add_widget(AddingEventScreen(name="addingevent"))

        return self.sm

    def buy_subscription(self):
        if self.paid_subscriber:
            app = MDApp.get_running_app()
            accountscreen = app.root.get_screen('account')
            addeventbutton = MDTextButton(text="-Добавить\n  мероприятие")
            addeventbutton.bind(on_release=self.to_create_event)
            accountscreen.ids.account_buttons_layout.add_widget(addeventbutton, 2)

    def to_create_event(self, arg):
        self.sm.current = "addingevent"

    def set_event_time(self, arg):
        time_dialog = MDTimePicker()
        if arg == "from":
            time_dialog.bind(on_save=self.set_begining_time_event)
        elif arg == "to":
            time_dialog.bind(on_save=self.set_ending_time_event)
        time_dialog.open()

    def set_begining_time_event(self, instance, time):
        app = MDApp.get_running_app()
        addingevent = app.root.get_screen('addingevent')
        self.begining_time_event = str(time)[:5]
        addingevent.ids.from_time_event.text = f'c {self.begining_time_event[:5]}'

    def set_ending_time_event(self, instance, time):
        app = MDApp.get_running_app()
        addingevent = app.root.get_screen('addingevent')
        self.ending_time_event = str(time)[:5]
        addingevent.ids.to_time_event.text = f'до {self.ending_time_event[:5]}'

    def set_event_date(self):
        date_dialog = MDDatePicker(year=int(pd.datetime.now().year), month=int(pd.datetime.now().mounth),
                                   day=int(pd.datetime.now().day))
        date_dialog.bind(on_save=self.set_date_event_complete)
        date_dialog.open()

    def set_date_event_complete(self, instance, value, date):
        app = MDApp.get_running_app()
        addingevent = app.root.get_screen('addingevent')
        self.date_event = str(value)
        addingevent.ids.date_of_event.text = self.date_event

    def submit_event(self):
        app = MDApp.get_running_app()
        addingevent = app.root.get_screen('addingevent')
        self.submited_event_header = addingevent.ids.event_create_header.text
        self.submited_event_description = addingevent.ids.event_create_description.text
        self.submited_event_location = addingevent.ids.event_create_location.text
        print(self.submited_event_header)
        print(self.submited_event_description)
        print(self.submited_event_location)
        print(self.date_event)
        print(self.begining_time_event)
        print(self.ending_time_event)
        addingevent.ids.event_create_header.text = ""
        addingevent.ids.event_create_description.text = ""
        addingevent.ids.to_time_event.text = "до"
        addingevent.ids.from_time_event.text = "c"
        addingevent.ids.date_of_event.text = "дата"
        self.sm.current = "main"

    def chose_date(self):
        date_dialog = MDDatePicker(year=int(pd.datetime.now().year), month=int(pd.datetime.now().month),
                                   day=int(pd.datetime.now().day))
        date_dialog.bind(on_save=self.chose_date_complete)
        date_dialog.open()

    def chose_date_complete(self, instance, value, date):
        self.date_of_list = str(value)
        app = MDApp.get_running_app()
        mainscreen = app.root.get_screen('main')
        mainscreen.ids.task_bar.clear_widgets()
        print(self.tasks_reminders)
        for task in self.tasks_reminders:
            if task.date == self.date_of_list:
                task_card = MDCard(elevation=10,
                                   size_hint=(1, None),
                                   height=100,
                                   radius=10,
                                   padding=10,
                                   orientation="horizontal")
                task_card.add_widget(MDLabel(text=task.name))
                task_card.add_widget(MDLabel(text=f"{task.time_begin}-{task.time_end}",
                                             halign="right",
                                             size_hint=(None, 1),
                                             width=100))
                task_card.add_widget(MDCheckbox(size_hint=(None, None),
                                                size=(50, 50),
                                                pos_hint={"center_y": .5}))
                mainscreen.ids.task_bar.add_widget(task_card)

    def sort_tasks(self):
        n = len(self.tasks_reminders)
        for j in range(n):
            already_sorted = True
            for i in range(n - j - 1):
                tf = int(self.tasks_reminders[i].time_begin.split(":")[0]) * 60 + int(
                    self.tasks_reminders[i].time_begin.split(":")[1])
                ts = int(self.tasks_reminders[i + 1].time_begin.split(":")[0]) * 60 + int(
                    self.tasks_reminders[i + 1].time_begin.split(":")[1])
                if tf > ts:
                    self.tasks_reminders[i], self.tasks_reminders[i + 1] = self.tasks_reminders[i + 1], \
                                                                           self.tasks_reminders[i]
                    already_sorted = False
                elif tf == ts:
                    tfe = int(self.tasks_reminders[i].time_end.split(":")[0]) * 60 + int(
                        self.tasks_reminders[i].time_end.split(":")[1])
                    tse = int(self.tasks_reminders[i + 1].time_end.split(":")[0]) * 60 + int(
                        self.tasks_reminders[i + 1].time_end.split(":")[1])
                    if tfe > tse:
                        self.tasks_reminders[i], self.tasks_reminders[i + 1] = self.tasks_reminders[i + 1], \
                                                                               self.tasks_reminders[i]
                        already_sorted = False
            if already_sorted:
                break


MyApp().run()
