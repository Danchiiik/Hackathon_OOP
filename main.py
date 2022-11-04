import json


class RegisterMixin:
    def register(self, name, password):
        with open('user.json') as file:
            data = json.load(file)
            if name in [i['name'] for i in data]:
                raise Exception('Такой юзер уже существует!')
            else:
                try:
                    maxid = max([i['id'] for i in data ])
                except ValueError:
                    maxid = 0
                
                data.append({
                'id': maxid + 1,
                'name': name,
                'password': password
                }) 
        
        with open('user.json', 'w') as file:
            json.dump(data, file)
            return 'Successfully registered'

    
class LoginMixin:
    def login(self, name, password):
        with open('user.json') as file:
            data = json.load(file)

        if name not in [i['name'] for i in data]:
            raise Exception('Нет такого юзера в БД!')
        if password == [i['password'] for i in data if i['name'] == name][0]:
            return 'Вы успешно залогинились!'
        else:    
            raise Exception('Неверный пароль!')
        

class ChangePasswordMixin:
    def change_password(self, name, old_password, new_password):
        with open('user.json') as file:
            data = json.load(file)
            
        if old_password == [i['password'] for i in data if i['name'] == name][0]:
            data[data.index([i for i in data if i['name'] == name][0])]['password'] = validate_password(new_password)
       
            with open('user.json', 'w') as file:
                json.dump(data, file)
                return 'Password changed successfully!'
        else:
            raise Exception('Старый пароль указан не верно!')
            
               
class ChangeUserNameMixin:
    def change_name(self, old_name, new_name):
        with open('user.json') as file:
            data = json.load(file)
        
        if old_name in [i['name'] for i in data if i['name'] == old_name]:
            while new_name in [i['name'] for i in data if i['name'] == new_name]:
                print('Пользователь с таким именем уже существует!')
                new_name = input('Enter another name: ')
            data[data.index([i for i in data if i['name'] == old_name][0])]['name'] = new_name
        
            with open('user.json', 'w') as file:
                json.dump(data, file)
                return 'Username changed successfully!'
        else:
            raise Exception('Нет такого зарегистрированного юзера в БД!')
            
    
class CheckOwnerMIxin:
    def check(self, owner): 
        with open('user.json') as file:
            data = json.load(file)
              
        if owner in [i['name'] for i in data]:
            print('Post created')
        else:
            raise Exception('Нет такого пользователя!')
    


class User(RegisterMixin, LoginMixin, ChangePasswordMixin, ChangeUserNameMixin):
    def __init__(self, name, password) -> None:
        self.name = name
        self.password = validate_password(password)
        
    def register(self):
        return super().register(self.name, self.password)
    
    def login(self):
        return super().login(self.name, self.password)
    
    
def validate_password(password):
    if len(password)<8:
        raise Exception('Пароль слишком короткий!')
    if password.isalpha() or password.isdigit():
        raise Exception('Пароль должен состоять из букв и цифр!')
    return password
        

class Post(CheckOwnerMIxin):
    def __init__(self, title, description, price, quantity, owner) -> None:
        self.title = title
        self.descripton = description
        self.price = price
        self.quantity = quantity
        self.owner = self.check(owner)
        
        
obj1 = User('Dan', '1234567a')
# print(obj1.register())
# print(obj1.login())
# print(obj1.change_password('Dan' , '1234567a', '1234aaaa'))
# print(obj1.change_name('Dan', 'Daniel'))
# photo = Post('name', 'des', 100, 5, 'Daniel')


        