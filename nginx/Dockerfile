FROM nginx:1.27-alpine

# Удаляем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/default.conf
