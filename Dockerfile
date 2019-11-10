FROM python:3.7

LABEL maintainer="emir.modiri@useinsider.com"

RUN apt-get update 

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]