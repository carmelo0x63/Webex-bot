FROM alpine:latest
ENV DESTDIR /usr/local/bin/
ENV TZ=Europe/Rome

RUN apk add --no-cache python3 py3-requests tzdata
COPY cibot.py ${DESTDIR}
WORKDIR ${DESTDIR}

CMD ["/usr/bin/python3", "-u", "cibot.py"]
