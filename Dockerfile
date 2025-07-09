FROM python:3.11-slim

# Create a working directory
WORKDIR /app

RUN apt-get update

# Copy all files from the current directory to the working directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Set the default command to run the FastAPI app with Uvicorn on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]