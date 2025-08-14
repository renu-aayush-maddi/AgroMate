FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
COPY . .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "hackx6.0", "/bin/bash", "-c"]

EXPOSE 8000

CMD ["conda", "run", "--no-capture-output", "-n", "hackx6.0", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
