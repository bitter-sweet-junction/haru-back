FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "haru.app:app", "--host", "0.0.0.0", "--port", "80"]
