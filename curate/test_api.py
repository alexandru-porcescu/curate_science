from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.shortcuts import reverse
from django.contrib import auth
import json
from curate import models
from django.conf import settings
import os, shutil

class TestAPIViews(TestCase):
    def setUp(self):
        #create_model_instances()
        self.client = Client()
        admin_user = models.User.objects.create(username='admin')
        admin_user.set_password('password')
        admin_user.is_staff = True
        admin_user.save()

        user = models.User.objects.create(username='new_user')
        user.set_password('password1')
        user.save()

        user = models.User.objects.create(username='new_user_2')
        user.set_password('password2')
        user.save()

        directory = settings.MEDIA_ROOT + '/key_figures/'
        if not os.path.exists(directory):
            os.makedirs(directory)

    def tearDown(self):
        folder = settings.MEDIA_ROOT + '/key_figures/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    # Account Creation
    def test_user_can_create_account(self):
        pass

    # Article tests
    # List Articles
    def test_anon_can_list_articles_api(self):
        self.client=Client()
        article_count = len(models.Article.objects.all())
        url = reverse('api-list-articles')
        r = self.client.get(url)
        d = json.loads(r.content.decode('utf-8'))
        assert(len(d) == article_count)
        assert r.status_code == 200

    def list_articles_for_author(self):
        self.client = Client()
        a = Author.objects.first()
        article_count = len(a.articles.all())
        url = reverse('api-list-articles-for-author', kwargs={'slug': a.slug})
        r = self.client.get(url)
        d = json.loads(r.content.decode('utf-8'))
        assert(len(d) == article_count)
        assert r.status_code == 200

    # View Articles
    def test_anonymous_user_can_view_article_api(self):
        self.client=Client()
        article = models.Article.objects.first()
        url = reverse('api-view-article', kwargs={'pk': article.id})
        r = self.client.get(url)
        assert r.status_code == 200
        assert "title" in r.content.decode('utf-8')

    def test_invalid_article_id_404(self):
        self.client = Client()
        url = reverse('api-view-article', kwargs={'pk': 99999})
        r = self.client.get(url)
        assert r.status_code == 404

    # Create Articles
    def test_authenticated_user_can_create_article_with_api(self):
        self.client.login(username='admin', password='password')
        url = reverse('api-create-article')
        r = self.client.post(url, {
            "doi": "001",
            "year": 2018,
            "journal": "Science",
            "title": "api test article",
            "article_type": "ORIGINAL",
            "research_area": "SOCIAL_SCIENCE",
            "author_list": "LeBel et al",
        })
        a = models.Article.objects.get(doi="001")
        assert a.title == "api test article"

    def test_non_admin_user_create_article_linked_to_author(self):
        self.client.login(username='new_user', password='password1')
        u = User.objects.get(username='new_user')
        author = models.Author.objects.create(user=u, name='New User')
        url = reverse('api-create-article')
        r = self.client.post(url, {
            "doi": "004",
            "year": 2019,
            "journal": "Science",
            "title": "api test article",
            "article_type": "ORIGINAL",
            "research_area": "SOCIAL_SCIENCE",
            "author_list": "LeBel et al",
        })
        article = models.Article.objects.get(doi="004")
        assert article.authors.first().name == 'New User'

    # def test_non_admin_author_can_only_update_own_articles(self):
    #     self.client.login(username='new_user', password='password1')
    #     u = User.objects.get(username='new_user')
    #     author = models.Author.objects.create(user=u, name='New User')
    #     article = models.Article.objects.first()
    #     url = reverse('api-update-article', kwargs={'pk': article.id})
    #     r = self.client.patch(url, {
    #         "title": "api test article updated",
    #     }, content_type="application/json")
    #     assert r.status_code == 403

    def test_create_invalid_article_400(self):
        self.client.login(username='admin', password='password')
        url = reverse('api-create-article')
        r = self.client.post(url, {
            "journal": "Science",
            "title": "api test article",
            "article_type": "ORIGINAL",
            "research_area": "SOCIAL_SCIENCE",
            "authors": [models.Author.objects.first().id,]
        })
        assert r.status_code == 400

    def test_article_year_can_be_in_press(self):
        self.client.login(username='admin', password='password')
        url = reverse('api-create-article')
        r = self.client.post(url, {
            "doi": "000",
            "year": "",
            "in_press": True,
            "author_list": "LeBel et al",
            "journal": "Science",
            "title": "api test article",
            "article_type": "ORIGINAL",
            "research_area": "SOCIAL_SCIENCE",
            "authors": [models.Author.objects.first().id,]
        })
        a = models.Article.objects.get(doi="000")
        assert str(a) == "LeBel et al (In Press) api test article"

    def test_anonymous_user_cannot_create_article_with_api(self):
        self.client=Client()
        url = reverse('api-create-article')
        r = self.client.post(
            url,
            {
                "doi": "002",
                "year": 2018,
                "journal": "Science",
                "title": "api test article 2",
                "article_type": "ORIGINAL",
                "research_area": "SOCIAL_SCIENCE",
                "authors": [models.Author.objects.first().id,]
            },
            content_type="application/json"
        )

        assert r.status_code == 403

    def test_authorized_user_can_get_article_create_form(self):
        self.client.login(username='new_user', password='password1')
        url = reverse('api-create-article')
        r = self.client.get(url)
        assert r.status_code == 200

    def test_admin_can_create_article_nested(self):
        self.client.login(username='admin', password='password')
        url = reverse('api-create-article')
        r = self.client.post(url, {
            "key_figures": [],
            "commentaries": [
                {
                    "authors_year": "Tester (2016)",
                    "commentary_url": "https://curatescience.org/"
                }
            ],
            "authors": [1],
            "doi": "doi test nested create",
            "journal": "",
            "author_list": "Beavis and Butthead",
            "year": 2019,
            "in_press": False,
            "title": "title test nested create",
            "article_type": "ORIGINAL",
            "number_of_reps": 0,
            "research_area": "SOCIAL_SCIENCE"
        })
        assert r.status_code == 201

    # Update Articles
    def test_authenticated_user_can_edit_article_with_api(self):
        self.client.login(username='new_user', password='password1')
        article=models.Article.objects.first()
        user = User.objects.get(username='new_user')
        author = models.Author.objects.create(user=user, name='New User')
        article.authors.add(author)
        url = reverse('api-update-article', kwargs={'pk': article.id})
        r = self.client.patch(
            url, {
                "id": article.id,
                "html_url": "http://www.curatescience.org/"
            },
            content_type="application/json")
        assert r.status_code == 200

    def test_anonymous_user_cannot_edit_article_api(self):
        self.client=Client()
        article=models.Article.objects.first()
        url = reverse('api-update-article', kwargs={'pk': article.id})
        r = self.client.patch(url, {
            "id": article.id,
            "keywords": ["testing"]
        })
        assert r.status_code == 403

    def test_update_invalid_article_id_404(self):
        self.client=Client()
        self.client.login(username='new_user', password='password1')
        url = reverse('api-update-article', kwargs={'pk': 99999})
        r = self.client.put(url, {"title": "_"})
        assert r.status_code == 404

    def test_admin_can_edit_article_nested(self):
        self.client.login(username='admin', password='password')
        article=models.Article.objects.first()
        url = reverse('api-update-article', kwargs={'pk': article.id})
        r = self.client.patch(
            url,
            {
                "id": article.id,
                "commentaries": [
                    {
                        "authors_year": "Test",
                        "commentary_url": "https://www.curatescience.org/",
                    }
                ]
            },
            content_type="application/json")
        assert r.status_code == 200
        assert article.commentaries.first().authors_year == "Test"

    # Delete Articles
    def test_anon_cannot_delete_article_api(self):
        self.client=Client()
        article=models.Article.objects.first()
        url = reverse('api-delete-article', kwargs={'pk': article.id})
        r = self.client.delete(url)
        assert r.status_code == 403

    def test_user_cannot_delete_article_api(self):
        self.client.login(username='new_user', password='password1')
        article=models.Article.objects.first()
        url = reverse('api-delete-article', kwargs={'pk': article.id})
        r = self.client.delete(url)
        assert r.status_code == 403

    def test_admin_can_delete_article_api(self):
        self.client.login(username='admin', password='password')
        url = reverse('api-create-article')
        r = self.client.post(url, {
            "doi": "003",
            "year": 2017,
            "journal": "Science",
            "title": "api test article 3",
            "article_type": "ORIGINAL",
            "research_area": "SOCIAL_SCIENCE",
            "authors": [models.Author.objects.first().id,]
        })
        article = models.Article.objects.get(doi="003")
        url = reverse('api-delete-article', kwargs={'pk': article.id})
        r = self.client.delete(url)
        assert r.status_code == 200
        assert len(models.Article.objects.filter(id=article.id)) == 0

    def test_delete_invalid_article_404(self):
        self.client.login(username='admin', password='password')
        url = reverse('api-delete-article', kwargs={'pk': 9999})
        r = self.client.delete(url)
        assert r.status_code == 404

    # Author tests
    # List Authors
    def test_anon_can_list_authors_api(self):
        self.client=Client()
        author_count = len(models.Author.objects.all())
        url = reverse('api-list-authors')
        r = self.client.get(url)
        d = json.loads(r.content.decode('utf-8'))
        assert(len(d) == author_count)
        assert r.status_code == 200

    # View Authors
    def test_anon_can_view_author_api(self):
        self.client=Client()
        author = models.Author.objects.filter(name='Etienne LeBel').first()
        url = reverse('api-view-author', kwargs={'slug': author.slug})
        r = self.client.get(url)
        assert r.status_code == 200
        assert "LeBel" in r.content.decode('utf-8')

    def test_invalid_author_id_404(self):
        self.client = Client()
        url = reverse('api-view-author', kwargs={'slug': 'foo'})
        r = self.client.get(url)
        assert r.status_code == 404

    # Create Authors
    def test_anon_cannot_create_author_api(self):
        self.client=Client()
        url = reverse('api-create-author')
        r = self.client.post(
            url,
            {
                'name':'test',
            },
            content_type="application/json"
        )

        assert r.status_code == 403

    def test_authorized_user_can_create_author_api(self):
        self.client.login(username='new_user', password='password1')
        url = reverse('api-create-author')
        r = self.client.post(url, {
            "name": "John Tester",
        })
        a = models.Author.objects.get(name="John Tester")
        assert a.name == "John Tester"
        assert a.user.username == "new_user"

    def test_user_with_author_cannot_create_another(self):
        self.client.login(username='new_user_2', password='password2')
        url = reverse('api-create-author')
        r = self.client.post(url, {
            "name": "John Doe",
        })
        a = models.Author.objects.get(name="John Doe")
        assert a.name == "John Doe"
        assert a.user.username == "new_user_2"
        r2 = self.client.post(url, {
            "name": "Jane Doe"
        })
        assert r2.status_code == 403

    def test_associated_user_can_update_author_api(self):
        self.client=Client()
        self.client.login(username='new_user', password='password1')
        url = reverse('api-create-author')
        r = self.client.post(url, {
            "name": "FirstNameTest LastNameTest"
        })
        author=models.Author.objects.get(name="FirstNameTest LastNameTest")
        url = reverse('api-update-author', kwargs={'slug': author.slug})
        r = self.client.patch(
            url, {
                "name": 'Jimmy'
            },
            content_type="application/json")
        assert r.status_code == 200

    def test_other_user_cannot_update_author_api(self):
        self.client=Client()
        self.client.login(username='new_user_2', password='password2')
        author=models.Author.objects.first()
        url = reverse('api-update-author', kwargs={'slug': author.slug})
        r = self.client.patch(url, {
            "id": author.id,
            "name": "test"
        })
        assert r.status_code == 401

    def test_superuser_create_author(self):
        self.client.login(username='admin', password='password')
        url = reverse('api-create-author')
        r = self.client.post(url, {
            "name": "Jill Tester",
        })
        a = models.Author.objects.get(name = "Jill Tester")
        assert a.name == "Jill Tester"
        assert a.user is None

    def test_authorized_user_can_get_author_create_form(self):
        self.client.login(username='new_user', password='password1')
        url = reverse('api-create-author')
        r = self.client.get(url)
        assert r.status_code == 200

    # Update Authors
    def test_anon_cannot_edit_author_api(self):
        self.client=Client()
        author=models.Author.objects.first()
        url = reverse('api-update-author', kwargs={'slug': author.slug})
        r = self.client.patch(url, {
            "id": author.id,
            "name": "test"
        })
        assert r.status_code == 403

    def test_authorized_user_can_patch_author(self):
        self.client.login(username='admin', password='password')
        author=models.Author.objects.first()
        url = reverse('api-update-author', kwargs={'slug': author.slug})
        r = self.client.patch(
            url, {
                "name": 'Jimmy'
            },
            content_type="application/json")
        assert r.status_code == 200

    def test_authorized_user_can_put_author(self):
        self.client.login(username='admin', password='password')
        author=models.Author.objects.first()
        url = reverse('api-update-author', kwargs={'slug': author.slug})
        r = self.client.put(
            url, {
                "name": 'Chen-Bo Zhong',
            },
            content_type="application/json")
        author=models.Author.objects.first()
        assert r.status_code == 200
        assert author.name == 'Chen-Bo Zhong'

    # Delete Authors
    def test_anon_cannot_delete_author_api(self):
        self.client=Client()
        author=models.Author.objects.first()
        url = reverse('api-delete-author', kwargs={'slug': author.slug})
        r = self.client.delete(url)
        assert r.status_code == 403

    def test_user_cannot_delete_author_api(self):
        self.client.login(username='new_user', password='password1')
        author=models.Author.objects.first()
        url = reverse('api-delete-author', kwargs={'slug': author.slug})
        r = self.client.delete(url)
        assert r.status_code == 403

    def test_admin_can_delete_author_api(self):
        self.client.login(username='admin', password='password')
        url = reverse('api-create-author')
        r = self.client.post(url, {
            "name": "John Tester",
        })
        author = models.Author.objects.get(name="John Tester")
        url = reverse('api-delete-author', kwargs={'slug': author.slug})
        r = self.client.delete(url)
        assert auth.get_user(self.client).is_authenticated
        assert auth.get_user(self.client).is_staff
        assert r.status_code == 200
        assert len(models.Author.objects.filter(id=author.id)) == 0

    def test_authorized_user_can_create_key_figure(self):
        client = APIClient()
        client.login(username='new_user', password='password1')
        article = models.Article.objects.first()
        url = reverse('api-create-key-figure', kwargs={'article_pk': article.id})
        f = open('curate/fixtures/image.jpg', mode='rb')
        res = client.put(url, {'file': f})

        assert len(article.key_figures.all()) == 1
        kf = article.key_figures.first()
        assert kf.image is not None
        assert kf.thumbnail is not None
        assert kf.width == 319
        assert kf.height == 400

    def test_unauthorized_cannot_create_key_figure(self):
        client = APIClient()
        article = models.Article.objects.first()
        url = reverse('api-create-key-figure', kwargs={'article_pk': article.id})
        f = open('curate/fixtures/image.jpg', mode='rb')
        res = client.put(url, {'file': f})
        assert res.status_code == 403

    def test_admin_can_delete_key_figure(self):
        client = APIClient()
        client.login(username='admin', password='password')
        article = models.Article.objects.first()
        url = reverse('api-create-key-figure', kwargs={'article_pk': article.id})
        f = open('curate/fixtures/image.jpg', mode='rb')
        res = client.put(url, {'file': f})
        kf = article.key_figures.first()

        url = reverse('api-delete-key-figure', kwargs={'pk': kf.id})
        r = client.delete(url)
        assert r.status_code == 200
        assert len(article.key_figures.all()) == 0

    def test_non_admin_cannot_delete_key_figure(self):
        client = APIClient()
        client.login(username='new_user', password='password1')
        article = models.Article.objects.first()
        url = reverse('api-create-key-figure', kwargs={'article_pk': article.id})
        f = open('curate/fixtures/image.jpg', mode='rb')
        res = client.put(url, {'file': f})
        kf = article.key_figures.first()

        url = reverse('api-delete-key-figure', kwargs={'pk': kf.id})
        r = client.delete(url)
        assert r.status_code == 403

    # def test_article_search(self):
    #     self.client.login(username='new_user', password='password1')
    #     url = reverse('api-search-articles') + "?q=A"
    #     r = self.client.get(url)
    #     d = json.loads(r.content.decode('utf-8'))
    #     assert r.status_code == 200
    #     assert d[0].get('title') == "A brief guide to evaluate replications"

    # def test_article_search_pagination(self):
    #     self.client.login(username='new_user', password='password1')
    #     url = reverse('api-search-articles') + "?q=LeBel&page_size=2"
    #     r = self.client.get(url)
    #     d = json.loads(r.content.decode('utf-8'))
    #     assert r.status_code == 200
    #     assert len(d) == 2
