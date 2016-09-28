'''Photos list view.'''

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.app import App
from kivy.clock import Clock

kv = '''
<PhotosView>:
    name: 'PhotosView'

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            id: content

            Label:
                id: label
                text: 'No data to display...'

        BoxLayout:
            size_hint: 1, None
            height: '60dp'

            Button:
                text: 'Refresh'
                on_release: root.refresh_button_clicked()

<PhotosStream>:
    viewclass: 'TitleImage'

    RecycleBoxLayout:
        size_hint: 1, None
        height: self.minimum_height
        orientation: 'vertical'
        default_size_hint: 1, None
        default_size: None, dp(200)

<TitleImage@AsyncImage>:
    allow_stretch: True
'''

Builder.load_string(kv)

class PhotosStream(RecycleView):
    pass


class PhotosView(Screen):

    def __init__(self, **kwargs):
        super(PhotosView, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.prepare(), 0)

    def prepare(self):
        self.content = self.ids.content
        self.status_label = self.ids.label.__self__ # strong reference
        self.photos_stream = PhotosStream()
        app = App.get_running_app()
        app.photos_view_model.bind(
            photos=lambda o, v: self.update_photos_stream(v)
        )
        app.photos_view_model.bind(
            on_photos_load_start=lambda *x: self.show_content_loading(),
            on_photos_load_progress=lambda *x: self.show_content_loading(),
            on_photos_load_error=lambda *x: self.show_content_error(),
            on_photos_load_success=lambda *x: self.show_content_loaded()
        )

    def refresh_button_clicked(self):
        app = App.get_running_app()
        app.photos_view_model.load_photos()

    def ensure_status_label(self):
        if not self.status_label.parent:
            self.ids.content.clear_widgets()
            self.ids.content.add_widget(self.status_label)

    def ensure_photos_stream(self):
        self.ids.content.clear_widgets()
        self.ids.content.add_widget(self.photos_stream)

    def show_content_empty(self):
        self.ensure_status_label()
        self.status_label.text = 'No photos available...'

    def show_content_loading(self):
        self.ensure_status_label()
        self.status_label.text = 'Loading photos in progress...'

    def show_content_loaded(self):
        self.ensure_photos_stream()

    def show_content_error(self):
        self.ensure_status_label()
        self.status_label.text = 'Photos loading error, try again later...'

    def update_photos_stream(self, photos):
        self.photos_stream.data = [
            {
                'source': photo.url
            }
            for photo in photos
        ]
        self.photos_stream.scroll_y = 1
