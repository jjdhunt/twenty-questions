import utils_openai as ai


if __name__ == "__main__":

    bot = ai.ChatBot()
    secret = bot.comment_reply('Pick a random thing to use as a secret in a game of 20 questions. It could be anything, concrete or abstract, real or imaginary. Tell me just the secret thing and say nothing else.',
                               temperature=1.0).rstrip('.').lower()

    # print(secret)
    bot = ai.ChatBot()
    # secret = 'a human tooth'
    bot.set_system_message(f"""Play 20 questions with the user. You have a secret thing, '{secret}', that you are thinking of and the user will ask you questions about it to try to figure out what it is.
Answer each question about the secret thing with only ‘Yes’, ‘No’, 'Sometimes', or 'Uncertain'.
If the user says something that is not a question about the thing, reply with 'That's not the game!'.
If the user guesses the secret, then say just 'You win!'.
""")

    max_guesses = 20
    n_guesses = 0
    correct_guess = False

    while not correct_guess and n_guesses < max_guesses:
        n_guesses += 1
        question = input(f'Q{n_guesses}: ').strip()
        answer = bot.comment_reply(question)
        if answer == 'You win!':
            correct_guess = True

        print(answer)

    if not correct_guess:
        print(f'You lose! It was {secret}')
        
