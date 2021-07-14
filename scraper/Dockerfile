# Use an official Python runtime as an image
FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container
# will listen for connections
EXPOSE 3306

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction
# creates a directory with this name if it doesn’t exist
WORKDIR /scraper
ADD . /scraper


# Install any needed packages specified in requirements.txt
COPY requirements.txt /scraper
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD python scraper.py