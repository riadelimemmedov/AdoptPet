"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# !Django Modules
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerSplitView

# !Abstract
from abstract.constants import AppName
from abstract.views import *

# *Admin Site Configuration
admin.site.site_header = _("Adopt Pet")  # login page
admin.site.site_title = _("AdopetPet Admin User")  # html <title> tag
admin.site.index_title = _("Welcome My AdoptPet Project")  # site administration

urlpatterns = []

if not settings.APP_NAME or settings.APP_NAME not in [app.value for app in AppName]:
    raise Exception(_("Please set app correct name same as abstract.constants.AppName"))


if settings.APP_NAME == AppName.ADMIN.name:
    # Only for admin
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        path("jet/", include("jet.urls", "jet")),
        path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
        path("api/schema", SpectacularAPIView.as_view(), name="schema_api"),
        path(
            "api/schema/docs",
            SpectacularSwaggerSplitView.as_view(url_name="schema_api"),
        ),
    ]
    urlpatterns += i18n_patterns(path("admin/", admin.site.urls))
    # urlpatterns += [path("users/", include("apps.users.urls", namespace="users"))]
    urlpatterns += [path("upload/", include("apps.upload.urls", namespace="upload"))]
    urlpatterns += [path("pets/", include("apps.pet.urls", namespace="pet"))]
    urlpatterns += [path("orders/", include("apps.order.urls", namespace="order"))]
    urlpatterns += [
        path("transactions/", include("apps.transaction.urls", namespace="transaction"))
    ]


# *Settings Debug
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
