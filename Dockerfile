# Gunakan Python image sebagai base
FROM python:3.12.2-slim-bullseye

# Mengatur working directory di dalam container
WORKDIR /app

# Instal dependencies sistem yang dibutuhkan untuk psycopg2-binary
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt ke dalam container
COPY requirements.txt /app/

# Upgrade pip dan install dependencies dari requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy seluruh isi direktori proyek ke dalam container
COPY . /app/

# Set perintah default untuk menjalankan aplikasi
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]
