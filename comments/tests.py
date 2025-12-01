from rest_framework import status
from rest_framework.test import APITestCase

from comments.factories import CommentFactory
from posts.factories import PostFactory
from users.factories import UserFactory


class CommentAPITestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.post = PostFactory(author=self.user)

    def test_create_comment(self):
        url = f"/api/v1/posts/{self.post.id}/comments/"
        response = self.client.post(
            url,
            {"content": "Comentário de teste"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user.id)

    def test_list_comments(self):
        CommentFactory(user=self.user, post=self.post)
        url = f"/api/v1/posts/{self.post.id}/comments/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
