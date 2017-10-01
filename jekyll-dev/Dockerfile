FROM ruby
RUN gem install jekyll bundler
WORKDIR /web/
EXPOSE 4000
CMD jekyll serve -H 0.0.0.0
