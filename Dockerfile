FROM python:3.6

WORKDIR /app

# Install Python basics
COPY setup.sh requirements.txt ./
RUN ./setup.sh

# Create data
RUN mkdir data
COPY static/csv/ ./static/csv/
COPY create-db.sh .
COPY scripts/ ./scripts/
RUN ./create-db.sh

# Install templates
COPY . .

EXPOSE 8001

CMD /app/venv-datasette/bin/datasette serve \
    --host 0 \
    --port 8001 \
    --template-dir ./templates \
    --static static:./static \
    --metadata metadata.json \
    data/*.db
