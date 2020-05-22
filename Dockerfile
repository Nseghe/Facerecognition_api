from ubuntu:latest

RUN apt-get update --fix-missing && apt-get --yes install software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get --yes install build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN python3.6 -m pip install pip --upgrade && python3.6 -m pip install wheel && python3.6 -m pip install virtualenv
RUN apt-get update --fix-missing && apt-get --yes install openalpr openalpr-daemon openalpr-utils libopenalpr-dev && apt-get update && apt-get --yes install locales && locale-gen en_US.UTF-8

WORKDIR /app

COPY . /app

RUN cd /usr/lib/python3.6 && ls
RUN git clone https://github.com/Nseghe/openalpr.git

RUN pip3 install -r requirements.txt

EXPOSE 5000

RUN cd /usr/lib/python3.5 && ls

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV FLASK_APP run

CMD ["flask", "run", "--port=5000"]

