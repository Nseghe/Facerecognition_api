from ubuntu:16.04

RUN apt-get update --fix-missing && apt-get --yes install software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get --yes install build-essential python3.6 python3.6-dev python3-pip && python3.6 -m pip install pip --upgrade && apt-get update && apt-get --yes install libsm6 libxext6 libxrender1 libfontconfig1

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3.6"]

CMD ["app.py"]
