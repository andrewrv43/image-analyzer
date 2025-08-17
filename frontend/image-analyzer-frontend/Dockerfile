# Stage 1: Build the Angular application
FROM node:18-alpine AS build
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the application from Nginx
FROM nginx:stable-alpine
COPY --from=build /usr/src/app/dist/image-analyzer-frontend/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
