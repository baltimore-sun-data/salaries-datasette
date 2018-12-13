FROM node:11 as yarn-builder

WORKDIR /app

COPY frontend/package.json frontend/yarn.lock ./
RUN yarn

COPY frontend/ .

RUN yarn build

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

COPY --from=yarn-builder /app/dist /app/frontend/dist

EXPOSE 9001

CMD ./run.sh serve-prod
