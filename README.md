# Kivy MVVM example Photos app
## MVVM implementation in Kivy app.
### Author: Rafał Kaczor aka rafalo1333

Project shows how to write data-driven Kivy application with Model-View-ViewModel design pattern in mind.

1. **Model** is the data representation and it can be any python class
2. **View** is a Kivy widget displaying the data. It can be a *Label*, *Button* or *Screen*.
3. **ViewModel** is the binding part between the **Model** and the **View**. It takes care of getting the data, formatting it to the **Model** object format and keeping the models collections references. During processing it fires the events, such as `on_work_start`, `on_work_progress` and `on_work_finish`. The **View** should subscribe to the ViewModel **properties** and events and update accordingly.

In Photos example app, the model is the simple python `Photo` class. ViewModel is implemented in `PhotosViewModel` class based on the `EventDispatcher`, because it needs to propagate framework events. View is a `Screen`, which reacts on ViewModel events to update the content. Note that the view object holds no references to models or viewmodels: it only reacts to events.

**Model-View-ViewModel** pattern was created by Mcrosoft for WPF framework with YAML originally. You can read more about MVVM [here](https://msdn.microsoft.com/en-us/library/hh848246.aspx)

Thanks for the [Kivy](https://kivy.org/#home) community for creating such awesome framework.
