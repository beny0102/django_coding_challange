# Dockerization for nextjs app

FROM node:16
RUN mkdir -p /app

COPY . /app

WORKDIR /app

RUN npm install

EXPOSE 3000