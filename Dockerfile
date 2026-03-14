# Base image
FROM python:3.11

# 1. Set working directory /app
WORKDIR /app

# 2. Copy requirements.txt
COPY requirements.txt .

# 3. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application files
COPY . .

# 5. Expose port 8000
EXPOSE 8000

# 6. Run FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
