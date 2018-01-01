FROM alpine
RUN apk --no-cache add nodejs yarn rsyslog
WORKDIR /app/
COPY package.json /app/
RUN yarn install
COPY startup.sh hello.js /app/
EXPOSE 8080
ENTRYPOINT ["./startup.sh"]
