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
    '''RecycleView widget used in app.'''
    pass


class PhotosView(Screen):
    '''Screen that shows the photos.

    Take a look that it only reacts to external events
    and do not know about the application data. Each method changes the state
    of the controls, but never directly touches the models.

    Button click action calls the ViewModel method,
    and there the processing is made. View is not doing any logic work itself.
    '''

    def __init__(self, **kwargs):
        super(PhotosView, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.prepare(), 0)

    def prepare(self):
        '''Prepares internal widgets references
        and subscribes to the ViewModel events.
        '''
        self.content = self.ids.content
        self.status_label = self.ids.label.__self__ # strong reference
        self.photos_stream = PhotosStream()
        app = App.get_running_app()
        app.photos_view_model.bind(
            photos=lambda o, v: self.update_photos_stream(v),
            on_photos_load_start=lambda *x: self.show_content_loading(),
            on_photos_load_progress=lambda *x: self.show_content_loading(),
            on_photos_load_error=lambda *x: self.show_content_error(),
            on_photos_load_success=lambda *x: self.show_content_loaded()
        )

    def refresh_button_clicked(self):
        '''Button click action handler.

        It just calls the ViewModel method.
        '''
        app = App.get_running_app()
        app.photos_view_model.load_photos()

    def ensure_status_label(self):
        '''Ensures that status label is shown.'''
        if not self.status_label.parent:
            self.content.clear_widgets()
            self.content.add_widget(self.status_label)

    def ensure_photos_stream(self):
        '''Ensures that photos stream is shown.'''
        self.content.clear_widgets()
        self.content.add_widget(self.photos_stream)

    def show_content_empty(self):
        '''Sets the status label text when the ViewModel data is empty.'''
        self.ensure_status_label()
        self.status_label.text = 'No photos available...'

    def show_content_loading(self):
        '''Informs the user about loading in progress.'''
        self.ensure_status_label()
        self.status_label.text = 'Loading photos in progress...'

    def show_content_loaded(self):
        '''Shows the photo stream to the user.

        Note that it does not update the photo stream, as the widget itself
        subscribes the data changes from ViewModel and updates automagically.
        '''
        self.ensure_photos_stream()

    def show_content_error(self):
        '''Informs the user about the loading error in the ViewModel.'''
        self.ensure_status_label()
        self.status_label.text = 'Photos loading error, try again later...'

    def update_photos_stream(self, photos):
        '''Updates the photo stream from a list of photos.

        This method is called every time when photos property
        in ViewModel changes. Everything is done via the event system.
        '''
        if not photos:
            self.show_content_empty()
        self.photos_stream.data = [
            {
                'source': photo.url
            }
            for photo in photos
        ]
        self.photos_stream.scroll_y = 1
