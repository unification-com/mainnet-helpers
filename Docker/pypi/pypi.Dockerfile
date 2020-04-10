FROM python:3.7.2

RUN apt-get update && \
    apt-get install -y gcc

RUN pip install --upgrade setuptools wheel twine
RUN pip install --upgrade pip

RUN mkdir /src && mkdir /src/tests && mkdir /src/undmainchain

COPY LICENSE /src
COPY MANIFEST.in /src
COPY README /src
COPY requirements.txt /src
COPY setup.cfg /src
COPY setup.py /src
COPY tests/. /src/tests
COPY undmainchain/. /src/undmainchain

WORKDIR /src

RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf

RUN python setup.py sdist

CMD python -m twine upload dist/*
