FROM python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /drfpython/tutors
COPY /requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

CMD python manage.py runserver 0.0.0.0:3000
