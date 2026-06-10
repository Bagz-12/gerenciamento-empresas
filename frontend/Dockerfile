# ── Estágio 1: build do Vue ──────────────────────────────────────────────────
FROM node:20-alpine AS builder

ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .
RUN npm run build

# ── Estágio 2: servir com Nginx ───────────────────────────────────────────────
FROM nginx:alpine

# Copia os arquivos buildados para o Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Configuração do Nginx para Vue Router (SPA)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
