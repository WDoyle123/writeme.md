from mongo:5.0.26

ENV MONGO_INITDB_ROOT_USERNAME=mongoadmin
ENV MONGO_INITDB_ROOT_PASSWORD=secret
ENV MONGO_INITDB_DATABASE=userSubmissions

expose 27017

CMD ["mongod", "--auth"]
