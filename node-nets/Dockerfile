FROM alpine
RUN apk --no-cache add nodejs yarn curl mariadb-client
WORKDIR /app/
COPY package.json /app/
RUN yarn install
COPY hello.js /app/
EXPOSE 8080
ENTRYPOINT ["node", "hello.js"]
