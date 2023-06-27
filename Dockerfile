# Use the official Python image as the base image
FROM python:3.9.1

# Copy the bot code and model file to the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint command to run your bot
CMD ["python", "bot.py"]