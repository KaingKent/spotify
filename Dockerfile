FROM python:latest 
WORKDIR /spotify-test
COPY . .
RUN pip install python-dotenv && pip install requests
ENTRYPOINT ["/usr/bin/env", "python3", "./main.py"]