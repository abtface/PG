FROM ubuntu:xenial

# Install package repositories, build dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  python3 python3-pip python3-setuptools \
  vim tmux \
  && apt-get install -y libglib2.0-0 \
  && apt-get install -y libsm6 libxext6 libxrender-dev \
  && pip3 install python-barcode opencv-python pillow fpdf

WORKDIR /usr/src/barcodez
#COPY scripts .

CMD ["bash"]
