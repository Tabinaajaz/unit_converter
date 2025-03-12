FROM python:3.10

# Workdir set karein
WORKDIR /app

# Dependencies copy karein
COPY requirements.txt /app/

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/
