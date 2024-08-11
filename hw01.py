from collections import UserDict
from datetime import datetime, timedelta
class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    @Field.value.setter
    def value(self, value):
        if value:
            self._value = value
        else:
            raise ValueError('Name cannot be empty')

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone number must contain 10 digits')
        self._value = value

class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def show_bd(self):
        return f"Date of birthday {self.birthday.value.strftime('%d.%m.%Y')}"

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(f"Error adding phone: {e}")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True  # Повертаємо True, якщо телефон видалено
        return False  # Повертаємо False, якщо телефон не знайдено

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                try:
                    self.phones[i] = Phone(new_phone)
                    return True  # Повертаємо True, якщо телефон змінено
                except ValueError as e:
                    print(f"Error editing phone: {e}")
        return False  # Повертаємо False, якщо телефон не знайдено

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_date):
        try:
            self.birthday = Birthday(birthday_date)
        except ValueError as e:
            print(f"Error adding birthday: {e}")
            
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()
        for user in self.data.values():
            if user.birthday == None:
                continue
            birthday = user.birthday.value
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            days_until_birthday = (birthday_this_year - today).days
            if 0 <= days_until_birthday <= 7:
                congratulation_date = birthday_this_year + timedelta(days=(7 - birthday_this_year.weekday()) % 7)
                upcoming_birthdays.append({"name": user.name.value, "congratulation_date": congratulation_date.strftime("%Y.%m.%d")})
        return upcoming_birthdays

book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday('12.08.1999')
# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555, congratulation_date: 12.08.1999

found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")
print(book.get_upcoming_birthdays())
