"""HAE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import HAE_DB.views

app_name='HAE_DB'

urlpatterns = [
    path('feed/user/', HAE_DB.views.user_feed_list),
    path('feed/crew/', HAE_DB.views.crew_feed_list),

    path('feed/create/', HAE_DB.views.user_feed_post),
    path('feed/put/<int:feed_ID>/', HAE_DB.views.user_feed_put),
    path('feed/delete/<int:feed_ID>/', HAE_DB.views.user_feed_delete),

    path('feed_comment/<int:feed_ID>/', HAE_DB.views.feed_comment_list),
    path('feed_comment/create/<int:feed_ID>/', HAE_DB.views.feed_comment_post),
    path('feed_comment/put/<int:feed_comment_ID>/', HAE_DB.views.feed_comment_put),
    path('feed_comment/delete/<int:feed_comment_ID>/', HAE_DB.views.feed_comment_delete),

    path('equipment/<str:X_loc>/<str:Y_loc>/<int:distance>/<int:category>/', HAE_DB.views.equipment_list),
    path('equipment/<str:X_loc>/<str:Y_loc>/<int:distance>/', HAE_DB.views.equipment_list),
    path('equipment/create/<str:X_loc>/<str:Y_loc>/<int:category>/', HAE_DB.views.equipment_post),
    path('equipment/delete/<int:equipment_ID>/', HAE_DB.views.equipment_delete),
    path('equipment/judge/', HAE_DB.views.equipment_judge),

    path('crew/', HAE_DB.views.crew_list),
    path('crew/user/', HAE_DB.views.crew_info),
    path('crew/<str:name>/', HAE_DB.views.crew_list),
    path('crew/header/delete/', HAE_DB.views.crew_delete),
    path('crew/user/create/', HAE_DB.views.crew_post),
    path('crew/user/delete/', HAE_DB.views.crew_leave),
    path('crew_header/', HAE_DB.views.check_crew_header),

    path('gathering/create/', HAE_DB.views.gathering_post),
    path('gathering/delete/<int:gathering_ID>/', HAE_DB.views.gathering_delete),
    path('gathering/', HAE_DB.views.gathering_list),

    path('gathering_comment/<int:gathering_ID>/', HAE_DB.views.gathering_comment_list),
    path('gathering_comment/create/<int:gathering_ID>/', HAE_DB.views.gathering_comment_create),
    path('gathering_comment/put/<int:gathering_comment_ID>/', HAE_DB.views.gathering_comment_update),
    path('gathering_comment/delete/<int:gathering_comment_ID>/', HAE_DB.views.gathering_comment_delete),

    path('gathering_participant/<int:gathering_ID>/', HAE_DB.views.gathering_participant_list),
    path('gathering_participant/put/<int:gathering_ID>/', HAE_DB.views.gathering_participate),
    path('gathering_participant/delete/<int:gathering_ID>/', HAE_DB.views.gathering_not_participate),

    path('user/create/', HAE_DB.views.user_post),
    path('user/put/', HAE_DB.views.user_put),
    path('user/', HAE_DB.views.user_profile),
    path('user/crew/put/<int:crew_ID>/', HAE_DB.views.crew_update),
    path('user/login/<str:ID>/<str:password>/', HAE_DB.views.user_login),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)