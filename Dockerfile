FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install requests pillow pandas tk
CMD ["python3", "/app/record_term.py"]
