import spacy

# Tải mô hình ngôn ngữ từ spaCy
nlp = spacy.load("en_core_web_md")

# Các câu hỏi và câu trả lời có sẵn
FAQ = {
    "What is your name?": "I am a chatbot built using spaCy!",
    "How are you?": "I'm just a piece of code, but thanks for asking!",
    "What can you do?": "I can chat with you, answer questions, and much more!",
    "Tell me a joke.": "Why don't scientists trust atoms? Because they make up everything!",
    "Goodbye": "Goodbye! Have a nice day!",
    "What is your favorite color?": "I don't have preferences, but I think blue is quite popular!",
    "Can you help me with my homework?": "Sure! What subject do you need help with?",
    "Do you like music?": "I don't have ears, but I can recommend some popular songs!",
    "What is your purpose?": "My purpose is to assist and provide information!",
    "Where are you from?": "I live in the cloud, just floating around the internet!"
}

# Hàm để tìm câu trả lời tốt nhất dựa trên độ tương đồng
def find_best_answer(user_input):
    # Chuyển câu hỏi người dùng thành vector
    user_input_vector = nlp(user_input)
    
    # Khởi tạo biến để lưu câu trả lời và độ tương đồng cao nhất
    best_match = None
    best_similarity = 0

    # Duyệt qua các câu hỏi có sẵn và tính toán độ tương đồng
    for question, answer in FAQ.items():
        question_vector = nlp(question)
        similarity = user_input_vector.similarity(question_vector)

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = answer

    return best_match, best_similarity

def start_chat():
    print("Chatbot: Hi! Ask me anything, or type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        # Tìm câu trả lời phù hợp
        answer, similarity = find_best_answer(user_input)
        if similarity > 0.6:  # Ngưỡng độ tương đồng để trả lời
            print("Chatbot:", answer)
        else:
            print("Chatbot: Sorry, I don't understand that yet.")

# Bắt đầu cuộc trò chuyện
if __name__ == "__main__":
    start_chat()
