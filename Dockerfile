FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
EXPOSE 8084
CMD ["waitress-serve", "--listen=*:8084", "app:app"]
