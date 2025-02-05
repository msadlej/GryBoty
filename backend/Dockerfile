# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app
RUN apt update && apt install -y make

COPY Makefile pyproject.toml requirements.txt setup.* /app/

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app
CMD ["make"]
