from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from models.photo import Photo

PHOTOS_URL = 'https://jsonplaceholder.typicode.com/photos'


class PhotosViewModel(EventDispatcher):

    __events__ = (
        'on_photos_load_start',
        'on_photos_load_progress',
        'on_photos_load_success',
        'on_photos_load_error'
    )

    photos = ListProperty([])

    def load_photos(self):

        def on_success(req, res):
            photos = [Photo(data['title'], data['thumbnailUrl']) for data in res]
            self.photos = photos
            self.dispatch('on_photos_load_success')

        def on_error(req, res):
            self.dispatch('on_photos_load_error')

        def on_progress(*args):
            self.dispatch('on_photos_load_progress')

        self.dispatch('on_photos_load_start')

        # lets simulate longer request with slow network

        def request(dt):
            UrlRequest(
                PHOTOS_URL,
                on_success=on_success,
                on_error=on_error,
                on_failure=on_error,
                on_redirect=on_error,
                on_progress=on_progress
            )

        Clock.schedule_once(request, 2)

    def on_photos_load_error(self):
        pass

    def on_photos_load_success(self):
        pass

    def on_photos_load_start(self):
        pass

    def on_photos_load_progress(self):
        pass
