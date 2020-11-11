FROM python:slim
LABEL maintainer=oge.blessing@gmail.com

#install relevant libs
RUN apt-get install wget
RUN apt install -y libgl1-mesa-glx 

WORKDIR /
RUN mkdir /loiddataset
WORKDIR /loiddataset
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/bash"]
