FROM python:3.8

WORKDIR /usr/src/app

COPY . .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
RUN pip install .

CMD ["gunicorn", "backstage:app", "-c", "./gunicorn.conf.py"]

