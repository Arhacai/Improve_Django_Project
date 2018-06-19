from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .forms import MenuForm
from .models import Menu, Item, Ingredient


################
#  TEST VIEWS  #
################
class MenuViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.menu = Menu.objects.create(
            season='Summer',
            expiration_day=timezone.now()
        )
        self.item = Item.objects.create(
            name='Soda',
            description='New designed soda',
            chef=self.user
        )
        self.ingredient = Ingredient.objects.create(
            name='Sugar'
        )

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu:menu_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_item_detail_view(self):
        resp = self.client.get(reverse('menu:item_detail',
                                       kwargs={'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('menu/detail_item.html')

    def test_item_detail_view_404(self):
        resp = self.client.get(reverse('menu:item_detail',
                                       kwargs={'pk': 0}))
        self.assertEqual(resp.status_code, 404)
        self.assertTemplateUsed('menu/detail_item.html')

    def test_create_new_menu_get_view(self):
        resp = self.client.get(reverse('menu:menu_new'))
        self.assertEqual(resp.status_code, 200)

    def test_create_new_menu_post_view(self):
        resp = self.client.post(reverse('menu:menu_new'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_menu_view_GET(self):
        resp = self.client.get(reverse('menu:menu_edit',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_edit_menu_view_POST(self):
        resp = self.client.post(reverse('menu:menu_edit',
                                        kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        self.menu.delete()


#################
#  TEST MODELS  #
#################
class MenuModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.menu = Menu.objects.create(
            season='Summer',
            expiration_day=timezone.now()
        )
        self.item = Item.objects.create(
            name='Soda',
            description='New designed soda',
            chef=self.user
        )
        self.ingredient = Ingredient.objects.create(
            name='Sugar'
        )

    def test_menu_str(self):
        result = str(self.menu)
        self.assertEqual(result, 'Summer')

    def test_item_str(self):
        result = str(self.item)
        self.assertEqual(result, 'Soda')

    def test_ingredient_str(self):
        result = str(self.ingredient)
        self.assertEqual(result, 'Sugar')

    def tearDown(self):
        self.user.delete()
        self.menu.delete()
        self.item.delete()
        self.ingredient.delete()


################
#  TEST FORMS  #
################
class MenuFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.item = Item.objects.create(
            name='Soda',
            description='New designed soda',
            chef=self.user
        )
        self.menu = Menu.objects.create(
            season='Summer',
            expiration_day=timezone.now()
        )

    def test_menu_form_clean_success(self):
        data = {
            'season': 'Summer',
            'items': self.item,
            'expiration_day': '03/04/20'
        }
        form = MenuForm(instance=self.menu, data=data)
        form.is_valid()
        result = form.clean_season()
        self.assertEqual(result, 'Summer')

    def test_menu_form_clean_fail(self):
        form = MenuForm(data={})
        with self.assertRaises(ValidationError):
            form.is_valid()
            form.clean_season()

    def tearDown(self):
        self.user.delete()
        self.item.delete()
