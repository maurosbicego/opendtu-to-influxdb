FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
COPY root.crt* /usr/local/share/ca-certificates/root.crt
RUN update-ca-certificates

CMD ["python", "./main.py"]