from collections import UserDict
from datetime import datetime, date
import re


class Field:
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @Field.value.setter
    def value(self, value):
        if re.match(r"^[a-zA-Z]{3,}$", value):
            Field.value.fset(self, value)
        else:
            raise ValueError('The name must be longer than one letter and not contain numbers!')

    def __repr__(self) -> str:
        return f'{self.value}'


class Phone(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @Field.value.setter
    def value(self, value):
        if re.match(r"\b\d{10}\b|\+?\d{12}\b", value):
            Field.value.fset(self, value)
        else:
            raise ValueError('Incorrect phone number input, check it and try again, please!')

    def __repr__(self) -> str:
        return f'{self.value}'


class Birthday(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @Field.value.setter
    def value(self, value):
        curr_date = datetime.today().date()
        birthday_date = datetime.strptime(value, '%d/%m/%Y').date()
        if curr_date.replace(year=curr_date.year - 100) <= birthday_date < curr_date.replace(year=curr_date.year - 8):
            Field.value.fset(self, value)
        else:
            raise ValueError('Incorrect birthday input, check it and try again, please!')

    def __repr__(self) -> str:
        return f'{self.value}'


class Record:
    def __init__(self, name: Name, phone: Phone | str = None, birthday: Birthday | str = None) -> None:
        self.name = name
        self.phones = []
        if phone is not None:
            self.add_phone(phone)
        if birthday is None:
            self.birthday = f'Birthday for contact {self.name} is not defined yet .'
        self.birthday = birthday

    def add_phone(self, phone: Phone | str) -> None:
        if isinstance(phone, str):
            phone = self.create_phone(phone)
        self.phones.append(phone)

    def add_birthday(self, birthday: Birthday | str):
        if self.birthday is None:
            self.birthday = birthday
            return f'Add birthday record {birthday} to contact {self.name}.'
        else:
            return f'Contact {self.name} has already had birthday record.'

    def create_phone(self, phone: str) -> Phone:
        return Phone(phone)

    def swap_number(self, old_phone, new_phone) -> str:
        for number in self.phones:
            if number.value == old_phone:
                number.value = new_phone
                return number

    def delete_number(self, phone: str) -> str:
        for number in self.phones:
            if number.value == phone:
                self.phones.remove(number)
                return number

    def show_phones(self) -> None:
        for index, phone in enumerate(self.phones, 1):
            print(f'{index}: {phone.value}')

    def show_birthday(self) -> None:
        if self.birthday:
            print(f'{self.birthday}')
        else:
            print(f'Birthday for contact {self.name} is not defined yet .')

    def get_phone(self, inx) -> list:
        return self.phones[inx - 1]

    def days_to_birthday(self) -> str:
        if self.birthday:
            date_of_birthday = datetime.strptime(str(self.birthday), '%d/%m/%Y').date()
            birthday_date_next = date_of_birthday.replace(year=date.today().year + 1)
            if date_of_birthday.replace(year=date.today().year + 1) < date.today():
                timedelta = birthday_date_next - date.today()
            else:
                timedelta = birthday_date_next - date.today()
            return f'{self.name}`s next birthday will be in {str(timedelta).split(", ")[0]}.'
        else:
            return f'For contact {self.name} you didn`t set birthday yet.'

    def get_name(self) -> str:
        return self.name.value

    def __str__(self) -> str:
        return f"name: {self.name}, phones: {', '.join(str(number) for number in self.phones)}, birthday: {self.birthday}"

    def __repr__(self) -> str:
        return f"Record({self.name!r}: {self.phones!r}, {self.show_birthday()})"


class AddressBook(UserDict):
    def __init__(self, record: Record | None = None) -> None:
        self.data = {}
        if record is not None:
            self.add_contact(record)

    def get_phones(self, name: str) -> str:
        return self.data[name]

    def add_contact(self, record: Record) -> None:
        self.data[record.get_name()] = record

    def show_contacts(self, how_many: int) -> None:
        count = 1
        if self.data:
            for name in self.data.keys():
                yield f'{self.get_phones(name)}'
                if count >= how_many: break
                count += 1
        else:
            print("You haven't any contacts yet.")

