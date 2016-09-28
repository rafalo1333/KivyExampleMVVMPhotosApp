'''Example Kivy app.'''

from kivy.app import App
from viewmodels.photosviewmodel import PhotosViewModel
from views.photosview import PhotosView


class KivyExampleMVVMPhotosApp(App):

    def build(self):
        self.photos_view_model = PhotosViewModel()
        return PhotosView()


if __name__ == '__main__':
    KivyExampleMVVMPhotosApp().run()
