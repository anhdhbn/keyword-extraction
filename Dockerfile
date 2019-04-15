FROM python:latest
ENV APP /app
RUN mkdir $APP
WORKDIR $APP
EXPOSE 5000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./app.py" ]