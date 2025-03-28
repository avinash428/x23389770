from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    home,
    signup,
    login_view,
    user_logout,
    update_charts
)


urlpatterns = [
    path('', home, name='home'),
    path("update-charts/", update_charts, name="update_charts"),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='signin'),
    path('logout/', user_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)