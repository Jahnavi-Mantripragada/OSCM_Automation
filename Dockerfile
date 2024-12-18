# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app's source code into the container
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Set the command to run Streamlit
CMD ["streamlit", "run", "OrderPlantoRoutePlanner.py"]
