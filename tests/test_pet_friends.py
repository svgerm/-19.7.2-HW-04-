from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet(name='Kusachka', animal_type='dog', age='2', pet_photo="images\pet_photo.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert 'id' in result

def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)


    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Кусачка', animal_type='плюшевая собака', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo(name='Gavkusha', animal_type='dog', age='2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert 'id' in result


def test_add_pet_photo(pet_photo='images/pet_photo.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result


def test_add_new_pet_with_some_data_missing(name='', animal_type='', age='2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    if status != 200:
        raise Exception("Заполните обязательные поля.")
    else:
        assert result["animal_type"] == animal_type

    # Баг: животное должно добавляться только в случае заполнения всех обязательных полей


def test_get_api_key_for_invalid_user(email="ghskd@bk.ru", password="qwerty"):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert "key" not in result


def test_get_api_key_without_credentials(email="", password=""):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert "key" not in result


def test_add_pet_photo_in_jpeg(pet_photo='images/pet_photo.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result


def test_add_pet_photo_in_png(pet_photo='images/pet_photo.png'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result


def test_add_new_pet_with_invalid_age(name='Kusachka', animal_type='dog', age='222', pet_photo="images\pet_photo.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert 'id' in result

    # Баг: значение возраста недопустимо, питомец не должен быть добавлен

def test_add_new_pet_with_invalid_animal_type(name='Sunny', animal_type='dino bones', age='65000000'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert 'id' in result

    # Баг: значение вида животного недопустимо, питомец не должен быть добавлен


def test_add_new_pet_with_too_long_name(name="Gavkusha"*20, animal_type="dog", age="2"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    # Баг: значение имени недопустимо, питомец не должен быть добавлен


def test_delete_any_pet_successful():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    pet_id = pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, pets = pf.get_list_of_pets(auth_key, "")
    assert status == 200
    assert pet_id not in pets.values()
    # Баг: удаление питомца, которого нет в собственном списке питомцев, должно быть недоступно


def test_update_any_pet_info(name="Барбоскин", animal_type="двортерьер", age="4"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    status, result = pf.update_pet_info(auth_key, pets["pets"][0]["id"], name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    # Баг: изменение данных питомца, которого нет в собственном списке питомцев, должно быть недоступно
























