import utils_openai as ai


if __name__ == "__main__":

    bot = ai.ChatBot()
    # secret = bot.comment_reply('Pick a random thing to use as a secret in a game of 20 questions. It could be anything, concrete or abstract, real or imaginary. Tell me just the secret thing and say nothing else.',
    #                            temperature=1.0).rstrip('.').lower()
    # print(f"The secret is '{secret}'.")

    secret = 'a lullaby'

    # set up the questioner
    questioner = ai.ChatBot()
    questioner.set_system_message(f"""Play 20 questions with me. I'm thinking of a secret thing - it could be anything, concrete or abstract, real or imaginary - and you must try to guess it by asking questions to narrow it down. Once you think you know what it is you can make a guess.
I'll answer your questions about the secret thing with only ‘Yes’, ‘No’, 'Sometimes', or 'Uncertain'.
We can play for more than 20 questions. We'll just keep going until you get it.
""")

    # set up the answerer
    answerer = ai.ChatBot()
    answerer.set_system_message(f"""Play 20 questions with the user. You have a secret thing, '{secret}', that you are thinking of and the user will ask you questions about it to try to figure out what it is.
Answer each question about the secret thing with only ‘Yes’, ‘No’, 'Sometimes', or 'Uncertain'.
If the user says something that is not a question about the thing, reply with 'That's not the game!'.
If the user guesses the secret, then say just 'You win!'.
You can play for more than 20 questions. Just keep going until they guess it.
""")

    # set up the game
    max_guesses = 50
    n_guesses = 0
    correct_guess = False

    # play the game
    question = questioner.comment_reply("OK, I'm thinking of something. Ask your first question.")
    while not correct_guess and n_guesses < max_guesses:
        n_guesses += 1
        answer = answerer.comment_reply(question)

        print(f'Q{n_guesses}: {question}')
        print(answer)

        if answer == 'You win!':
            correct_guess = True
        else:
            question = questioner.comment_reply(answer)

    if not correct_guess:
        print(f'You lose! It was {secret}')
        
