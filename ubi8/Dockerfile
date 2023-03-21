FROM ubi8:latest
RUN dnf -y install python3 && dnf -y clean all
COPY . /app
ENTRYPOINT ["python3", "/app/test_openssl1.py"]
