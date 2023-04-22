# Étape de construction
FROM node:14.17.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --prod

# Étape de production
FROM nginx:1.21.0-alpine
COPY --from=build /app/dist/petition-front /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
