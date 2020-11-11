FROM python:slim
LABEL maintainer=oge.blessing@gmail.com
WORKDIR /
RUN mkdir /loiddataset
WORKDIR /loiddataset
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/bash"]
