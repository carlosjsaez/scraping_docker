FROM python:3.6

WORKDIR /api
ADD . /api

COPY requirements.txt /scraper
RUN pip install -r requirements.txt

CMD ["python", "api.py" ]
