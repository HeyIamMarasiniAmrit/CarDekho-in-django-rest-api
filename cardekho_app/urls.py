from django.urls import path
from . import views

urlpatterns = [
    path('list', views.car_list_view, name='car_list'),
    path('<int:pk>', views.car_detail_view, name='car_detail'),
    path('Showroom', views.Showroom_view.as_view(), name='showroom_view'),
    path('Showroom/<int:pk>', views.showroom_details.as_view(), name='showroom_details'),  # Added this
    path('showroom/<int:pk>', views.showroom_details.as_view(), name='showroom_details'),
    path('review',views.Reviewlist.as_view(),name='review_list'),
    path('review/<int:pk>',views.ReviewDetails.as_view(),name='review_detail'),
]
