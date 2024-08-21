from django.contrib.auth import get_user_model

from blog import models

User = get_user_model()


class DataCleaner:
    def _delete_comments(self) -> None:
        models.CommentLike.objects.all().delete()
        models.CommentDislike.objects.all().delete()
        models.Comment.objects.all().delete()

    def _delete_posts(self) -> None:
        models.PostLike.objects.all().delete()
        models.PostDisLike.objects.all().delete()
        models.Post.objects.all().delete()

    def _delete_categories(self) -> None:
        models.Category.objects.all().delete()

    def _delete_users(self) -> None:
        models.Follow.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

    def clean(self):
        self._delete_comments()
        self._delete_posts()
        self._delete_categories()
        self._delete_users()

