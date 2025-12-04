FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set PYTHONPATH so the app can find the modules
ENV PYTHONPATH=.

# Fetch initial data during build so the app has data to serve immediately
RUN python -m pitaco.commands.download_megasena

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "pitaco.application:app", "--bind", "0.0.0.0:8000"]
