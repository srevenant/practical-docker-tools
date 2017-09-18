FROM alpine
RUN apk --no-cache add gcc libc-dev linux-headers make vim bash libaio-dev curl
WORKDIR /fio
#ADD fio-3.0.tar.gz /fio
RUN curl -sLO https://github.com/axboe/fio/archive/fio-3.0.tar.gz && \
    mkdir src && \
    tar -C src --strip 1 -xzf fio-3.0.tar.gz && \
    rm -f fio-3.0.tar.gz && \
    cd src && \
    make

# this has many 'fmt' errors but these are okay
#RUN cd fio-fio-3.0 && make
VOLUME /vol1-named
VOLUME /vol2-bind
RUN mkdir /vol3-local
COPY bench.sh /fio/
CMD ./bench.sh
