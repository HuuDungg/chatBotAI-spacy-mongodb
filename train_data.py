import pymongo
import spacy
import re
from pymongo import MongoClient

# Tải mô hình spaCy
nlp = spacy.load("en_core_web_md")

FAQ = [
    {"question": "What materials are your jerseys made from?", "answer": "Our jerseys are made from a blend of polyester and spandex for durability and comfort."},
    {"question": "Can I wash my jersey in a washing machine?", "answer": "Yes, you can wash it in a machine on a gentle cycle, but avoid fabric softeners."},
    {"question": "Do you have jerseys for kids?", "answer": "Yes, we offer a range of sizes for kids as well as adults."},
    {"question": "What payment methods do you accept?", "answer": "We accept all major credit cards, PayPal, and bank transfers."},
    {"question": "How long does shipping take?", "answer": "Shipping typically takes 5-7 business days for domestic orders."},
    {"question": "Can I customize my jersey with a different color?", "answer": "Yes, we offer customization in various colors for most jerseys."},
    {"question": "Are there any special care instructions for jerseys?", "answer": "Yes, it's best to wash them in cold water and air dry."},
    {"question": "Do you offer international shipping?", "answer": "Yes, we ship to select international destinations."},
    {"question": "What sizes do your jerseys come in?", "answer": "Our jerseys range from small to 3XL."},
    {"question": "Are your jerseys suitable for team sports?", "answer": "Yes, our jerseys are designed for both individual and team sports."},
    {"question": "Can I track my order once it has shipped?", "answer": "Yes, you will receive a tracking number via email once your order ships."},
    {"question": "Do you have any discounts for bulk purchases?", "answer": "Yes, we offer discounts for bulk orders. Please contact us for more details."},
    {"question": "What is your policy on exchanges?", "answer": "You can exchange items within 30 days of purchase as long as they are in original condition."},
    {"question": "Do you have breathable options for hot weather?", "answer": "Yes, we offer jerseys made with moisture-wicking fabrics ideal for hot weather."},
    {"question": "How often do you update your jersey collection?", "answer": "We update our collection seasonally and for special events."},
    {"question": "Are there any promotions running right now?", "answer": "Yes, please check our website for the latest promotions and discounts."},
    {"question": "Can I order a jersey with my own design?", "answer": "Yes, we accept custom designs for bulk orders."},
    {"question": "How do I care for my jersey to prevent fading?", "answer": "Avoid washing in hot water and direct sunlight to help prevent fading."},
    {"question": "What makes your jerseys different from others?", "answer": "We focus on quality materials, custom designs, and customer satisfaction."},
    {"question": "Do you offer any loyalty programs?", "answer": "Yes, we have a loyalty program that rewards frequent shoppers."},
    {"question": "Can I pre-order upcoming jersey releases?", "answer": "Yes, you can pre-order select upcoming releases on our website."},
    {"question": "What is the best way to store my jerseys?", "answer": "Store them in a cool, dry place, preferably folded rather than hung."},
    {"question": "Are your jerseys environmentally friendly?", "answer": "We strive to use sustainable materials and practices in our production."},
    {"question": "How do I find my perfect fit?", "answer": "Refer to our size chart and consider your usual fit preferences."},
    {"question": "Do you provide care labels on your jerseys?", "answer": "Yes, each jersey comes with a care label for your reference."},
    {"question": "What are your customer service hours?", "answer": "Our customer service is available from 9 AM to 6 PM, Monday to Friday."},
    {"question": "Do you have an option for express shipping?", "answer": "Yes, we offer express shipping for an additional fee."},
    {"question": "Can I change my order after it has been placed?", "answer": "You can change your order within an hour of placing it by contacting customer service."},
    {"question": "Are there any benefits for signing up for your newsletter?", "answer": "Yes, subscribers receive exclusive discounts and updates on new arrivals."},
    {"question": "Do you have any collaborations with athletes?", "answer": "Yes, we occasionally collaborate with athletes for special edition jerseys."},
    {"question": "What if my jersey doesn't fit?", "answer": "You can exchange it for a different size within 30 days."},
    {"question": "Are your jerseys machine washable?", "answer": "Yes, but we recommend washing them on a gentle cycle."},
    {"question": "What color options do you have for your jerseys?", "answer": "We offer a wide variety of colors, including classic and trendy shades."},
    {"question": "How can I stay updated on new products?", "answer": "Follow us on social media and subscribe to our newsletter."},
    {"question": "What is the most requested jersey style?", "answer": "The classic team jersey remains our most requested style."},
    {"question": "Do you have jerseys for female athletes?", "answer": "Yes, we have a specific line of jerseys designed for female athletes."},
    {"question": "Can I use a discount code on a sale item?", "answer": "Discount codes cannot be combined with sale items."},
    {"question": "Do you have a size guide available?", "answer": "Yes, our size guide is available on each product page."},
    {"question": "What should I do if my jersey is defective?", "answer": "Please contact our support team for assistance with defective items."},
    {"question": "Are there any seasonal promotions?", "answer": "Yes, we run seasonal promotions throughout the year."},
    {"question": "What is the best-selling jersey this month?", "answer": "Our best-selling jersey this month is the [insert popular design]."},
    {"question": "Can I buy gift cards for your store?", "answer": "Yes, we offer gift cards available for purchase on our website."},
    {"question": "Do you have a return label included in my order?", "answer": "Yes, a return label is included for your convenience."},
    {"question": "What kind of printing technique do you use?", "answer": "We use state-of-the-art sublimation printing for vibrant colors."},
    {"question": "Are there any fabric options for sensitive skin?", "answer": "Yes, we offer hypoallergenic options suitable for sensitive skin."},
    {"question": "Can I visit your warehouse?", "answer": "Warehouse visits are available by appointment only."},
    {"question": "What sports do you cater to?", "answer": "We cater to a variety of sports including soccer, basketball, baseball, and more."},
]


# Kết nối đến MongoDB với chuỗi kết nối đã sửa
client = MongoClient(
    "mongodb+srv://huudung038:1@clusterhuudung.z5tdrft.mongodb.net/?retryWrites=true&w=majority&appName=ClusterHuuDung&tlsAllowInvalidCertificates=true")
db = client['chatbot_db']
collection = db['faq_collection']

# Hàm tiền xử lý văn bản
def preprocess_text(text):
    text = text.lower()  # Chuyển đổi thành chữ thường
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Xóa ký tự đặc biệt, giữ lại chữ cái, số và khoảng trắng
    return text

# Chuyển đổi câu hỏi thành vector và lưu vào MongoDB
def save_training_data(data):
    # Xóa dữ liệu cũ nếu có
    # collection.delete_many({})

    # Chuyển đổi câu hỏi thành vector và lưu vào MongoDB
    for entry in data:
        processed_question = preprocess_text(entry['question'])
        question_vector = nlp(processed_question).vector.tolist()
        entry['question_vector'] = question_vector

    collection.insert_many(data)
    print("Training data saved to MongoDB.")

if __name__ == "__main__":
    save_training_data(FAQ)
