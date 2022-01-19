FROM python:3.9
WORKDIR /share/src/ovh-notifier/src/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /share/src/ovh-notifier/
CMD [ "python", "kimsufi.py" ]