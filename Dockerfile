FROM python:3.9.1-slim

# Specify the working directory
WORKDIR /

# Copy the requirements.txt file to the container
COPY requirements.txt requirements.txt

# Install the requirements
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8080

# Define environment variable
ENV FLASK_APP=server.py

# Run flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]