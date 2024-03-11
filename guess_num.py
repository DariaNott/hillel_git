from random import randint

num = randint(1, 10)
print("Let's play a game! I think of a number from 1 to 10 and you guess it.")
guess = input("Guess a number: ")
if guess.isdecimal() and guess.isalnum():
    print("Your number is ", guess)
    guess = int(guess)
    if guess > 0 and guess < 10:
        if guess == num:
            print("Correct! You won!")
        else:
            print("Ooh, you were so close! My number was ", num)
    else:
        print("Wrong guess. Number should be from 1 to 10! I thought of ", num)
elif any(c.isalpha() for c in guess):
    print("Don't use letters. Game is over.")
elif guess.replace('.', '').isnumeric() or guess.replace(',', '').isnumeric():
    print("Don't use floating point. Game is over.")
else:
    print(guess, "? Let's try again!", sep='')
