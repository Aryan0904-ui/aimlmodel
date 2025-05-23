# Use official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Set the environment variable
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["python", "app/app.py"]
