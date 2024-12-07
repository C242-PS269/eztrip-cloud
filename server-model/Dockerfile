# Use the official Python 3.12 image from Docker Hub
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable to indicate the app is in production
ENV FLASK_ENV=production

# Expose the port that the app will run on
EXPOSE 8080

# Define the command to run the app using python server.py
CMD ["python", "server.py"]