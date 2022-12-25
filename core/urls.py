from django.urls import path
from . import views


urlpatterns = [
    path(
        'api/v1/client/<pk>',
        views.get_delete_update_client,
        name='get_delete_update_client'
    ),
    path(
        'api/v1/clients/',
        views.get_post_clients,
        name='get_post_clients'
    ),
    path(
        'api/v1/mailing/<pk>',
        views.get_delete_update_mailing,
        name='get_delete_update_mailing'
    ),
    path(
        'api/v1/mailings/',
        views.get_post_mailing,
        name='get_post_mailing',
    ),
    path(
        'api/v1/mailing/stat/',
        views.get_common_mailing_stat,
        name='get_common_mailing_stat'
    ),
    path(
        'api/v1/mailing/stat/<pk>',
        views.get_mailing_stat,
        name='get_mailing_stat'
    ),
    path(
        'api/v1/mailings/start/',
        views.start_mailing,
        name='start_mailing'
    )
]