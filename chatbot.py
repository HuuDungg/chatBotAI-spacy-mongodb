from flask import Flask, request, jsonify
import spacy
import pymongo
import numpy as np
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity

# Khởi tạo Flask
app = Flask(__name__)

# Tải mô hình spaCy
nlp = spacy.load("en_core_web_md")

# Kết nối đến MongoDB
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

# Tải dữ liệu từ MongoDB
faq_data = load_training_data()

# Định nghĩa endpoint cho API
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    answer, similarity = find_best_answer(user_input, faq_data)

    if similarity > 0.6:  # Ngưỡng độ tương đồng để trả lời
        return jsonify({'response': answer})
    else:
        return jsonify({'response': "Sorry, I don't understand that yet."})

if __name__ == "__main__":
    app.run(debug=True)
