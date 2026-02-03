ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    python3 \
    py3-pip \
    && pip3 install --no-cache-dir --break-system-packages \
    flask==3.0.0 \
    requests==2.31.0 \
    google-generativeai==0.8.3 \
    gunicorn==21.2.0 \
    PyYAML==6.0.1

COPY app.py /
COPY templates /templates/
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
