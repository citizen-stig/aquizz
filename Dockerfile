FROM python:3.6-onbuild

RUN pip3 install -r ./requirements.txt && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get install -y nodejs && \
    npm install --prefix aquizz-client && \
    npm run build --prefix aquizz-client

EXPOSE 5000

CMD ["gunicorn", "--config", "aquizz/gunicorn.conf.py", "--log-file=-", "aquizz.wsgi:app"]
