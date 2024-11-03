FROM python:3.12

ADD borsa_pitone.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python","./borsa_pitone.py"]

