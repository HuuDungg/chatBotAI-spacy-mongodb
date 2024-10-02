FROM python:3.9

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt mô hình SpaCy
RUN python -m spacy download en_core_web_md

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=chatbot.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
