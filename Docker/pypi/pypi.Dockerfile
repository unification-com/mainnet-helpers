FROM python:3.7.2

RUN apt-get update && \
    apt-get install -y gcc

RUN pip install --upgrade setuptools wheel twine
RUN pip install --upgrade pip

COPY src /src/src

WORKDIR /src/src

RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf

RUN python setup.py sdist

CMD python -m twine upload dist/*
