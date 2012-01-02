from mongoengine.django.auth import User
from todoy.conftest import override_settings

def test_valid_register(mc):
    assert len(User.objects.all()) == 1
    response = mc.client.get("/accounts/register/")
    assert response.status_code == 200
    response = mc.client.post("/accounts/register/",
            {'username': 'hu',
                'password': 'portish',
                'password_confirm': 'portish',
                'email': 'hu@example.com'})
    assert response.status_code == 302
    assert response['location'] == 'http://testserver/accounts/login/'
    assert len(User.objects.all()) == 2
    assert User.objects.get(username="hu").email == 'hu@example.com'

def test_passwords_no_match(mc):
    response = mc.client.post("/accounts/register/",
            {'username': 'hu',
                'password': 'portish',
                'password_confirm': 'portisk',
                'email': 'hu@example.com'})
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'] == [u"The passwords do not match"]

def test_duplicate_name(mc):
    '''test_user is created on the mc funcarg'''
    response = mc.client.post("/accounts/register/",
            {'username': 'test_user',
                'password': 'portish',
                'password_confirm': 'portish',
                'email': 'bob@example.com'})
    assert response.status_code == 200
    assert response.context['form'].errors['username'] == ["The user test_user already exists"]

def test_registration_disabled(mc):
    with override_settings(DISABLE_REGISTRATION=True):
        response = mc.client.get("/accounts/register/")
    assert response.status_code == 403