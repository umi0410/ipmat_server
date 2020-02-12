# ipmat backend rest api server
# env IPMAT_DEBUG

FROM python:3.7
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
# EXPOSE 9000
ENV DEBUG False
CMD ["python", "manage.py",  "runserver", "0:8000", "--insecure"]
