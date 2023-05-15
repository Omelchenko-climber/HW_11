import re

from classes import AddressBook, Name, Phone, Record, Birthday


USERS = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError:
            return 'Check the correctness of the entered data and try again, please.'
        except TypeError:
            return 'Give me the name, please.'
        except KeyError:
            return 'Check the command you entered and try again, please.'
        except IndexError:
            print('Check the command you entered and try again, please.')
            main()
    return inner


@input_error
def add_contact(user_name: str, user_phones: str) -> str:
    name = Name(user_name)
    phone = Phone(user_phones)
    record = Record(name, phone)
    USERS.add_contact(record)
    return f'Contact {user_name} with phone number {user_phones} has been added.'


@input_error
def add_phone(user_name: str, user_phones: str) -> str:
    record = USERS.get_phones(user_name)
    phone = Phone(user_phones)
    record.add_phone(phone)
    return f'Phone number {user_name} has just been added to contact {user_name}'


@input_error
def change_phone(user_name: str, user_phones: str) -> str:
    old_phone, new_phone = user_phones.split()
    record = USERS.get_phones(user_name)
    record.swap_number(old_phone, new_phone)
    return f'The phone number of the user {user_name} with old phone number {old_phone} changed to new {new_phone}.'


@input_error
def delete_phone(user_name: str, user_phones: str) -> str:
    record = USERS.get_phones(user_name)
    record.delete_number(user_phones)
    return f'Phone number {user_phones} has just been deleted from contact {user_name}.'


def add_birthday(user_name: str, user_date: str) -> str:
    if re.match(r"^\d{2}\/\d{2}\/\d{4}$", user_date):
        birthday = Birthday(user_date)
        record = USERS.get_phones(user_name)
        return record.add_birthday(birthday)
    else: return 'Check your input and try again, please.'


def days_to_birthday(user_name: str) -> str:
    record = USERS.get_phones(user_name)
    return record.days_to_birthday()


@input_error
def show_contact(user_name: str) -> str:
    print(USERS.get_phones(user_name))
    return f'{"-" * 30}'


@input_error
def show_contacts(number=1) -> str:
    print(*USERS.show_contacts(number))
    return f'{"-" * 30}'


def close() -> None:
    print('Good bye!')


@input_error
def show_commands() -> None:
    print("""Сommand list (enter the number corresponding to the command you need):
    0 : to show commands,
    1 : to add new contact  (input format: contact phone, contact birthday - optional),
    2 : to add new phone  (input format: Name new_phone),
    3 : to delete the phone  (input format: Name phone_to_delete),
    4 : to change phone  (input format: Name old_phone new_phone),    
    5 : to add birthday  (input format: Name day/month/year),
    6 : to see how many days to some contact birthday (input format: Name)
    7 : to show contact  (input format: Name),
    8 : to show contacts (input format: name and N - numbers of contacts you want to see),
    9 : to close the app""")


COMMANDS = {
    '0': show_commands,
    '1': add_contact,
    '2': add_phone,
    '3': delete_phone,
    '4': change_phone,
    '5': add_birthday,
    '6': days_to_birthday,
    '7': show_contact,
    '8': show_contacts,
    '9': close,
}


def get_user_input(user_command: str) -> str:
    user_input = ''
    if user_command in ['1', '2', '3']:
        user_input = input('Enter the name and the phone, please: ')
    elif user_command == '4':
        user_input = input('Enter the name and the phones, please: ')
    elif user_command == '5':
        user_input = input('Enter the name and birthday: ')
    elif user_command in ['6', '7']:
        user_input = input('Enter the name: ')
    elif user_command == '8':
        user_input = int(input('Enter the quantity of contacts you want to see: '))
    return user_input

@input_error
def main() -> None:
    while True:
        user_command = input('Waiting for command: ')
        if not user_command: show_commands(); continue
        if user_command in COMMANDS:
            if user_command == '0':
                COMMANDS[user_command](); continue
            if user_command == '9':
                COMMANDS['9'](); break
            if user_command in ['6', '7', '8']:
                user_input = get_user_input(user_command)
                print(COMMANDS[user_command](user_input))
                continue
            user_input = get_user_input(user_command)
            input_name, *input_phone = re.split(r'(?=\s[\+0-9])', user_input)
            if input_phone:
                phones = input_phone[0].strip()
                print(COMMANDS[user_command](input_name.capitalize(), phones))
            else:
                print(COMMANDS[user_command](input_name.capitalize()))
        else:
            print('You has just entered wrong number, try again please.')


if __name__ == '__main__':
    show_commands()
    main()


