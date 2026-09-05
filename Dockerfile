FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY exampleAvecVoies.json exampleSansVoies.json ./
COPY data ./data

ENV PYTHONPATH=/app/src
ENV PROJETCINE_DATA=/app/data

EXPOSE 8000

CMD ["uvicorn", "webPackage.applicationWeb:app", "--host", "0.0.0.0", "--port", "8000"]
