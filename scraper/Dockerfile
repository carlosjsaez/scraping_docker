FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container
# will listen for connections
EXPOSE 3306

WORKDIR /scraper
ADD . /scraper

COPY requirements.txt /scraper
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD [ "stdbuf", "-oL", "python", "scraper.py"]