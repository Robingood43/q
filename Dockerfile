FROM python:3.11.5-slim

WORKDIR /site_shinnik1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install router
EXPOSE 8000
CMD ["uvicorn", "router.main:app", "--host", "0.0.0.0", "--port", "8000"]
