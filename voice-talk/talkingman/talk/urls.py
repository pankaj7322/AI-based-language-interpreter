from django.urls import path
from .views import upload_image
from . import views
from django.urls import path
from .views import login_view
from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home, name='home'),
     path('', login_view, name='login'),
    path('translate/', views.translate_text1, name='translate'),
    path('upload_image/', upload_image, name='upload_image'),
    path('upload_audio/', views.upload_audio, name='upload_audio'),
    path('translate/', views.translate_text, name='translate_text'),
    path('select-language/', views.language_selection, name='select_language'),
    path('language-selection/', views.language, name = "language_selection"),
    path('translation-page/', views.translation_page, name='translation_page'),
    path("home_page",views.home_page, name = "home_page"),
    path('index_selection/', views.index_selection, name='index_selection'),
    path('index/', views.handle_input_selection, name = "handle_input_selection"),
    path('text/', views.text, name= 'text'),
    path('image/', views.image_view, name='image_page'),  # image page view
    path('audio/', views.audio_view, name='audio_page'),

]

