import random

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
from tqdm import tqdm

from blog import models

User = get_user_model()


class DataPopulate:
    def __init__(self):
        self.fake = Faker()
        self.users: list[User] = []

    def _create_categories(self, count: int = 10) -> None:
        for _ in tqdm(range(count), desc='Creating categories'):
            name = self.fake.word()
            models.Category.objects.create(
                name=name,
                slug=slugify(name)
            )

    def _create_users(self, count: int = 10) -> None:
        for _ in tqdm(range(count), desc='Creating users'):
            user = User.objects.create_user(
                username=self.fake.user_name(),
                email=self.fake.email(),
                password='password123'
            )
            self.users.append(user)

    def _create_posts(self, count: int = 50) -> None:
        categories = models.Category.objects.all()
        for _ in tqdm(range(count), desc='Creating posts'):
            title = self.fake.sentence()
            publish = timezone.make_aware(self.fake.date_time_this_year())
            post = models.Post.objects.create(
                title=title,
                slug=slugify(title),
                author=random.choice(self.users),
                body=self.fake.text(),
                publish=publish,
                image_url=self.get_image_url(),
                category=random.choice(categories),
                status=random.choice(['d', 'p'])
            )
            self._create_comments(post)
            self._create_post_likes_dislikes(post)

    def _create_comments(self, post: models.Post, count: int = 10) -> None:
        for _ in tqdm(range(count), desc=f'Creating  comments for post: {post.id}'):
            comment = models.Comment.objects.create(
                post=post,
                author=random.choice(self.users),
                body=self.fake.paragraph(),
            )
            self._create_comment_likes_dislikes(comment)

    def _create_post_likes_dislikes(self, post: models.Post, count: int = 10) -> None:
        for _ in tqdm(range(count), desc=f'Creating Like/Dislike for post: {post.id}'):
            user = random.choice(self.users)
            if random.choice([True, False]):
                if not models.PostLike.objects.filter(post=post, user=user).exists():
                    models.PostLike.objects.create(
                        post=post,
                        user=user
                    )
            else:
                if not models.PostDisLike.objects.filter(post=post, user=user).exists():
                    models.PostDisLike.objects.create(
                        post=post,
                        user=user
                    )

    def _create_comment_likes_dislikes(self, comment: models.Comment, count: int = 10) -> None:
        for _ in tqdm(range(count), desc=f'Creating Like/Dislike for comment: {comment.id}'):
            user = random.choice(self.users)
            if random.choice([True, False]):
                if not models.CommentLike.objects.filter(comment=comment, user=user).exists():
                    models.CommentLike.objects.create(
                        comment=comment,
                        user=user
                    )
            else:
                if not models.CommentDislike.objects.filter(comment=comment, user=user).exists():
                    models.CommentDislike.objects.create(
                        comment=comment,
                        user=user
                    )

    def _create_follow(self, count: int = 20) -> None:
        for _ in tqdm(range(count), desc=f'Creating follows'):
            follower = random.choice(self.users)
            followed = random.choice([user for user in self.users if user != follower])
            models.Follow.objects.get_or_create(follower=follower, followed=followed)

    @staticmethod
    def get_image_url() -> str:
        return f'https://picsum.photos/seed/{random.randint(1, 1000)}/1280/720'

    def populate(self) -> None:
        self._create_categories()
        self._create_users()
        self._create_posts()
        self._create_follow()
