# Python base image
FROM python:3.12.5-alpine3.19

# Define the working directory
WORKDIR ./usr/src/wall_project

# Copy the project files to the working directory
COPY . .

# Install the project dependencies
RUN pip install -r requirements.txt

# Run the Django migrations
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Expose the server port
EXPOSE 8080

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
