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
from kivy.uix.image import Image
from kivymd.uix.selectioncontrol import MDCheckbox
from typing import NamedTuple
import pandas as pd
import datetime
from kivy.clock import Clock
import pickle
import backend


class Task_reminder(NamedTuple):
    name: str
    type: str
    time_begin: str
    time_end: str
    date: str


class Event(NamedTuple):
    title: str
    description: str
    date: str
    time_begin: str
    time_end: str
    type: str
    location: str


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


class MyApp(MDApp):
    avatar_source = "images/avatar.png"
    recreation_event_img = "images/recreation_events.PNG"
    concerts_event_img = "images/concerts_events.PNG"
    sports_event_img = "images/sport_events.PNG"
    user_name = "Наталья\nПень"
    email = "example@gmail.com"
    password = "********"
    cities = ["Омск", "Москва", "Краснодар"]
    event_types = ["recreation", "sport", "concerts"]
    begin_date_of_events = f"{pd.datetime.now().day}.{pd.datetime.now().month}.{pd.datetime.now().year}"
    end_date_of_event = f"{pd.datetime.now().day + 7}.{pd.datetime.now().month}.{pd.datetime.now().year}"
    dates_of_events = f"{begin_date_of_events}-{end_date_of_event}"
    event_layout_width = 840
    events = [
        Event("Фестиваль \"большие огурцы\"", "test большие огурцы", "23.12.2004", "12:30", "13:00", "recreation",
              "Омск"),
        Event("Цирк клоунов", "test Цирк клоунов", "23.12.2004", "12:30", "13:00", "sport", "Москва"),
        Event("Парад кринжа", "test Парад кринжа", "23.12.2004", "12:30", "13:00", "concerts", "Краснодар")]
    task_types = ["учёба", "работа", "хобби", "покупки", "другое"]
    tasks_reminders = []
    date_of_list = pd.datetime.now().date()
    current_time = str(datetime.datetime.now().time())
    paid_subscriber = True
    in_delete_mode = False
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=NoTransition())
        self.load_tasks()
        self.screen = Builder.load_file("kivymd.kv")

    def set_events_in_list(self, event_type):
        self.current_event_type = event_type
        app = MDApp.get_running_app()
        event_list = app.root.get_screen('eventlist')
        event_list.ids.events_list_layout.clear_widgets()
        for event in self.events:
            if event_type == event.type and int(self.begin_date_of_events.split('.')[2]) <= int(
                    event.date.split('.')[2]) <= \
                    int(self.end_date_of_event.split('.')[2]) and self.current_location == event.location:
                if (int(self.begin_date_of_events.split('.')[2]) == int(event.date.split('.')[2]) and (
                        int(self.begin_date_of_events.split('.')[1]) > int(event.date.split('.')[1]) or (
                        int(self.begin_date_of_events.split('.')[0]) > int(event.date.split('.')[0]) and int(
                        self.begin_date_of_events.split('.')[1]) == int(event.date.split('.')[1])))) or (int(
                        self.end_date_of_event.split('.')[2]) == int(event.date.split('.')[2]) and
                        (int(self.end_date_of_event.split('.')[1]) < int(event.date.split('.')[1]) or
                         (int(self.end_date_of_event.split('.')[0]) < int(event.date.split('.')[0]) and
                          (int(self.end_date_of_event.split('.')[1]) == int(event.date.split('.')[1]))))):
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
                              self.ending_time, str(self.date_of_list).replace(",", "-")))
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
                              self.ending_time, date))
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
        self.sm.add_widget(EventsScreen(name="events"))
        self.sm.add_widget(EventsListScreen(name="eventlist"))
        self.sm.add_widget(EventDetailsScreen(name="eventdetails"))
        self.sm.add_widget(AddingTaskScreen(name="addingtask"))
        self.sm.add_widget(AddingEventScreen(name="addingevent"))
        self.sm.add_widget(TimerScreen(name="timer"))
        Clock.schedule_interval(self.update_timer, 1 / 30.)

        return self.sm

    def on_start(self, **kwargs):
        self.filter_tasks("@")

    def buy_subscription(self):
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
        backend.submit_event(event_title, event_description, self.date_event, self.begining_time_event, self.ending_time_event, event_type, event_location)

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
        else:
            for task in self.tasks_reminders:
                if (str(self.date_of_list).replace(",", "-") in task.date or str(
                        self.date_of_list.weekday()) in task.date) and task.type == filter and not f"-{self.date_of_list}" in task.date:
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

    def add_event_to_tasks(self):
        self.tasks_reminders.append(
            Task_reminder(self.current_event.title, self.current_event.type, self.current_event.time_begin,
                          self.current_event.time_end, self.current_event.date))
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
                                   height=100,
                                   radius=10,
                                   padding=10,
                                   orientation="horizontal")
                task_card.add_widget(MDLabel(text=task.name))
                task_card.add_widget(MDLabel(text=f"{task.time_begin}-{task.time_end}",
                                             halign="right",
                                             size_hint=(None, 1),
                                             width=100))
                if self.in_delete_mode:
                    delete_button = Button(size_hint=(None, None),
                                           size=(50, 50),
                                           pos_hint={"center_y": .5},
                                           background_color=(0, 0, 0, 0))
                    buttoncallback = partial(self.delete_task, delete_button.parent)
                    delete_button.add_widget(Image(source=self.bin_icon,
                                                   size_hint=(None, None),
                                                   pos=delete_button.pos,
                                                   size=(60, 60)))
                    delete_button.bind(on_release=buttoncallback)
                    task_card.add_widget(delete_button)
                else:
                    task_card.add_widget(MDCheckbox(size_hint=(None, None),
                                                    size=(50, 50),
                                                    pos_hint={"center_y": .5}))
                mainscreen.ids.task_bar.add_widget(task_card)

    def delete_task(self, args, task):
        for task_a in self.tasks_reminders:
            if task.parent.children[2].text == task_a.name and task_a.time_begin == \
                    task.parent.children[1].text.split("-")[0] and task_a.time_end == \
                    task.parent.children[1].text.split("-")[1]:
                if str(self.date_of_list) == task_a.date:
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
        self.tasks_reminders.remove(task)
        self.save_tasks()
        self.dialog.dismiss()
        self.filter_tasks(self.current_filter)

    def delete_for_the_day(self, task, args):
        self.tasks_reminders.remove(task)
        new_task = Task_reminder(task.name, task.type, task.time_begin, task.time_end,
                                 task.date + f"-{self.date_of_list}")
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
                self.tasks_reminders = pickle.load(f)
        except(EOFError):
            pass

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
        print("cool")


MyApp().run()
