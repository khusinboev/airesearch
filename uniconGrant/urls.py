"""intelsoft URL Configuration

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
from django.contrib import admin
from django.urls import path
from contentanalyze.views import index, statistic, about, mail, programService, electronicService, modelingService
from contentanalyze.views import semanticTahlil, contact, service, education, hardwareProducts, simulationProducts, tutorialProducts
from django.conf import settings
import contentanalyze.views as vw_ca
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("about", about),
    path("mail", mail),
    path("programService", programService),
    path("electronicService", electronicService),
    path("modelingService", modelingService),
    path("contact", contact),
    path("service", service),
    path("education", education),
    path("hardwareProducts", hardwareProducts),
    path("simulationProducts", simulationProducts),
    path("tutorialProducts", tutorialProducts),
    path("statistic", statistic),
    path("semantic", semanticTahlil),
    path("sohalar", vw_ca.show_sohalar),
    path("lugat", vw_ca.show_lugat),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# path("import_l22", vw_ca.import_L22),
# path("import_l1", vw_ca.import_l1),
# path("import_l2", vw_ca.import_l2),
# path("import_l4", vw_ca.import_l4),
# path("import_l5", vw_ca.import_l5),
# path("import_l6", vw_ca.import_l6),
# path("import_l8", vw_ca.import_l8),
# path("import_l9", vw_ca.import_l9),
# path("import_l10", vw_ca.import_l10),
# path("import_l11", vw_ca.import_l11),
# path("import_l12", vw_ca.import_l12),
# path("import_l13", vw_ca.import_l13),
# path("import_l14", vw_ca.import_l14),
# path("import_l15", vw_ca.import_l15),
# path("import_l16", vw_ca.import_l16),
# path("import_l17", vw_ca.import_l17),
# path("import_l18", vw_ca.import_l18),
# path("import_l19", vw_ca.import_l19),
# path("import_l20", vw_ca.import_l20),
# path("import_l21", vw_ca.import_l21),
# path("import_l23", vw_ca.import_l23),
# path("import_l24", vw_ca.import_l24),
# path("import_l25", vw_ca.import_l25),
