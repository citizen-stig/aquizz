FROM python:3.8

COPY . /

RUN pip3 install -r /requirements.txt && \
    curl -sL https://deb.nodesource.com/setup_15.x | bash - && \
    apt-get install -y nodejs && \
    npm install --prefix aquizz-client && \
    npm run build --prefix aquizz-client

EXPOSE 5000

CMD ["gunicorn", "--config", "aquizz/gunicorn.conf.py", "--log-file=-", "aquizz.wsgi:app"]
