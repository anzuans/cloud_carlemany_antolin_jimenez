<<<<<<< HEAD
FROM tiangolo/uvicorn-gunicorn:python3.10 AS carlemany-backend-base
=======
FROM anzuans/carlemany-backend_sep15 AS carlemany-backend-base
>>>>>>> activity-4

RUN pip install --upgrade pip

COPY requirements/base.txt /tmp/requirements/

RUN pip install -r /tmp/requirements/base.txt

RUN mkdir /backend-backend

WORKDIR /carlemany-backend

COPY . ./

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "error", "--lifespan", "on"]

FROM carlemany-backend-base AS carlemany-backend-dev

COPY requirements/dev.txt /tmp/requirements/

RUN pip install -r /tmp/requirements/dev.txt
<<<<<<< HEAD

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "error", "--lifespan", "on"]
=======
>>>>>>> activity-4
