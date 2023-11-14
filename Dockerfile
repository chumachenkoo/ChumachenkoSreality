# Use the official Python image as the base image
FROM python:3.8

# Set environment variables (customize as needed)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=localhost
ENV FLASK_RUN_PORT=8080

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port where the Flask app will run
EXPOSE 8080

# Command to run the Flask app
CMD ["flask", "run", "--host=localhost", "--port=8080"]
