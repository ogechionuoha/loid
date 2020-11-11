FROM python:slim
LABEL maintainer=oge.blessing@gmail.com

#install relevant libs
RUN apt-get -y update
RUN apt-get install wget
RUN apt install -y libgl1-mesa-glx 
RUN apt-get install -y libglib2.0-0

WORKDIR /
RUN mkdir /loiddataset
WORKDIR /loiddataset
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/bash"]
