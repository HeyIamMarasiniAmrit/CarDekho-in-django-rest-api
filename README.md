i'm curently learning restapi this project im building just for learning
Django REST framework (DRF) is a powerful toolkit for building web APIs with Django. Here's a structured overview of everything you need to know:

1. Setting Up Django REST Framework (DRF)
Install Django and DRF:

bash
Copy
Edit
pip install django djangorestframework
Add rest_framework to INSTALLED_APPS in settings.py:

python
Copy
Edit
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Add this
]
2. Creating a Basic API
(a) Define a Django Model
Create a models.py file inside an app:

python
Copy
Edit
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title
Run migrations:

bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
(b) Create a Serializer
Serializers convert Django models into JSON data and vice versa.
Create serializers.py:

python
Copy
Edit
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
(c) Create API Views
Use Django REST framework’s class-based views (CBVs) or function-based views (FBVs).

Using APIView (Class-based View)
Create views.py:

python
Copy
Edit
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer

class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
Using ViewSets & Routers (More Efficient)
python
Copy
Edit
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
(d) Define URLs
Create urls.py:

python
Copy
Edit
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
3. Authentication & Permissions
DRF provides built-in authentication and permission classes:
Modify settings.py:

python
Copy
Edit
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
To use token authentication:

bash
Copy
Edit
pip install djangorestframework-simplejwt
Add JWT authentication:

python
Copy
Edit
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
]
Generate a token:

bash
Copy
Edit
python manage.py migrate
python manage.py createsuperuser
4. Filtering, Searching, and Pagination
Filtering
Install Django filters:

bash
Copy
Edit
pip install django-filter
Modify settings.py:

python
Copy
Edit
INSTALLED_APPS += ['django_filters']
REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'] = ['django_filters.rest_framework.DjangoFilterBackend']
Use filters in a view:

python
Copy
Edit
from django_filters.rest_framework import DjangoFilterBackend

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'published_date']
Searching
Add search functionality:

python
Copy
Edit
from rest_framework.filters import SearchFilter

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author']
Pagination
Modify settings.py:

python
Copy
Edit
REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'rest_framework.pagination.PageNumberPagination'
REST_FRAMEWORK['PAGE_SIZE'] = 10
5. Handling File Uploads
Modify models.py:

python
Copy
Edit
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
Modify serializers.py:

python
Copy
Edit
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
Ensure MEDIA_URL is set in settings.py:

python
Copy
Edit
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
Update urls.py:

python
Copy
Edit
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
6. Deploying Django REST API
(a) Use Gunicorn & Nginx
Install Gunicorn:

bash
Copy
Edit
pip install gunicorn
Run the server:

bash
Copy
Edit
gunicorn project_name.wsgi:application
(b) Use Docker for Deployment
Create a Dockerfile:

dockerfile
Copy
Edit
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "project_name.wsgi:application", "--bind", "0.0.0.0:8000"]
Build and run:

bash
Copy
Edit
docker build -t django_api .
docker run -p 8000:8000 django_api
7. Advanced Concepts
(a) Caching with Redis
bash
Copy
Edit
pip install django-redis
Modify settings.py:

python
Copy
Edit
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
(b) Celery for Asynchronous Tasks
bash
Copy
Edit
pip install celery
Modify settings.py:

python
Copy
Edit
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
Create tasks.py:

python
Copy
Edit
from celery import shared_task

@shared_task
def add(x, y):
    return x + y
Run Celery worker:

bash
Copy
Edit
celery -A project_name worker --loglevel=info



![Screenshot 2025-01-08 144649](https://github.com/user-attachments/assets/585879c8-a726-4592-ab96-d85a7afda9af)

![Image](https://github.com/user-attachments/assets/940286ac-4c24-4651-ae6e-88a7998870c5)

![Image](https://github.com/user-attachments/assets/028c27a9-eef0-45e7-abe6-889edf3c5fcb)

admin 
![Image](https://github.com/user-attachments/assets/46930292-3157-4d0c-9236-0553e84709bf)


test on api in postman
![Image](https://github.com/user-attachments/assets/83e57b14-5273-4d3a-bace-fb9d78e4f7e4)

![Image](https://github.com/user-attachments/assets/83e57b14-5273-4d3a-bace-fb9d78e4f7e4)


username , email  password gernerated check in postman
![Image](https://github.com/user-attachments/assets/d2928250-7e16-4687-95b0-85a9c1eceacf)


![Image](https://github.com/user-attachments/assets/d2928250-7e16-4687-95b0-85a9c1eceacf)




use JWT JSON Web Tokens
Authorization: This is the most common scenario for using JWT. Once the user is logged in, each subsequent request will include the JWT, allowing the user to access routes, services, and resources that are permitted with that token. Single Sign On is a feature that widely uses JWT nowadays because of its small overhead and its ability to be easily used across different domains.
Information Exchange: JSON Web Tokens are a good way of securely transmitting information between parties. Because JWTs can be signed—for example, using public/private key pairs—you can be sure the senders are who they say they are. Additionally, as the signature is calculated using the header and the payload, you can also verify that the content hasn't been tampered with
