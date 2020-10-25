FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
# RUN pip install --no-cache-dir requests && \
#     pip install --no-cache-dir beautifulsoup4 && \
#     pip install --no-cache-dir pika && \
#     pip install --no-cache-dir pyyaml
    # pip install --no-cache-dir lxml

# RUN pip install --no-cache-dir beautifulsoup4

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./receive.py" ]