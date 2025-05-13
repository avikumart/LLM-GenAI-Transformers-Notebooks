FROM python:3.10-slim
RUN ln -s /usr/bin/python3 /usr/bin/python
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "main.py"]
