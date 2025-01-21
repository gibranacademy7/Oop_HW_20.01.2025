import re
from datetime import datetime


# 1. Define custom error classes
class UserNameTooShortError(Exception):
    pass

class UserNameNonCharError(Exception):
    pass

class IllegalEmailFormatError(Exception):
    pass

class IllegalPasswordFormatError(Exception):
    pass

class IllegalBirthdayError(Exception):
    pass

class UserTooYoungError(Exception):
    pass

###########################################
# 2. Define the User class

class User:
    def __init__(self, name, email, password, birthday):
        # Use setters to validate the values
        self.name = name
        self.email = email
        self.password = password
        self.birthday = birthday  # This will call the setter and validate birthday
        self.__created_at = datetime.now()  # Save the current time when the user is created

    # __int__ method: It could return an ID if needed or any other integer representation
    def __int__(self):
        return hash(self.__name)

##################################

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if len(value) < 4:
            raise UserNameTooShortError("The username must contain at least 4 characters")
        if not any(char.isalpha() for char in value):
            raise UserNameNonCharError("The username must contain at least one alphabetic character")
        self.__name = value


    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value:
            raise IllegalEmailFormatError("The email must contain '@' and a '.'")
        self.__email = value


    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if len(value) < 8:
            raise IllegalPasswordFormatError("The password must contain at least 8 characters")
        if not any(char.islower() for char in value):
            raise IllegalPasswordFormatError("The password must contain at least one lowercase letter")
        if not any(char.isupper() for char in value):
            raise IllegalPasswordFormatError("The password must contain at least one uppercase letter")
        if not any(char in "~!@%$#^&*" for char in value):
            raise IllegalPasswordFormatError("The password must contain at least one special character from ~!@%$#^&*")
        self.__password = value


    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, value):
        # Check if value is a string and convert it to datetime if so
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d")


        # Check if the date is in the future
        if value > datetime.today():
            raise IllegalBirthdayError("The birthday must be in the past")

        # Now set the birthday
        self.__birthday = value

        # Check if the user is older than 20
        age = self.age  # This will now work properly since birthday is set
        if age < 20:
            raise UserTooYoungError("The user must be older than 20 years")

    # Getter for created_at (cannot be set)
    @property
    def created_at(self):
        return self.__created_at

    # Age Getter
    @property
    def age(self):
        today = datetime.today()
        age = today.year - self.__birthday.year
        if today.month < self.__birthday.month or (
                today.month == self.__birthday.month and today.day < self.__birthday.day):
            age -= 1
        return age

    # String representation
    def __str__(self):
        return f"User(name={self.name}, email={self.email}, birthday={self.birthday.strftime('%Y-%m-%d')}, age={self.age}, created_at={self.created_at})"


# 3. Testing with multiple user data
user_data = [
    ("Wisam", "Wisam.Gibran@example.com", "StrongP@ssw0rd", "1990-05-15"),  # Valid user
    ("Yosi", "Yosi.arnheim.com", "password", "2026-01-01"),  # Short name, invalid email, invalid password, future birthday
    ("Peter", "Peter.dorr@example", "MyPass#123", "2003-12-30")  # Invalid email, valid password, user older than 20
]

for name, email, password, birthday in user_data:
    try:
        user = User(name, email, password, birthday)
        print(f"User created successfully: {user}")
    except UserNameTooShortError as e:
        print(f"Error (UserNameTooShortError): {e}")
    except UserNameNonCharError as e:
        print(f"Error (UserNameNonCharError): {e}")
    except IllegalEmailFormatError as e:
        print(f"Error (IllegalEmailFormatError): {e}")
    except IllegalPasswordFormatError as e:
        print(f"Error (IllegalPasswordFormatError): {e}")
    except IllegalBirthdayError as e:
        print(f"Error (IllegalBirthdayError): {e}")
    except UserTooYoungError as e:
        print(f"Error (UserTooYoungError): {e}")
    print("-" * 50)
