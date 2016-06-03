FROM ubuntu:latest
MAINTAINER Alberto Barradas "abcsds@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /Mercutio
WORKDIR /Mercutio
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
