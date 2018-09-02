FROM alpine
RUN apk --no-cache add nodejs npm curl mariadb-client
WORKDIR /app/
COPY package.json /app/
RUN npm install
COPY hello.js /app/
EXPOSE 8080
ENTRYPOINT ["node", "hello.js"]
