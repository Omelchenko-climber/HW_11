from collections import UserDict


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f'{self.value}'


class Phone(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f'{self.value}'


class Record:
    def __init__(self, name: Name, phone: Phone | str = None) -> None:
        self.name = name
        self.phones = []
        if phone is not None:
            self.add_phone(phone)

    def add_phone(self, phone: Phone | str) -> None:
        if isinstance(phone, str):
            phone = self.create_phone(phone)
        self.phones.append(phone)

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


    def show(self) -> None:
        for inx, p in enumerate(self.phones, 1):
            print(f'{inx}: {p.value}')

    def get_phone(self, inx) -> list:
        return self.phones[inx - 1]

    def get_name(self) -> str:
        return self.name.value

    def __str__(self) -> str:
        return f"name: {self.name}, phones: {', '.join(str(number) for number in self.phones)}"

    def __repr__(self) -> str:
        return f"Record({self.name!r}: {self.phones!r})"


class AddressBook(UserDict):
    def __init__(self, record: Record | None = None) -> None:
        self.data = {}
        if record is not None:
            self.add_contact(record)

    def add_contact(self, record: Record) -> None:
        self.data[record.get_name()] = record

    def show_contacts(self) -> None:
        if self.data:
            for name, record in self.data.items():
                print(f'{name}:')
                record.show()
        else: print("You haven't any contacts yet.")

    def get_phones(self, name: str) -> None:
        return self.data[name]