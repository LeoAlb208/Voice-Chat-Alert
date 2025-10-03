# Usa Python 3.11 slim come base
FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia requirements e installa le dipendenze
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del codice
COPY . /app

# Espone la porta 8080
EXPOSE 8080

# Avvia il bot
CMD ["python", "main.py"]
