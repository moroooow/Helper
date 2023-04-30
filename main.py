from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDTextButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.button import Button
from functools import partial
from kivymd.uix.picker import MDTimePicker, MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from typing import NamedTuple
import pandas as pd
import datetime
from kivy.clock import Clock
import pickle
import backend
import voice_assistant
import os
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

Window.size = (375, 641)


class Task_reminder(NamedTuple):
    name: str
    type: str
    time_begin: str
    time_end: str
    date: str
    uploaded: bool
    id: int


class Event(NamedTuple):
    title: str
    description: str
    date: str
    time_begin: str
    time_end: str
    type: str
    location: str


class RegisterScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class AccountScreen(Screen):
    pass


class AddingTaskScreen(Screen):
    pass


class EventsScreen(Screen):
    pass


class EventsListScreen(Screen):
    pass


class EventDetailsScreen(Screen):
    pass


class AddingEventScreen(Screen):
    pass


class TimerScreen(Screen):
    pass


class YourDayApp(MDApp):
    avatar_source = "images/avatar.png"
    recreation_event_img = "images/recreation_events.PNG"
    concerts_event_img = "images/concerts_events.PNG"
    sports_event_img = "images/sport_events.PNG"
    user_name = "Аноним"
    email = "email: "
    cities = ["Омск", "Москва", "Краснодар"]
    event_types = ["отдых", "спорт", "концерт"]
    begin_date_of_events = f"{pd.datetime.now().day}.{pd.datetime.now().month}.{pd.datetime.now().year}"
    end_date_of_event = f"{pd.datetime.now().day + 7}.{pd.datetime.now().month}.{pd.datetime.now().year}"
    dates_of_events = f"{begin_date_of_events}-{end_date_of_event}"
    event_layout_width = 410
    task_types = ["учёба", "работа", "покупки", "другое", "отдых", "спорт", "концерт"]
    tasks_reminders = []
    date_of_list = pd.datetime.now().date()
    current_time = str(datetime.datetime.now().time())
    paid_subscriber = False
    in_delete_mode = False
    use_network = True
    waiting_for_command = False
    creating_task_va = False
    add_task_icon = "images/add_task_icon.PNG"
    calendar_icon = "images/calendar.PNG"
    timer_icon = "images/timer_icon.PNG"
    menu_icon = "images/menu_icon.PNG"
    back_icon = "images/back_icon.png"
    clock_icon = "images/clock_icon.png"
    shoping_filter_icon = "images/shoping_filter_icon.PNG"
    book_filter_icon = "images/book_filter_icon.PNG"
    work_filter_icon = "images/work_filter_icon.PNG"
    pen_filter_icon = "images/pen_filter_icon.PNG"
    hobby_filter_icon = "images/hobby_filter_icon.PNG"
    reset_filter_icon = "images/reset_filter_icon.PNG"
    bin_mode_icon = "images/bin_mode_icon.PNG"
    bin_icon = "images/bin_icon.PNG"
    current_task_time = ""
    current_task_begin = ""
    current_event = None
    current_filter = "@"
    current_event_type = ""
    current_location = ""
    user_id = -1
    task_colors = {"учёба": (82 / 255, 214 / 255, 252 / 255, 1),
                   "работа": (255 / 255, 217 / 255, 119 / 255, 1),
                   "покупки": (254 / 255, 165 / 255, 125 / 255, 1),
                   "другое": (1, 1, 1, 1),
                   "отдых": (178 / 255, 221 / 255, 139 / 255, 1),
                   "спорт": (1, 1, 1, 1),
                   "концерт": (1, 1, 1, 1)}

    va_task_title = ""
    va_task_time = ""
    va_task_type = ""
    va_task_date = ""
    creation_step = 0
    previous_va_data = ""
    command_to_ignore = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=NoTransition())
        self.screen = Builder.load_file("layout.kv")

    def set_events_in_list(self, event_type):
        self.current_event_type = event_type
        app = MDApp.get_running_app()
        event_list = app.root.get_screen('eventlist')
        event_list.ids.events_list_layout.clear_widgets()

        events = []
        if self.use_network:
            try:
                for event in backend.get_events(event_type, self.current_location):
                    events.append(Event(event[0], event[1], event[2], event[3], event[4], event[5], event[6]))
            except TypeError:
                pass
        for event in events:
            if int(self.begin_date_of_events.split('.')[2]) <= int(
                    event.date.split('.')[2]) <= \
                    int(self.end_date_of_event.split('.')[2]) and self.current_location == event.location:
                if (int(self.begin_date_of_events.split('.')[2]) == int(event.date.split('.')[2]) and (
                        int(self.begin_date_of_events.split('.')[1]) > int(event.date.split('.')[1]) or (
                        int(self.begin_date_of_events.split('.')[0]) > int(event.date.split('.')[0]) and int(
                    self.begin_date_of_events.split('.')[1]) == int(event.date.split('.')[1])))) or (int(
                    self.end_date_of_event.split('.')[2]) == int(event.date.split('.')[2]) and
                                                                                                     (int(
                                                                                                         self.end_date_of_event.split(
                                                                                                             '.')[
                                                                                                             1]) < int(
                                                                                                         event.date.split(
                                                                                                             '.')[1]) or
                                                                                                      (int(
                                                                                                          self.end_date_of_event.split(
                                                                                                              '.')[
                                                                                                              0]) < int(
                                                                                                          event.date.split(
                                                                                                              '.')[
                                                                                                              0]) and
                                                                                                       (int(
                                                                                                           self.end_date_of_event.split(
                                                                                                               '.')[
                                                                                                               1]) == int(
                                                                                                           event.date.split(
                                                                                                               '.')[
                                                                                                               1]))))):
                    pass
                else:
                    ev_box = MDCard(elevation=10,
                                    size_hint=(1, None),
                                    height=100,
                                    radius=10,
                                    padding=10,
                                    orientation="horizontal")
                    ev_box.add_widget(MDLabel(
                        text=f"{event.title}\n[size=12]{event.date} \nc{event.time_begin} до{event.time_end}[/size]",
                        markup=True))
                    ev_box.add_widget(MDFillRoundFlatButton(text="подробнее..."))
                    buttoncallback = partial(self.show_event_details, event)
                    ev_box.bind(on_release=buttoncallback)
                    event_list.ids.events_list_layout.add_widget(ev_box)

    def show_event_details(self, event, instance):
        self.sm.current = "eventdetails"
        app = MDApp.get_running_app()
        event_details = app.root.get_screen('eventdetails')
        event_details.ids.event_image.source = "images/kokun.png"
        event_details.ids.event_header.text = event.title
        event_details.ids.event_label.text = f"[size=12]{event.date}\nc {event.time_begin} до {event.time_end}[/size]\n\n{event.description}"
        self.current_event = event

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
        date = ""
        if addingtask.ids.chb_once.active:
            self.tasks_reminders.append(
                Task_reminder(addingtask.ids.task_input.text, addingtask.ids.type_spinner.text, self.begining_time,
                              self.ending_time, str(self.date_of_list).replace(",", "-"), False, -1))
            if self.use_network:
                handler = self.upload_tasks(self.tasks_reminders[-1])
                if handler[0] == 1:
                    o_t = self.tasks_reminders[-1]
                    new_task = Task_reminder(o_t.name, o_t.type, o_t.time_begin, o_t.time_end, o_t.date, True,
                                             handler[1])
                    self.tasks_reminders.remove(self.tasks_reminders[-1])
                    self.tasks_reminders.append(new_task)
            self.save_tasks()
        else:
            if addingtask.ids.chb_mon.active:
                date += "0"

            if addingtask.ids.chb_tue.active:
                date += "1"

            if addingtask.ids.chb_wed.active:
                date += "2"

            if addingtask.ids.chb_thu.active:
                date += "3"

            if addingtask.ids.chb_fri.active:
                date += "4"

            if addingtask.ids.chb_sat.active:
                date += "5"

            if addingtask.ids.chb_sun.active:
                date += "6"

            self.tasks_reminders.append(
                Task_reminder(addingtask.ids.task_input.text, addingtask.ids.type_spinner.text, self.begining_time,
                              self.ending_time, date, False, -1))
            if self.use_network:
                handler = self.upload_tasks(self.tasks_reminders[-1])
                if handler[0] == 1:
                    o_t = self.tasks_reminders[-1]
                    new_task = Task_reminder(o_t.name, o_t.type, o_t.time_begin, o_t.time_end, o_t.date, True,
                                             handler[1])
                    self.tasks_reminders.remove(self.tasks_reminders[-1])
                    self.tasks_reminders.append(new_task)
            self.save_tasks()

        self.sort_tasks()
        self.begining_time = ""
        self.ending_time = ""
        addingtask.ids.task_input.text = ""
        mainscreen.ids.task_bar.clear_widgets()
        for task in self.tasks_reminders:
            if str(self.date_of_list).replace(",", "-") in task.date or str(self.date_of_list.weekday()) in task.date:
                task_card = MDCard(elevation=10,
                                   size_hint=(1, None),
                                   height=80,
                                   radius=10,
                                   padding=10,
                                   md_bg_color=self.task_colors[task.type],
                                   orientation="horizontal")
                task_card.add_widget(MDLabel(text=task.name))
                task_card.add_widget(MDLabel(text=f"{task.time_begin}-{task.time_end}",
                                             halign="right",
                                             size_hint=(None, 1),
                                             width=100))
                task_card.add_widget(MDCheckbox(size_hint=(None, None),
                                                size=(70, 70),
                                                pos_hint={"center_y": .5}))
                mainscreen.ids.task_bar.add_widget(task_card)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Amber"

        self.sm.add_widget(RegisterScreen(name="register"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(AccountScreen(name="account"))
        self.sm.add_widget(EventsScreen(name="events"))
        self.sm.add_widget(EventsListScreen(name="eventlist"))
        self.sm.add_widget(EventDetailsScreen(name="eventdetails"))
        self.sm.add_widget(AddingTaskScreen(name="addingtask"))
        self.sm.add_widget(AddingEventScreen(name="addingevent"))
        self.sm.add_widget(TimerScreen(name="timer"))
        Clock.schedule_interval(self.update_timer, 1 / 30.)
        Clock.schedule_interval(self.listen_to_command, 1 / 30.)

        return self.sm

    def on_start(self, **kwargs):
        self.init_login()
        self.update_if_paid()
        self.tasks_reminders = self.load_tasks()
        self.filter_tasks("@")

    def listen_to_command(self, *args):
        data = voice_assistant.read_data_stream()
        if data == -1:
            return -1
        if voice_assistant.assistant_name in data and not self.waiting_for_command:
            self.va_task_date = ""
            self.va_task_time = ""
            self.va_task_title = ""
            self.va_task_type = ""
            self.timer = 0
            self.waiting_for_command = True
            listening_sound = SoundLoader.load(filename='./sounds/listening_sound.mp3')
            listening_sound.play()

        if self.waiting_for_command:
            if data == voice_assistant.assistant_name or data == "":
                self.timer = self.timer + 1 / 30
                if self.timer > 4:
                    self.waiting_for_command = False
            else:
                self.timer = 0

        if (not self.previous_va_data == voice_assistant.assistant_name) and self.waiting_for_command:
            if data == "":
                response = voice_assistant.understand_and_respond(self.previous_va_data)
                if response == "ql":
                    self.waiting_for_command = False
                if response == "sgt":
                    self.creation_step = 1
                    self.command_to_ignore = self.previous_va_data

        if data == "" and not (self.previous_va_data == self.command_to_ignore or self.previous_va_data == ""):
            if self.creation_step == 1:
                self.va_task_title = self.previous_va_data
                if not self.va_task_title == "":
                    print(self.va_task_title)
                    voice_assistant.va_say("what is the time of the task")
                    self.command_to_ignore = self.previous_va_data
                    self.creation_step = 2
            if self.creation_step == 2:
                self.va_task_time = voice_assistant.understand_time(self.previous_va_data)
                if not self.va_task_time == "":
                    self.creation_step = 3
                    print(self.va_task_time)
            if self.creation_step == 3:
                self.va_task_date = voice_assistant.understand_date(self.previous_va_data) + "." + pd.datetime.now().year
                if not self.va_task_date == "." + pd.datetime.now().year:
                    self.creation_step = 4
                    print(self.va_task_date)
            if self.creation_step == 4:
                if self.previous_va_data in self.task_types:
                    self.va_task_type = self.previous_va_data
                    self.creation_step = 5
                    print(self.va_task_type)
                    voice_assistant.va_say("save the task")
            if self.creation_step == 5:
                if self.previous_va_data == "да":
                    self.tasks_reminders.append(Task_reminder(self.va_task_title, self.va_task_type, self.va_task_time.split("-")[0], self.va_task_time.split("-")[1], self.va_task_date, False, -1))
                    if self.use_network:
                        handler = self.upload_tasks(self.tasks_reminders[-1])
                        if handler[0] == 1:
                            self.tasks_reminders.remove(self.tasks_reminders[-1])
                            self.tasks_reminders.append(
                                Task_reminder(self.va_task_title, self.va_task_type, self.va_task_time.split("-")[0], self.va_task_time.split("-")[1], self.va_task_date, True, handler[1]))
                    self.save_tasks()
                    self.sort_tasks()
                    self.filter_tasks("@")
                else:
                    self.waiting_for_command = False

        self.previous_va_data = data



    def buy_subscription(self):
        if not self.paid_subscriber and self.use_network:
            app = MDApp.get_running_app()
            accountscreen = app.root.get_screen('account')
            addeventbutton = MDTextButton(markup=True,
                                          text="[b][color=#f306a7]—[/color] Добавить\n  мероприятие[/b]")
            addeventbutton.bind(on_release=self.to_create_event)
            accountscreen.ids.account_buttons_layout.add_widget(addeventbutton, 2)
            backend.set_paid(self.email)

    def update_if_paid(self):
        if self.paid_subscriber:
            app = MDApp.get_running_app()
            accountscreen = app.root.get_screen('account')
            addeventbutton = MDTextButton(markup=True,
                                          text="[b][color=#f306a7]—[/color] Добавить\n  мероприятие[/b]")
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
        date_dialog = MDDatePicker(year=int(pd.datetime.now().year), month=int(pd.datetime.now().month),
                                   day=int(pd.datetime.now().day))
        date_dialog.bind(on_save=self.set_date_event_complete)
        date_dialog.open()

    def set_date_event_complete(self, instance, value, date):
        app = MDApp.get_running_app()
        addingevent = app.root.get_screen('addingevent')
        self.date_event = str(value).split("-")[2] + "." + str(value).split("-")[1] + "." + str(value).split("-")[0]
        addingevent.ids.date_of_event.text = self.date_event

    def submit_event(self):
        if self.use_network:
            app = MDApp.get_running_app()
            addingevent = app.root.get_screen('addingevent')
            event_title = addingevent.ids.event_create_header.text
            event_description = addingevent.ids.event_create_description.text
            event_location = addingevent.ids.event_create_location.text
            event_type = addingevent.ids.event_create_type.text

            addingevent.ids.event_create_header.text = ""
            addingevent.ids.event_create_description.text = ""
            addingevent.ids.to_time_event.text = "до"
            addingevent.ids.from_time_event.text = "c"
            addingevent.ids.date_of_event.text = "дата"
            self.sm.current = "main"
            backend.submit_event(event_title, event_description, self.date_event, self.begining_time_event,
                                 self.ending_time_event, event_type, event_location)

    def chose_date(self):
        date_dialog = MDDatePicker(year=int(pd.datetime.now().year), month=int(pd.datetime.now().month),
                                   day=int(pd.datetime.now().day))
        date_dialog.bind(on_save=self.chose_date_complete)
        date_dialog.open()

    def chose_date_complete(self, instance, value, date):
        self.date_of_list = value
        app = MDApp.get_running_app()
        mainscreen = app.root.get_screen('main')
        mainscreen.ids.task_bar.clear_widgets()
        for task in self.tasks_reminders:
            if (str(self.date_of_list).replace(",", "-") in task.date or str(
                    self.date_of_list.weekday()) in task.date) and not f"-{self.date_of_list}" in task.date:
                task_card = MDCard(elevation=10,
                                   size_hint=(1, None),
                                   height=80,
                                   radius=10,
                                   padding=10,
                                   md_bg_color=self.task_colors[task.type],
                                   orientation="horizontal")
                task_card.add_widget(MDLabel(text=task.name))
                task_card.add_widget(MDLabel(text=f"{task.time_begin}-{task.time_end}",
                                             halign="right",
                                             size_hint=(None, 1),
                                             width=100))
                task_card.add_widget(MDCheckbox(size_hint=(None, None),
                                                size=(70, 70),
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

    def start_timer(self):
        app = MDApp.get_running_app()
        timer = app.root.get_screen('timer')
        for task in self.tasks_reminders:
            if task.date == str(pd.datetime.now().date()).replace(",", "-") and int(
                    task.time_end.split(":")[0]) * 60 + int(
                task.time_end.split(":")[1]) > int(self.current_time.split(":")[0]) * 60 + int(
                self.current_time.split(":")[1]):
                timer.ids.current_task.text = task.name
                self.current_task_time = task.time_end
                self.current_task_begin = task.time_begin
                break

    def update_timer(self, *args):
        try:
            self.current_time = str(datetime.datetime.now().time())
            app = MDApp.get_running_app()
            timer = app.root.get_screen('timer')
            hrem = int(self.current_task_time.split(":")[0]) - int(self.current_time.split(":")[0])
            mrem = int(self.current_task_time.split(":")[1]) - int(self.current_time.split(":")[1])
            progress = (hrem * 60 + mrem) / ((int(self.current_task_time.split(":")[0]) - int(
                self.current_task_begin.split(":")[0])) * 60 + (int(self.current_task_time.split(":")[1]) - int(
                self.current_task_begin.split(":")[1]))) * 100
            timer.ids.time_bar.value = progress
            if mrem < 0:
                hrem -= 1
                mrem += 60
            if hrem < 0:
                timer.ids.time_remaining.text = "время вышло"
            else:
                timer.ids.time_remaining.text = f"{hrem}ч {mrem}мин"
        except(ValueError):
            pass

    def filter_tasks(self, filter):
        app = MDApp.get_running_app()
        mainscreen = app.root.get_screen('main')
        mainscreen.ids.task_bar.clear_widgets()
        self.current_filter = filter
        if filter == "@":
            for task in self.tasks_reminders:
                if (str(self.date_of_list).replace(",", "-") in task.date or str(
                        self.date_of_list.weekday()) in task.date) and not f"-{self.date_of_list}" in task.date:
                    task_card = MDCard(elevation=10,
                                       size_hint=(1, None),
                                       height=80,
                                       radius=10,
                                       padding=10,
                                       md_bg_color=self.task_colors[task.type],
                                       orientation="horizontal")
                    task_card.add_widget(MDLabel(text=task.name))
                    task_card.add_widget(MDLabel(text=f"{task.time_begin}-{task.time_end}",
                                                 halign="right",
                                                 size_hint=(None, 1),
                                                 width=100))
                    task_card.add_widget(MDCheckbox(size_hint=(None, None),
                                                    size=(70, 70),
                                                    pos_hint={"center_y": .5}))
                    mainscreen.ids.task_bar.add_widget(task_card)
        else:
            for task in self.tasks_reminders:
                if (str(self.date_of_list).replace(",", "-") in task.date or str(
                        self.date_of_list.weekday()) in task.date) and task.type == filter and not f"-{self.date_of_list}" in task.date:
                    task_card = MDCard(elevation=10,
                                       size_hint=(1, None),
                                       height=80,
                                       radius=10,
                                       padding=10,
                                       md_bg_color=self.task_colors[task.type],
                                       orientation="horizontal")
                    task_card.add_widget(MDLabel(text=task.name))
                    task_card.add_widget(MDLabel(text=f"{task.time_begin}-{task.time_end}",
                                                 halign="right",
                                                 size_hint=(None, 1),
                                                 width=100))
                    task_card.add_widget(MDCheckbox(size_hint=(None, None),
                                                    size=(70, 70),
                                                    pos_hint={"center_y": .5}))
                    mainscreen.ids.task_bar.add_widget(task_card)

    def add_event_to_tasks(self):
        self.tasks_reminders.append(
            Task_reminder(self.current_event.title, self.current_event.type, self.current_event.time_begin,
                          self.current_event.time_end, self.current_event.date, False, -1))
        if self.use_network:
            handler = self.upload_tasks(self.tasks_reminders[-1])
            if handler[0] == 1:
                self.tasks_reminders.remove(self.tasks_reminders[-1])
                self.tasks_reminders.append(
                    Task_reminder(self.current_event.title, self.current_event.type, self.current_event.time_begin,
                                  self.current_event.time_end, self.current_event.date, True, handler[1]))
        self.save_tasks()
        self.sort_tasks()
        self.filter_tasks("@")

    def enter_delete_mode(self):
        app = MDApp.get_running_app()
        mainscreen = app.root.get_screen('main')
        mainscreen.ids.task_bar.clear_widgets()
        self.in_delete_mode = not self.in_delete_mode
        for task in self.tasks_reminders:
            if (str(self.date_of_list).replace(",", "-") in task.date or str(
                    self.date_of_list.weekday()) in task.date) and not f"-{self.date_of_list}" in task.date:
                task_card = MDCard(elevation=10,
                                   size_hint=(1, None),
                                   height=80,
                                   radius=10,
                                   padding=10,
                                   md_bg_color=self.task_colors[task.type],
                                   orientation="horizontal")
                task_card.add_widget(MDLabel(text=task.name))
                task_card.add_widget(MDLabel(text=f"{task.time_begin}-{task.time_end}",
                                             halign="right",
                                             size_hint=(None, 1),
                                             width=100))
                if self.in_delete_mode:
                    delete_button = Button(size_hint=(None, None),
                                           size=(70, 70),
                                           pos_hint={"center_y": .5},
                                           background_normal=self.bin_icon,
                                           background_down=self.bin_icon)
                    buttoncallback = partial(self.delete_task, delete_button.parent)
                    delete_button.bind(on_release=buttoncallback)
                    task_card.add_widget(delete_button)
                else:
                    task_card.add_widget(MDCheckbox(size_hint=(None, None),
                                                    size=(70, 70),
                                                    pos_hint={"center_y": .5}))
                mainscreen.ids.task_bar.add_widget(task_card)

    def delete_task(self, args, task):
        for task_a in self.tasks_reminders:
            if task.parent.children[2].text == task_a.name and task_a.time_begin == \
                    task.parent.children[1].text.split("-")[0] and task_a.time_end == \
                    task.parent.children[1].text.split("-")[1]:
                if str(self.date_of_list) == task_a.date:
                    if task_a.uploaded and self.use_network:
                        backend.delete_task(task_a.id)
                    self.tasks_reminders.remove(task_a)
                    self.save_tasks()

                    break
                elif str(self.date_of_list.weekday()) in task_a.date:
                    buttoncallback1 = partial(self.delete_completely, task_a)
                    buttoncallback2 = partial(self.delete_for_the_day, task_a)
                    self.dialog = MDDialog(
                        title="Внимание!",
                        text="Как удалить это задание?",
                        buttons=[
                            MDFlatButton(
                                text="НА ВСЕ ДНИ",
                                on_release=buttoncallback1
                            ),
                            MDFlatButton(
                                text="НА СЕГОДНЯ",
                                on_release=buttoncallback2
                            ),
                        ],
                    )
                    self.dialog.open()
        self.filter_tasks(self.current_filter)
        self.enter_delete_mode()

    def delete_completely(self, task, args):
        if task.uploaded and self.use_network:
            backend.delete_task(task.id)

        self.tasks_reminders.remove(task)
        self.save_tasks()
        self.dialog.dismiss()
        self.filter_tasks(self.current_filter)

    def delete_for_the_day(self, task, args):
        self.tasks_reminders.remove(task)
        new_task = Task_reminder(task.name, task.type, task.time_begin, task.time_end,
                                 task.date + f"-{self.date_of_list}", False, -1)
        if (not task.uploaded) and self.use_network:
            handler = self.upload_tasks(task)
            if handler[0] == 1:
                new_task = Task_reminder(task.name, task.type, task.time_begin, task.time_end,
                                         task.date + f"-{self.date_of_list}", True, handler[1])
        else:
            new_task = Task_reminder(task.name, task.type, task.time_begin, task.time_end,
                                     task.date + f"-{self.date_of_list}", True, task.id)
        if self.use_network:
            backend.change_task_date(new_task.id, new_task.date)
        self.tasks_reminders.append(new_task)
        self.sort_tasks()
        self.filter_tasks(self.current_filter)
        self.save_tasks()
        self.dialog.dismiss()

    def save_tasks(self):
        with open("data.pickle", "wb") as f:
            pickle.dump(self.tasks_reminders, f, 5)

    def load_tasks(self):
        try:
            with open("data.pickle", "rb") as f:
                tasks = pickle.load(f)
                return tasks
        except(EOFError, FileNotFoundError):
            return []

    def set_event_date_range(self):
        date_dialog = MDDatePicker(year=int(pd.datetime.now().year), month=int(pd.datetime.now().month),
                                   day=int(pd.datetime.now().day), mode="range")
        date_dialog.bind(on_save=self.set_date_event_range_complete)
        date_dialog.open()

    def set_date_event_range_complete(self, instance, value, date):
        self.begin_date_of_events = str(date[0]).replace("-", ".").split(".")[2] + "." + \
                                    str(date[0]).replace("-", ".").split(".")[1] + "." + \
                                    str(date[0]).replace("-", ".").split(".")[0]
        self.end_date_of_event = str(date[-1]).replace("-", ".").split(".")[2] + "." + \
                                 str(date[-1]).replace("-", ".").split(".")[1] + "." + \
                                 str(date[-1]).replace("-", ".").split(".")[0]

        self.dates_of_events = f"{self.begin_date_of_events}-{self.end_date_of_event}"
        app = MDApp.get_running_app()
        eventlist = app.root.get_screen('eventlist')
        eventlist.ids.date_of_events_button.text = self.dates_of_events
        self.set_events_in_list(self.current_event_type)

    def choose_location(self):
        app = MDApp.get_running_app()
        events = app.root.get_screen('events')
        self.current_location = events.ids.location_spinner.text

    def register(self):
        app = MDApp.get_running_app()
        reg = app.root.get_screen('register')
        email = reg.ids.email_input.text
        first_name = reg.ids.first_name_input.text
        last_name = reg.ids.last_name_input.text
        password = reg.ids.password_input.text
        password_rep = reg.ids.password_repeat_input.text
        if not password_rep == password:
            reg.ids.out_reg.text = "пароли не совпадают"
        else:
            handler = backend.regestration(first_name, last_name, email, password)
            if handler[0] == 1:
                self.sm.current = "main"
                self.save_login_data(email, password)
                self.email = email
                self.user_id = handler[1]
                account = app.root.get_screen('account')
                account.ids.username_label.text = f"{first_name}\n{last_name}"
                account.ids.email_label.text = f"email: {email}"
            elif handler[0] == 0:
                reg.ids.out_reg.text = "эта электронная почта занята"
            elif handler[0] == -1:
                reg.ids.out_reg.text = "ошибка соединения"

    def login(self):
        app = MDApp.get_running_app()
        log = app.root.get_screen('login')
        email = log.ids.email_input.text
        password = log.ids.password_input.text
        handler = backend.log_in(email, password)
        if handler[0] == 2:
            self.sm.current = "main"
            self.save_login_data(email, password)
            self.email = email
            account = app.root.get_screen('account')
            account.ids.username_label.text = f"{handler[1]}\n{handler[2]}"
            account.ids.email_label.text = f"email: {email}"
            self.paid_subscriber = handler[3]
            self.user_id = handler[4]
            tsks = backend.get_tasks(self.user_id)
            tasks_uploaded = []
            try:
                tsks = tsks[0]
                tasks_uploaded.append(Task_reminder(tsks[0], tsks[1], tsks[2], tsks[3], tsks[4], True, tsks[6]))
            except:
                pass
            tasks_saved = self.load_tasks()
            self.compare_choose(tasks_saved, tasks_uploaded)


        elif handler[0] == 1:
            log.ids.out_log.text = "неверный пароль"
        elif handler[0] == 0:
            log.ids.out_log.text = "эта почта не зарегестрированна"
        elif handler[0] == -1:
            log.ids.out_log.text = "ошибка соединения"

    def save_login_data(self, email, password):
        with open("login_data.pickle", "wb") as f:
            pickle.dump([email, password], f, 5)

    def init_login(self):
        try:
            with open("login_data.pickle", "rb") as f:
                log_data = pickle.load(f)
            handler = backend.log_in(log_data[0], log_data[1])
            if handler[0] == 2:
                app = MDApp.get_running_app()
                self.sm.current = "main"
                account = app.root.get_screen('account')
                self.email = log_data[0]
                self.user_id = handler[4]
                account.ids.username_label.text = f"{handler[1]}\n{handler[2]}"
                account.ids.email_label.text = f"email: {log_data[0]}"
                self.paid_subscriber = handler[3]
                tsks = backend.get_tasks(self.user_id)

                tasks_uploaded = []
                try:
                    tsks = tsks[0]
                    tasks_uploaded.append(Task_reminder(tsks[0], tsks[1], tsks[2], tsks[3], tsks[4], True, tsks[6]))
                except:
                    pass
                tasks_saved = self.load_tasks()
                self.compare_choose(tasks_saved, tasks_uploaded)
        except:
            pass

    def logout(self):
        os.remove("login_data.pickle")
        self.sm.current = "register"
        with open("data.pickle", "wb") as f:
            pickle.dump("", f)

    def upload_tasks(self, task):
        return backend.upload_tasks(task.name, task.type, task.time_begin, task.time_end, task.date, self.user_id)

    def compare_choose(self, saved_ts, uploaded_ts):
        dif = False
        if len(saved_ts) == len(uploaded_ts):
            for task in saved_ts:
                if not task.uploaded:
                    dif = True
                    break
        else:
            dif = True
        if dif:
            choose_saved = partial(self.choose_saved, saved_ts)
            choose_uploaded = partial(self.choose_uploaded, uploaded_ts)
            self.dialog = MDDialog(
                title="Внимание!",
                text="Данные в облаке и на устройстве отличаются.",
                buttons=[
                    MDFlatButton(
                        text="ЗАГРУЗИТЬ ЛОКАЛЬНЫЕ",
                        on_release=choose_saved
                    ),
                    MDFlatButton(
                        text="ЗАГРУЗИТЬ ИЗ ОБЛАКА",
                        on_release=choose_uploaded
                    ),
                ],
            )
            self.dialog.open()

    def choose_saved(self, tasks, args):
        backend.clear_tasks(self.user_id)
        self.tasks_reminders = []
        for task in tasks:
            handle = backend.upload_tasks(task.name, task.type, task.time_begin, task.time_end, task.date, self.user_id)
            if handle[0] == 1:
                self.tasks_reminders.append(
                    Task_reminder(task.name, task.type, task.time_begin, task.time_end, task.date, True, handle[1]))
        self.save_tasks()
        self.dialog.dismiss()
        self.filter_tasks("@")

    def choose_uploaded(self, tasks, args):
        self.tasks_reminders = []
        for task in tasks:
            self.tasks_reminders.append(Task_reminder(task[0], task[1], task[2], task[3], task[4], True, task[6]))
        self.save_tasks()
        self.dialog.dismiss()
        self.filter_tasks("@")


YourDayApp().run()
