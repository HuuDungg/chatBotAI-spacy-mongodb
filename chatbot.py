import spacy
import pymongo
import numpy as np
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity

# Tải mô hình spaCy
nlp = spacy.load("en_core_web_md")

# Kết nối đến MongoDB với chuỗi kết nối đã sửa
client = MongoClient(
    "mongodb+srv://huudung038:1@clusterhuudung.z5tdrft.mongodb.net/?retryWrites=true&w=majority&appName=ClusterHuuDung&tlsAllowInvalidCertificates=true")
db = client['chatbot_db']
collection = db['faq_collection']


# Tải dữ liệu huấn luyện từ MongoDB
def load_training_data():
    faq_data = list(collection.find())
    return faq_data


# Hàm tìm câu trả lời tốt nhất dựa trên độ tương đồng
def find_best_answer(user_input, faq_data):
    user_input_vector = nlp(user_input).vector.reshape(1, -1)
    best_match = None
    best_similarity = -1

    for faq in faq_data:
        question_vector = np.array(faq['question_vector']).reshape(1, -1)
        similarity = cosine_similarity(user_input_vector, question_vector)[0][0]

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = faq['answer']

    return best_match, best_similarity


def start_chat(faq_data):
    print("Chatbot: Hi! Ask me anything, or type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        # Tìm câu trả lời phù hợp
        answer, similarity = find_best_answer(user_input, faq_data)
        if similarity > 0.6:  # Ngưỡng độ tương đồng để trả lời
            print("Chatbot:", answer)
        else:
            print("Chatbot: Sorry, I don't understand that yet.")


if __name__ == "__main__":
    # Tải dữ liệu từ MongoDB
    faq_data = load_training_data()
    # Bắt đầu cuộc trò chuyện
    start_chat(faq_data)
