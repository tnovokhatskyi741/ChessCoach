import openai


def get_feedback(api_key, user_move, board_fen):
    openai.api_key = api_key
    prompt = (
        f"You are a knowledgeable and supportive chess coach. "
        f"The user played {user_move}. "
        f"The current board state is: {board_fen}. "
        f"Provide constructive feedback on the move and suggest improvements."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a knowledgeable and supportive chess coach.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        feedback = response.choices[0].message["content"].strip()
        return feedback
    except openai.error.AuthenticationError:
        return "Authentication Error: Invalid OpenAI API Key."
    except openai.error.RateLimitError:
        return "Rate Limit Exceeded: Please try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}"
