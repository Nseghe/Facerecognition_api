from ubuntu:latest

RUN apt-get update --fix-missing && apt-get --yes install software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get --yes install build-essential python3 python3-dev python3-pip
RUN apt-get update --fix-missing && apt-get update && apt-get --yes install locales && locale-gen en_US.UTF-8

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN cd /usr/lib/python3.8 && ls

EXPOSE 5000

#ENV LANG en_US.UTF-8
#ENV LANGUAGE en_US:en
#ENV LC_ALL en_US.UTF-8
#ENV FLASK_APP run

ENTRYPOINT ["python3.6"]
CMD ["app.py"]

