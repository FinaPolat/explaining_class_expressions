FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip

RUN pip3 install openai retry

RUN apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

ENV OPENAI_API_KEY=""

COPY . .

CMD ["python3", "explain_a_CE.py"]
