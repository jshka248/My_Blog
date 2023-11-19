from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    prefix_default_language=True,  
    # 기본 언어 URL에 언어 접두사 보이기 설정
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
