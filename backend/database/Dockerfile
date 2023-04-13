FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD mysecretpassword
ENV POSTGRES_DB petitions

EXPOSE 5432