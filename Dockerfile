# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire project directory into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8002 available to the world outside this container
EXPOSE 8002

# Define environment variable
ENV NAME World

# Run app.py when the container launches on port 8002
CMD ["uvicorn", "predict_house_value.app.app:app", "--host", "0.0.0.0", "--port", "8002"]

