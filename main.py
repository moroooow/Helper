from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from functools import partial
from kivymd.uix.pickers import MDTimePicker


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


class MyApp(MDApp):
    avatar_source = "images/avatar.JPG"
    recreation_event_img = "images/recreation_events.JPG"
    concerts_event_img = "images/concerts_events.JPG"
    sports_event_img = "images/sport_events.JPG"
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
        event_details.ids.event_image.source = "images/kokun.JPG"
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
        app = MDApp.get_running_app()
        addingtask = app.root.get_screen('addingtask')
        addingtask.ids.from_button.text = f'c'
        addingtask.ids.to_button.text = f'до'
        addingtask.ids.task_input.text = ""

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

        return self.sm
MyApp().run()