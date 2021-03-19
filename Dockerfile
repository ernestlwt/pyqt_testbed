# docker build . -t pyqt_calculator

# xhost +local:docker && docker run --rm -e "DISPLAY=${DISPLAY}" -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" pyqt_calculator

FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y

# fix tzdata interactive configuration when installing python3-pip
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get install -y \
    python3-pyqt5 \
    python3-pip

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY ./calculator.py /app/calculator.py

CMD ["python3", "calculator.py"]
