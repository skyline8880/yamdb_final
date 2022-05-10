from django.urls import include, path
from rest_framework import routers

from .views import (APIToken, CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUp, TitleViewSet, UserViewSet)

app_name = "api"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

authorization = [
    path("signup/", SignUp.as_view()),
    path("token/", APIToken.as_view()),
]

urlpatterns = [
    path("v1/auth/", include(authorization)),
    path("v1/", include(router.urls)),
]
