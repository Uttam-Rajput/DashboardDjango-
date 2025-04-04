from django.contrib import admin
from django.urls import path, include
from mainApp.views import dashboard_view, get_chart_data, fetch_data, chart,login,signup,average_intensity_chart,average_likelihood_chart,average_relevance_chart
from mainApp.views import unique_topic_chart,unique_regions_chart,fetch_string_data

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', dashboard_view, name='dashboard'),  
    path('api/chart-data/', get_chart_data, name='chart-data'),  
    path('fetch_data/', fetch_data, name='fetch_data'),
    path('chart/', chart, name='chart'),  
    path('django_plotly_dash/', include('django_plotly_dash.urls')),  
    path('login/',login, name='login'),
    path('signup/',signup, name='signup'),
    path('average-intensity/', average_intensity_chart, name='average_intensity_chart'),
    path("average-likelihood/", average_likelihood_chart, name="average_likelihood_chart"),
    path("average-relevance/", average_relevance_chart, name="average_relevance_chart"),
    path('unique-topic-chart/', unique_topic_chart, name='unique-topic-chart'),
    path('unique-regions/', unique_regions_chart, name='unique_regions_chart'),
    path('fetch_string_data/', fetch_string_data, name='fetch_string_data'),

]
