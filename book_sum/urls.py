
from django.urls import path
from .views import BookSummaryView, CodeComponentView, MovieSynopsisView

urlpatterns = [
    path('summarize/', BookSummaryView.as_view(), name='book-summary'),
    path('code/', CodeComponentView.as_view(), name='code-component'),
    path('movie/', MovieSynopsisView.as_view(), name='movie-synopsis')
]