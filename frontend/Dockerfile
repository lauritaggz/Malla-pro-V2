# Frontend dev server for local development (docker compose). Production builds keep using
# Netlify/Vercel/cPanel as before.
FROM node:22-slim

WORKDIR /app/frontend
COPY package.json package-lock.json ./
RUN npm ci && sha1sum package-lock.json > node_modules/.lock-hash

EXPOSE 5174
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
