FROM    python:3.9

COPY    requirements.txt ./

RUN     pip install --no-cache-dir -r requirements.txt && \
        pip install --no-cache-dir gunicorn

#RUN     useradd -m codelab

#USER    codelab

WORKDIR /usr/src/app

COPY    . .

RUN     chmod +x install-java-8.sh && ./install-java-8.sh

RUN     pybabel compile -d translations

CMD     [ "gunicorn", "-b", ":5000", "--limit-request-field_size", "16380", "app:app" ]

EXPOSE  5000
