FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install requests pillow pandas tk pysimplegui
ENV DISPLAY :0
CMD ["python3", "/app/record_gui.py"]