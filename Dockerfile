# Starting from a python base
FROM python:3.12

# Creating working directory
WORKDIR /app

# Copying everything from soure to working directory
COPY . .

# Using pip to install all required packages
RUN pip install requests pillow pandas tk

# Compiling and running program
CMD ["python3", "/app/record_term.py"]
