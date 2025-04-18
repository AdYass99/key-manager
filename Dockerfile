FROM python:alpine
WORKDIR /key-manager
COPY . /key-manager

RUN mkdir instance
RUN pip install --no-cache-dir -r requirements.txt
RUN python generate_cert.py
EXPOSE 5000

CMD ["python", "run.py"]