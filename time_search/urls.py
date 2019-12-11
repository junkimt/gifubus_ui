from django.urls import path

from . import views

app_name = 'time_search'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('result/', views.SearchResultView.as_view(), name='result'),
    path('guideline/', views.GuideLineView.as_view(), name='guideline'),
    path('analysis/', views.AnalysisView.as_view(), name='analysis'),
]
