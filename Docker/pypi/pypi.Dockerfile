FROM python:3.7.2

RUN apt-get update && \
    apt-get install -y gcc pandoc

RUN pip install --upgrade setuptools wheel twine pip

RUN mkdir /src && mkdir /src/tests && mkdir /src/undmainchain

COPY LICENSE /src
COPY MANIFEST.in /src
COPY README.org /src
COPY requirements.txt /src
COPY setup.cfg /src
COPY setup.py /src
COPY tests/. /src/tests
COPY undmainchain/. /src/undmainchain

WORKDIR /src

RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
RUN pandoc -f org -t markdown README.org -o README.md

RUN python setup.py sdist

CMD python -m twine upload dist/*
