from django.urls import include, path

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter


from .views import (
    AccessTokenCreate,
    FileViewSet,
    FolderContentsView,
    FolderViewSet,
    UserRetrieveDestroyView,
)

router = DefaultRouter()
router.register('files', FileViewSet)
router.register('folders', FolderViewSet)


@api_view(('GET',))
def api(request, _format=None):
    api_root_dict = {}

    list_name = router.routes[0].name
    for prefix, viewset, basename in router.registry:  # noqa pylint: disable=unused-variable
        api_root_dict[prefix] = reverse('api:' + list_name.format(basename=basename),
                                        request=request, format=_format)

    api_root_dict['access_tokens'] = reverse('api:access-token-create',
                                             request=request, format=_format)
    return Response(api_root_dict)


app_name = 'api'
urlpatterns = [
    path('', api, name='root'),
    path('', include(router.urls)),
    path('folders/<int:pk>/contents/', FolderContentsView.as_view()),
    path('access_token/', AccessTokenCreate.as_view(), name='access-token-create'),
    path('users/<int:pk>/', UserRetrieveDestroyView.as_view(), name='cloudstoreuser-detail'),
]
