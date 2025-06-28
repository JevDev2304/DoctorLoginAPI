# Usar una imagen oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requirements y archivos de la app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto que usará Uvicorn
EXPOSE 10000

# Comando para correr la app en Render
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"] 