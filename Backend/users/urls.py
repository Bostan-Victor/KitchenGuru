from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("profile", views.ProfileView.as_view()),
    path('add-to-watch-list', views.AddWatchListView.as_view(), name='add-to-watch-list'),
    path('recent-recipes', views.RecentRecipesView.as_view(), name='recent-recipes'),
    path("update-avatar", views.UpdateAvatarView.as_view()),
    path('update-username', views.UpdateUsernameView.as_view()),
    path('update-email', views.UpdateEmailView.as_view())
]
