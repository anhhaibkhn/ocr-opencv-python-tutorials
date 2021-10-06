FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
MAINTAINER Rick Torzynski "ricktorzynski@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y libtesseract-dev
COPY . /app
WORKDIR /app
RUN pip install pillow
RUN pip install pytesseract
RUN pip install opencv-contrib-python
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]