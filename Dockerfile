FROM python:2.7
MAINTAINER Felix Enescu <felix@enescu.name>

ADD . /async
WORKDIR /async/

RUN pip install -r requirements.txt


