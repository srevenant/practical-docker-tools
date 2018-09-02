FROM alpine
RUN apk --no-cache add nodejs npm rsyslog
WORKDIR /app/
COPY package.json /app/
RUN npm install
COPY startup.sh hello.js /app/
EXPOSE 8080
ENTRYPOINT ["./startup.sh"]
