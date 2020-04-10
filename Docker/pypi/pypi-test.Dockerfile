FROM python:3.7.2

RUN apt-get update && \
    apt-get install -y gcc

RUN pip install --upgrade --index-url https://pypi.org/simple/ undmainchain

CMD python -m undmainchain.upgrade
