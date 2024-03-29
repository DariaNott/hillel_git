import argparse
import csv
import password_generator as gen

csv_file = "data.csv"


def pass_save(title, login, password):
    row_list = [title, login, password]
    pass_exists = check_pass_exist(title, login)
    if pass_exists:
        print("Password for", title, "with login", login, "already exists. Do you want to update password? (Yes/No)")
        answer = input()
        if answer.lower() == 'yes':
            file_obj = open(csv_file, 'r')
            reader = csv.reader(file_obj)
            rows_keep = [line for line in reader if
                         line[0].lower().strip() != title.lower().strip() and line[1] != login]
            file_obj = open(csv_file, 'w', newline='')
            writer = csv.writer(file_obj, lineterminator='\n')
            rows_keep.append(row_list)
            for row in rows_keep:
                writer.writerow(row)
            print("Password for", title, "with login", login, "updated.")
        else:
            print("No changes saved.")
    else:
        file_obj = open(csv_file, 'a', newline='')
        csv_obj = csv.writer(file_obj, lineterminator='\n')
        csv_obj.writerow(row_list)
        file_obj.close()
        print('Password for', title, 'saved!')


def check_pass_exist(title, login):
    results = get_data(title)
    if results:
        for row in results:
            if row['login'] == login:
                return True
    else:
        return False


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
    results = get_data(title)
    print("You have saved passwords for ", len(results), title, "accounts:\n")
    if results:
        for row in results:
            for x in row:
                print(x, row[x], sep=': ')
            print('')
    else:
        print("Password for", title, "not found!")


def get_data(title):
    file_obj = open(csv_file, 'r')
    dict_reader = csv.DictReader(file_obj)
    results = []
    for row in dict_reader:
        if row['title'].lower().strip() == title.lower().strip():
            results.append(row)
    return results


def get_all_titles():
    file_obj = open(csv_file, 'r')
    dict_reader = csv.DictReader(file_obj)
    titles = set()
    for col in dict_reader:
        titles.add(col['title'])
    if not titles:
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