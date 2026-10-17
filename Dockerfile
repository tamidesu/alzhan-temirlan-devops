FROM python:3.12-slim
WORKDIR /app
COPY app/ ./app/
COPY config/student.json ./config/student.json
RUN python -m compileall -q app
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "app/main.py"]
