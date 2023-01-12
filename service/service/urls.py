from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from services.views import SubscriptionView

router = SimpleRouter()
router.register('subscription', SubscriptionView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
