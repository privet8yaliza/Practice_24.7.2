from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
	status, result = pf.get_api_key(email, password)
	
	assert status == 200
	assert "key" in result


def test_get_all_pets_with_valid_key(filter = ""):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.get_list_of_pets(auth_key, filter)

	assert status == 200
	assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name = "LIZA", animal_type = "cat", age = "3", pet_photo = "images/pet_lili.jpg"):
	pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

	assert status == 200
	assert result["name"] == name


def test_successful_delete_self_pet():
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

	if len(my_pets["pets"]) == 0:
		pf.add_new_pet(auth_key, "VOLT", "cat", "8", "images/pet_lili.jpg")
		_, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

		pet_id = my_pets["pets"][0]["id"]
		status, _ = pf.delete_pet(auth_key, pet_id)

		_, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

		assert status == 200
		assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name = "MARUSIA", animal_type = "CAT", age = 8):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

	if len(my_pets["pets"]) > 0:
		status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)

		assert status == 200
		assert result["name"] == name 
	else:
		raise Exception("There is no my pets")



#tests_10

def test_add_info_about_new_pet_without_photo(name = "VOLT", animal_type = "DOG", age = 6):
	_, auth_key = pf.get_api_key(valid_email, valid_password)

	status, result = pf.add_info_about_new_pet_without_photo(auth_key, name, animal_type, age)

	assert status == 200
	assert result["name"] == name


def test_add_photo_of_pet(name = "VOLT", pet_photo = "images/pet_mar.jpg"):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

	for pet in my_pets["pets"]:
		if name == pet["name"]:
			if pet["pet_photo"] == "":
				pet_id = pet["id"]
				break

	status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

	assert status == 200
	assert result["name"] == name


def test_get_api_key_for_invalid_user_password(email = "liz@liz8liza.com", password = "98765"):
	status, _ = pf.get_api_key(email, password)

	assert status == 403


def test_add_info_about_new_pet_without_photo_incorrect_data(name = "LILI", animal_type = "cat", age = -3):
	"""Проверка на создание питомца без фотографии с отрицательным параментом age.
	В данной ситуации выдает ошибку, что status_code должен быть 200, следовательно, это баг,
	который необходимо устранить для корректной и эффективной работы программы."""

	_, auth_key = pf.get_api_key(valid_email, valid_password)

	status, result = pf.add_info_about_new_pet_without_photo(auth_key, name, animal_type, age)

	assert status == 400


def test_add_info_about_new_pet_without_photo_incorrect_auth_key(auth_key = {"key": "ea738148a1f10838e1c5d1413877f3691a3731380e733e877b0ae729"}, name = "LOLO", animal_type = "cat", age = 2):
	status, result = pf.add_info_about_new_pet_without_photo(auth_key, name, animal_type, age)

	assert status == 403


def test_get_list_of_pets_incorrect_auth_key(auth_key = {"key": "ea738148a1f10838e1c5d1413877f3691a3731380e733e877b0ae728"}, filter = ""):
	status, result = pf.get_list_of_pets(auth_key, filter)

	assert status == 403


def test_add_new_pet_incorrect_data(name = "VOLTTY", animal_type = "DOG", age = -8, pet_photo = "images/pet_mar.jpg"):
	"""Проверка на создание питомца без фотографии с отрицательным параментом age.
	В данной ситуации выдает ошибку, что status_code должен быть 200, следовательно, это баг,
	который необходимо устранить для корректной и эффективной работы программы."""

	pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

	assert status == 400


def test_add_new_pet_incorrect_auth_key(auth_key = {"key": "ea738148a1f10838e1c5d1413877f3691a3731380e733e877b0ae720"}, name = "Tony", animal_type = "hamster", age = 1, pet_photo = "images/pet_mar.jpg"):
	pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
	status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

	assert status == 403


def test_add_photo_of_pet_incorrect_data(pet_id = "f3043661-b5a7-41b2-be7c-39e1e3141243", pet_photo = "images/pet_mar.jpg"):
	"""Проверка на добавление фотографии питомца с несуществующим параметром pet_id."""

	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

	assert status == 400


def test_add_photo_of_pet_incorrect_auth_key(auth_key = {"key": "ea738148a1f10838e1c5d1413877f3691a3731380e733e877b0ae720"}, pet_id = "9C4AEC87-37A4-4EE0-8F1B-3170C816536C", pet_photo = "images/pet_mar.jpg"):
	"""Проверка на добавление фотографии с несуществующем auth_key."""

	status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

	assert status == 403


def test_delete_pet_incorrect_auth_key(auth_key = {"key": "ea738148a1f10838e1c5d1413877f3691a3731380e733e877b0ae720"}, pet_id = "9C4AEC87-37A4-4EE0-8F1B-3170C816536C"):
	"""Проверка удаления питомца с несуществующим auth_key."""

	status, result = pf.delete_pet(auth_key, pet_id)

	assert status == 403


def test_update_pet_info_incorrect_data(name = "VOLT", animal_type = "DOG", age = 6, pet_photo = "images/pet_mar.jpg"):
	"""Проверка изменения у существующего питомца параметра animal_type, который принимает тип str.
	В данной ситуации выдает ошибку, что свидетельствует о наличие бага."""

	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

	for pet in my_pets["pets"]:
		if name == pet["name"]:
			if pet["animal_type"] == "DOG":
				pet_id = pet["id"]
				break

	status, result = pf.update_pet_info(auth_key, pet_id, name, "123", age)

	assert status == 400


def test_update_pet_info_incorrect_auth_key(auth_key = {"key": "ea738148a1f10838e1c5d1413877f3691a3731380e733e877b0ae756"}, pet_id = "9C4AEC87-37A4-4EE0-8F1B-3170C816536C", name = "VOLT", animal_type = "DOG", age = 6):
	_, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

	status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

	assert status == 403
