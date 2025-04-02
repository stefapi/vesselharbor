# frontend/Dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

FROM node:16-alpine

RUN npm install -g serve

WORKDIR /app
COPY --from=build /app/dist ./dist

EXPOSE 5000
CMD ["serve", "-s", "dist", "-l", "5000"]

