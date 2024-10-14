from django.urls import path, include


urlpatterns = [

    # path('', include('assistant.urls')),
    path('user/', include('user.urls')),
    path('admin/', include('admin.urls')),
]
