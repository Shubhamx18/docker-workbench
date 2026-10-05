FROM python:latest

# Set working directory inside container
WORKDIR /myapp

# Copy the Python script into the container
COPY mycode.py /myapp/

# Install pymysql
RUN pip install pymysql

# Run the Python script
CMD ["python", "mycode.py"]
