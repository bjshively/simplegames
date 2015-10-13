import urllib2
import re

# retrieves a word to play with from a random word API
def get_word():
    print "...Getting your word..."
    response = urllib2.urlopen("http://randomword.setgetgo.com/get.php")
    word = response.read().strip()
    return word

def get_guess():
    guess = raw_input("Guess a letter: ")
    guess = guess.strip().lower()
    return guess

def valid_guess(current_guess):
    if(len(current_guess) != 1):
        return False
    elif(current_guess not in 'abcdefghijklmnopqrstuvwxyz'):
        return False
    else:
        return True

def update_guess(current_guess, word_parts, past_guesses):
    updated = []
    for l in word_parts:
        if l in past_guesses:
            updated.append(l)
        else:
            updated.append('_')
    return updated

def render_guess(guess):
    # makes pretty formatted guess string for printing
    val = ""
    for l in guess:
        val = val + l + " "
    val = val.strip()
    return val

miss_count = 0
miss_limit = 5

# setup game
print "*" * 50
print "Welcome to Hangman!"
print "Let's play. You get " + str(miss_limit) + " guesses."
print "*" * 50 + "\n"

# word = 'apple' #DEBUG
# get a random word
word = get_word()
word_parts = []
for l in word:
    word_parts.append(l)

past_guesses = []
guess_word = []
for letter in word:
    guess_word.append('_')

# game loop
while True:

    # check - player wins
    if "".join(guess_word).strip() == word:
        print "YOU WIN! Your word was " + word
        break

    # check - player loses
    if miss_count >= miss_limit:
        print "You're all out of guesses. You lose! The word was " + word + "."
        break

    # show word with blanks
    print "\nYour word looks like:",
    print render_guess(guess_word)
    print "So far, you've guessed: " + ", ".join(past_guesses)

    # ask for guess
    current_guess = get_guess()

    #validate guess
    if not valid_guess(current_guess):
        print "Invalid guess"
        continue

    # if letter has already been guessed, prompt user
    if current_guess not in past_guesses:
        past_guesses.append(current_guess)
    else:
        print "You already guessed " + current_guess + "."
        continue
    
    # if guess is right, update output
    if current_guess in word_parts:
        print "Good guess! " + current_guess + " is in the word."
        guess_word = update_guess(current_guess, word_parts, past_guesses)
        continue

    # if guess is wrong, update drawing and incorrect guess list
    else:
        miss_count += 1
        print "Sorry! " + current_guess + " is not part of the word."