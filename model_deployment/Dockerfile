FROM python:3.10
WORKDIR /app

# Create a virtual environment and activate it
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip

RUN pip install scikit-learn
RUN pip install lightgbm
RUN pip install gunicorn

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model file and Flask app
COPY flask_airline_best_model_26.08.2023.bin .
COPY predict.py .
COPY static/ static/
COPY templates/ templates/
COPY tests/ tests/

# Expose the port 9696 from the container
EXPOSE 9696

# Start the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]

