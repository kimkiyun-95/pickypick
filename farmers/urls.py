from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = "farmers"

urlpatterns= [
    path('', views.farmers_page, name='farmers_page'),
    path('farmer_search/', views.farmer_search, name='farmer_search'),

    path('farmer_story_search/', views.farmer_story_search, name='farmer_story_search'),
    path('farmer_story/detail/<int:pk>/', views.Story_Detail.as_view(), name="farmer_story_detail"),
    path('farmer_story/create/', views.farmer_story_create, name='farmer_story_create'), # 추후 url 경로 수정하기
    path('farm_cat_search/', views.farm_cat_search, name='farm_cat_search'),
    path('farmer_detail/<int:pk>/', views.farmer_detail, name='farmer_detail'),

    path('farm_apply/', views.farm_apply, name='farm_apply'),
    path('farm_enroll/<str:step>/', views.FarmEnroll.as_view(), name='farm_enroll'),
]