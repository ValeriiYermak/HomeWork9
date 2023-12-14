# Змінні

CONTACTS = {}   # Контакти
is_active = True   # Якщо False Бот завершить роботу


# Декоратори


def Handler_command_decorator(func):
    def wrapper(command):
        command = command.lower()
        return func(command)
    return wrapper


def input_error(func):
    def wrapper(*args):
        try:

            return func(*args)
        except IndexError:
            print()
            print("Please provide a name and phone number.")
            return
        except ValueError:
            print('ValueError')
            return
        except KeyError:
            print('This contact is not found.')
            return
    return wrapper


def correct_arguments_decorator(func):
    def wrapper(*args):
        help_number_message = """
---------------------------------------------------------------------------
 The phone number consists of the country code (+38)
 and 10 digits following it.
 The phone number cannot contain letters.
 It can include symbols such as '+', '-', ' ', '(', ')'.
 Examples of phone number formats:
   \u25CF +38(050)40-40-400
   \u25CF +380504040400
   \u25CF 38(050)40-40-400
   \u25CF 380504040400
   \u25CF 38 (050) 40 40 400
   \u25CF 38 050 40 40 400
   \u25CF (050)-40-40-400
   \u25CF 050-40-40-400
   \u25CF 0504040400
   \u25CF 050-40 40-400
Please try again.
---------------------------------------------------------------------------
        """
        args[0][0] = args[0][0].capitalize()
        if args[0][0].isalpha():
            pass
        else:
            print('--------------------------------------------------------')
            print("The name can only consist of letters.\nPlease try again.")
            print('--------------------------------------------------------')
            return
        phone = ' '.join(args[0][1:])
        correct_phone = str(phone)
        correct_phone = correct_phone.replace('(', '')
        correct_phone = correct_phone.replace(')', '')
        correct_phone = correct_phone.replace('-', '')
        correct_phone = correct_phone.replace(' ', '')
        correct_phone = correct_phone.replace('*', '')
        correct_phone = correct_phone.replace('#', '')
        if len(correct_phone) == 10:
            correct_phone = '+38' + correct_phone
        if len(correct_phone) == 12:
            correct_phone = '+' + correct_phone
        if len(correct_phone) < 10 or len(correct_phone) > 13:
            print(help_number_message)
            return
        if correct_phone.startswith('+') and correct_phone[1:].isdigit():
            args[0][1] = correct_phone
        else:
            print(help_number_message)
            return
        return func(*args)
    return wrapper

# Функції


def hello_human():
    print('How can I help you?')


@input_error
@correct_arguments_decorator
def add_name_phone(*args):   # Добавляє новий контакт в словник
    new_contact = {args[0][0]: args[0][1]}
    print('-----------------------------------------------------------------')
    print(f'Contact {new_contact} added: ')
    print('-----------------------------------------------------------------')
    CONTACTS.update(new_contact)


@input_error
@correct_arguments_decorator
def new_phone_number(*args):    # Змінює Номер телефону в словнику
    global CONTACTS
    if args[0][0] in CONTACTS:
        CONTACTS[args[0][0]] = args[0][1]

        print('-------------------------------------------------------------')
        print('The phone number has been changed.')
        print('-------------------------------------------------------------')

# Повертає номер телефону по імені якщо таке існує


@input_error
def return_phone_number(*args):
    name = args[0][0].capitalize()
    global CONTACTS

    if name in CONTACTS:
        print('---------------------------')
        print(f'Phone: {CONTACTS[name]}')
        print('---------------------------')
    else:
        print('---------------------------')
        print('User Not found. try again.')
        print('---------------------------')


def show_list_phone_number():   # Виводить в консоль всі Контакти
    print('List of phone numbers: ')
    for item, value in CONTACTS.items():
        print(item, ' ' + value)


def stop_work():   # Завершує роботу
    print('Good Bye')
    global is_active
    is_active = False

# Команда хелп Виводить на Екран всі команди які вміє виконувати бот


def help_help(*args):
    if len(args[0]) == 0:
        for key in HELP:
            print('--------------------------------------------------------')
            print(HELP[key])
            print('--------------------------------------------------------')
    elif len(args[0]) == 1:
        command = args[0][0]
        if command in HELP:
            print('--------------------------------------------------------')
            print(HELP[command])
            print('--------------------------------------------------------')
        else:
            print('--------------------------------------------------------')
            print('Command not found...')
            print('--------------------------------------------------------')
    elif len(args[0]) > 1:
        command = args[0][0] + ' ' + args[0][1]
        if command in HELP:
            print('--------------------------------------------------------')
            print(HELP[command])
            print('--------------------------------------------------------')
        else:
            print('--------------------------------------------------------')
            print('Command not found...')
            print('--------------------------------------------------------')
# Словник з інформацією про команди


HELP = {
    "help": """The 'help' command provides information about the usage
    of other commands.
Syntax:  'help    |   help [Command]'.
Example: 'help    |   help add'.""",
    "add": """The 'add' command allows you to add a new contact to your
    phone list.
    Syntax: 'add [Name] [Phone]'.
    Example: 'add John 050-40-40-400'.
    This will add a new contact named 'John' with the phone number
    '+380504040400' to your phone list.""",

    "change": """The 'change' command allows you to update the phone number of
    an existing contact in your phone list.
    Syntax: 'change [Name] [New Phone]'.
    Example: 'change John 050-40-40-400'.
    This will update the phone number of the contact named 'John' to
    '+380504040400' in your phone list.""",

    "phone": """The 'phone' command allows you to retrieve the phone number
    of an existing contact from your phone list.
    Syntax: 'phone [Name]'.
    Example: 'phone John'.
    This will show you the phone number of the contact named 'John' from
    your phone list, if it exists.""",
    "show all": """The 'show all' command allows you to display a list of
    all names and phone numbers
    from your phone list.
    Syntax: 'show all'.
This will show you a list of all contacts along with their phone numbers
in your phone list.""",
    "good bye": "The 'good bye' command allows you to exit the bot.",
    "close": "The 'close' command allows you to exit the bot.",
    "exit": "The 'exit' command allows you to exit the bot.",
}

# Словник Команд
OPERATIONS = {
    "help": help_help,
    "hello": hello_human,
    "add": add_name_phone,
    "change": new_phone_number,
    "phone": return_phone_number,
    "show all": show_list_phone_number,
    "good bye": stop_work,
    "close": stop_work,
    "exit": stop_work,
}


#  Хендлер
@Handler_command_decorator
def get_handler(command):
    return OPERATIONS[command]


def main():   # Основний код
    while is_active:
        request = input('Enter Comand:  ').lower()
        command_parts = request.split()
        if command_parts[0] == 'hello':
            command = command_parts[0]
            handler = get_handler(command)
            handler()
        if command_parts[0] == 'add':
            command = command_parts[0]
            arguments = command_parts[1:]
            handler = get_handler(command)
            handler(arguments)
        if command_parts[0] in ['exit', 'close']:
            command = command_parts[0]
            handler = get_handler(command)
            handler()
        if command_parts[0] == 'good' and command_parts[1] == 'bye':
            command = command_parts[0] + ' ' + command_parts[1]
            handler = get_handler(command)
            handler()
        if command_parts[0] == 'show' and command_parts[1] == 'all':
            command = command_parts[0] + " " + command_parts[1]
            handler = get_handler(command)
            handler()
        if command_parts[0] == 'change':
            command = command_parts[0]
            arguments = command_parts[1:]
            handler = get_handler(command)
            handler(arguments)
        if command_parts[0] == 'phone':
            command = command_parts[0]
            arguments = command_parts[1:]
            handler = get_handler(command)
            handler(arguments)
        if command_parts[0] == 'help':
            command = command_parts[0]
            if len(command_parts) > 1:
                arguments = command_parts[1:]
            else:
                arguments = []
            handler = get_handler(command)
            handler(arguments)


if __name__ == "__main__":  # Точка входження
    main()
