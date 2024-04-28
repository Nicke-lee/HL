import math
import random


# checks users enter yes (y) or no (n)
def yes_no(question):
    while True:
        response = input(question).lower()

        # check user response, question
        # repeats if users don't enter yes / no
        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("Please enter yes / no")


def instructions():
    print('''

**** Instructions ****

To begin, choose the number of rounds and either customise
the game parameters or go with the default game (where the
secret number will be between 1 and 100)

Then choose how many rounds you'd like to play <enter> for infinite mode.

Your goal is to try to guess the secret number without running out 
of guesses.

Good Luck.

    ''')


# checks for an integer with optional upper /
# lower limits and an optional exit code for infinite mode
# / quitting game
def int_check(question, low=None, high=None, exit_code=None):

    # if any integer is allowed...
    if low is None and high is None:
        error = "Please enter an integer"

    # if the number needs to be more than an
    # integer (ie: rounds / 'high number'
    elif low is not None and high is None:
        error = (f"Please enter an integer that is "
                 f"more than / equal to {low}")

    # if the number needs to between low & high
    else:
        error = (f"Please enter an integer that"
                 f" is between {low} and {high} (inclusive)")

    while True:
        response = input(question).lower()

        # checks for infinite mode / exit code
        if response == exit_code:
            return response

        try:
            response = int(response)

            # Check the integer is not too low...
            if low is not None and response < low:
                print(error)

            # check response is more than the low number
            elif high is not None and response > high:
                print(error)

            # if response is valid, return it
            else:
                return response

        except ValueError:
            print(error)


# calculate the number of guesses allowed
def calc_guesses(low, high):
    num_range = high - low + 1
    max_raw = math.log2(num_range)
    max_upped = math.ceil(max_raw)
    max_guesses = max_upped + 1
    return max_guesses


# Main Routine Starts here

# Initialise game variables
mode = "regular"
rounds_played = 0
end_game = "no"
feedback = ""

game_history = []
all_scores = []

print("⚡⚡⚡ Welcome to the Higher lower Game 🎇🎇🎇 ")
print()

want_instructions = yes_no("Do you want to read the instructions? ").lower()

# check users enter yes (y) or no (n)
if want_instructions == "yes":
    instructions()

# Ask user for number of rounds / infinite mode
num_rounds = int_check("Rounds <enter for infinite>: ",
                       low=1, exit_code="")

if num_rounds == "infinite":
    mode = "infinite"
    num_rounds = 5

# ask user if they want to customise the number range
default_params = yes_no("Do you want to user the default game parameters?")
if default_params == "yes":
    low_num = 0
    high_num = 10

# allow user to choose the high / low number
else:
    low_num = int_check("Low Number? ")
    high_num = int_check("High Number? ", low=low_num + 1)

# calculate the maximum number of guesses based on the low and high number
guesses_allowed = calc_guesses(low_num, high_num)

# Game loops starts here
while rounds_played < num_rounds:

    # Rounds heading (based on mode)
    if mode == "infinite":
        rounds_heading = f"\n 💿💿💿Rounds {rounds_played +1} (Infinite mode) 💿💿💿 "
    else:
        rounds_heading = f"\n💿💿💿 Round {rounds_played +1} of {num_rounds} 💿💿💿"

    print(rounds_heading)

    # Rounds starts here
    # Set guesses used to zero at the start of each round
    guesses_used = 0
    already_guessed = []

    # choose a 'secret' number between the low and high number
    secret = random.randint(low_num, high_num)

    guess = ""
    while guess != secret and guesses_used < guesses_allowed:

        # ask the user to guess the number
        guess = int_check("Guess: ", low_num, high_num, "xxx")

        # check that they don't want to quit
        if guess == "xxx":
            # set end_game to use so that outer loop can be
            end_game = "yes"
            break

        # check that guess is not a duplicate
        if guess is already_guessed:
            print(f"You've already guessed {guess}, You've *still* used"
                  f"{guesses_used} / {guesses_allowed} guesses")
            continue

        # if guess is not a duplicate, add it to the 'already guesses' list
        else:
            already_guessed.append(guess)

        # add one to the number of guesses used
        guesses_used += 1

        # compare the user's choice with the secret number set up feedback statement

        # if we have guesses left
        if guess < secret and guesses_used < guesses_allowed:
            feedback = (f"Too low, please try a higher number. "
                        f" you've used {guesses_used} out of {guesses_allowed} guesses")
        elif guess > secret and guesses_used < guesses_allowed:
            feedback = (f"Too high, please try a lower number."
                       f"You've used {guesses_used} out of {guesses_allowed} guesses")

        # when the secret number is guesses. we have three different feedback
        elif guess == secret:

            if guesses_used == 1:
                feedback = "Lucky! you got it on the first guess."
            elif guesses_used == guesses_allowed:
                feedback = f"Phew You got it in {guesses_used} guesses"
            else:
                feedback = F"Well done! You guesses the secret number in {guesses_used} guesses"

        # if there are no guesses left
        else:
            feedback = "Sorry - you have no more guesses. You lose this round!"

        # print feedback to user
        print(feedback)

        # additional feedback
        if guesses_used == guesses_allowed - 1:
            print("Careful you have one more guess left")

        print()

        # Rounds end here

    # If user has entered the exit code
    if end_game == "yes":
        break

    rounds_played += 1

    all_scores.append(guesses_used)
    game_history.append(f"Round {rounds_played}: {feedback}")

    # if user are in infinite mode, increase number of rounds!
    if mode == "infinite":
        num_rounds += 1


# Game loop ends here

# check the user have played at least one round
# before calculation stats
if rounds_played > 0:
    # Game history / statistics area

    # Calculate statistics
    all_scores.sort()
    best_score = all_scores[0]
    worst_score = all_scores[-1]
    average_score = sum(all_scores) / len(all_scores)

    # Output the statistics
    print("\n🍭🍭🍭 Statistics 🍭🍭🍭")
    print(f"Best: {best_score} | Worst:{worst_score} | Average:{average_score}")
    print()

    # Display the game history on request
    see_history = yes_no("Do you want to see your game history? ")
    if see_history == "yes":
        for item in game_history:
            print(item)
