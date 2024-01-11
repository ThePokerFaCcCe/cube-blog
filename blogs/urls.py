from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"comments", views.CommentViewSet, basename="comment")
urlpatterns = router.urls
