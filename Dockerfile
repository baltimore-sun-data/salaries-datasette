FROM python:3.6

WORKDIR /app

# Install Python basics
COPY run.sh requirements.txt ./
RUN ./run.sh setup-prod

# Create data
RUN mkdir data
COPY static/csv/ ./static/csv/
COPY scripts/ ./scripts/
RUN ./run.sh create-db

# Install templates
COPY . .

EXPOSE 9001

CMD ./run.sh serve-prod
