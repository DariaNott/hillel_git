import argparse
import csv
import password_generator as gen

# Task doesn't state if title is unique.
# Case when user tries to save creds for existing title is not handled.
# For the same reason returning password by title returns first occurrence.

csv_file = "data.csv"


def pass_save(title, login, password):
    row_list = [title, login, password]
    file_obj = open(csv_file, 'a', newline='')
    csv_obj = csv.writer(file_obj, lineterminator='\n')
    csv_obj.writerow(row_list)
    file_obj.close()
    print('Password for', title, 'saved!')


def pass_generate(uppercase, symbols, numbers, duplicates, pass_length):
    if uppercase is None:
        uppercase = True
    if symbols is None:
        symbols = False
    if numbers is None:
        numbers = False
    if duplicates is None:
        duplicates = False
    if pass_length is None or pass_length < 8:
        pass_length = 8
    return gen.generate_password(letters=uppercase, symbols=symbols, numbers=numbers, duplicates=duplicates,
                                 pass_length=pass_length)


def get_pass(title):
    file_obj = open(csv_file, 'r')
    dict_reader = csv.DictReader(file_obj)
    for row in dict_reader:
        if row['title'].lower().strip() == title.lower().strip():
            for x in row:
                print(x, row[x], sep=': ')
            return
    print("Password for", title, "not found!")


def get_all_titles():
    file_obj = open(csv_file, 'r')
    dict_reader = csv.DictReader(file_obj)
    titles = []
    for col in dict_reader:
        titles.append(col['title'])
    if len(titles) == 0:
        print('No saved passwords in manager.')
    else:
        print("You've saved passwords for following resources: ", ', '.join(titles))


def main():
    parser = argparse.ArgumentParser(
        description="""Input title; title and login (optional parameters for password); 
        title, login and password or no parameters""")
    parser.add_argument('--title', dest='title', type=str, help='Input your title')
    parser.add_argument('--login', dest='login', type=str, help='Input your login')
    parser.add_argument('--password', dest='password', type=str, help='Input your password')
    # arguments for password generator
    parser.add_argument('--uppercase', dest='uppercase', type=bool,
                        help='True if password to have uppercase letters (optional)')
    parser.add_argument('--symbols', dest='symbols', type=bool, help='True if password to have symbols (optional)')
    parser.add_argument('--numbers', dest='numbers', type=bool, help='True if password to have numbers (optional)')
    parser.add_argument('--duplicates', dest='duplicates', type=bool,
                        help='True if password to have duplicates (optional)')
    parser.add_argument('--pass_length', dest='password_length', type=int, help='Input your password length (optional)')

    args = parser.parse_args()
    if all(value is None for value in vars(args).values()):
        get_all_titles()
    elif args.title is not None and args.login is None and args.password is None:
        get_pass(args.title)
    elif args.title is not None and args.login is not None and args.password is None:
        password = pass_generate(args.uppercase, args.symbols, args.numbers, args.duplicates, args.password_length)
        pass_save(args.title, args.login, password)
    elif args.title is not None and args.login is not None and args.password is not None:
        pass_save(args.title, args.login, args.password)
    else:
        print("Unsupported parameters provided. Please check help.")
        parser.print_help()


if __name__ == '__main__':
    main()
