from django.urls import path
from . import views

urlpatterns = [
    path('get-document/<path:page_url>/', views.get_document, name='get_document'),
    path('create-documentation/', views.create_documentation, name='create_documentation'),
    path('edit-documentation/<int:pk>/', views.edit_documentation, name='edit_document'),
    path('all-documentation/', views.AllDocumentation.as_view(), name='all_documentation'),
    path('add-documentation/', views.add_documentation, name='add_documentation'),
    path('view/<slug:slug>/', views.view_document, name='documentation'),
    path('history/<int:pk>/', views.HistoryView.as_view(), name='view_history'),
    path('history/<int:pk>/revert/<int:history_id>', views.revert_history, name='revert_history'),
    path('history/<int:pk>/view/<int:history_id>', views.view_history_document, name='view_history_document'),
]