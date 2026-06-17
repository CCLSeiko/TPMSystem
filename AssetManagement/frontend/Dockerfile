# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage with nginx
FROM nginx:alpine
RUN addgroup --system app && adduser --system --ingroup app app && \
    mkdir -p /var/cache/nginx /var/run /var/log/nginx && \
    chown -R app:app /var/cache/nginx /var/run /var/log/nginx && \
    chmod -R 755 /var/cache/nginx /var/run /var/log/nginx
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN chown -R app:app /usr/share/nginx/html && \
    touch /run/nginx.pid && chown app:app /run/nginx.pid
USER app
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
