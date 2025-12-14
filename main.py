from mchat_predictor import MChatPredictor
from mchat_chatbot import MChatChatbot


if __name__ == "__main__":

    predictor = MChatPredictor()
    chatbot = MChatChatbot(model_predictor=predictor)

    print(chatbot.start_conversation())

    while chatbot.stage != "complete":
        user_input = input("\nYou: ")
        response = chatbot.chat(user_input)
        print(f"\nAssistant: {response}")