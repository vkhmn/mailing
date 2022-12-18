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
    )
]