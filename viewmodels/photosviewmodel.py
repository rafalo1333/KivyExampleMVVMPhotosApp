from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from models.photo import Photo

PHOTOS_URL = 'https://jsonplaceholder.typicode.com/photos'
'''Photos API url.'''


class PhotosViewModel(EventDispatcher):
    '''ViewModel responsible for handling the photos data.

    It uses external API calls to update the data
    and fires the events about its state.
    View part can subscribe to them to update the user interface.

    In Kivy it must be EventDispatcher derived class.
    '''

    __events__ = (
        'on_photos_load_start',
        'on_photos_load_progress',
        'on_photos_load_success',
        'on_photos_load_error'
    )
    '''Events fired by the ViewModel.'''

    photos = ListProperty([])
    '''Photo model object list. View should subscribe to this property events
    to be informed about the data changes.
    '''

    def load_photos(self):
        '''Loads the photos from the external API and fires the work events.'''

        def on_success(req, res):
            photos = [Photo(data['title'], data['thumbnailUrl']) for data in res]
            self.photos = photos
            self.dispatch('on_photos_load_success')

        def on_error(req, res):
            self.dispatch('on_photos_load_error')

        def on_progress(*args):
            self.dispatch('on_photos_load_progress')

        self.dispatch('on_photos_load_start')

        # lets simulate longer request with slow network (2 seconds slowdown)

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
        '''Default event handler.'''
        pass

    def on_photos_load_success(self):
        '''Default event handler.'''
        pass

    def on_photos_load_start(self):
        '''Default event handler.'''
        pass

    def on_photos_load_progress(self):
        '''Default event handler.'''
        pass
