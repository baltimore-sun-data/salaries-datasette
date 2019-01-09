FROM node:11 as yarn-builder

WORKDIR /app

COPY frontend/package.json frontend/yarn.lock ./
RUN yarn

COPY frontend/ .

RUN yarn build

FROM python:3.7 as py-base

WORKDIR /app

# Install Python basics
COPY run.sh .
COPY requirements/*.txt requirements/
RUN ./run.sh setup-prod

FROM py-base as db-creator
# Create data
RUN mkdir data
COPY static/csv/ ./static/csv/
COPY scripts/ ./scripts/
RUN ./run.sh create-db

FROM py-base as py-server

COPY . .

COPY --from=db-creator /app/data /app/data
COPY --from=yarn-builder /app/dist /app/frontend/dist

EXPOSE 9001

CMD ./run.sh serve-prod
