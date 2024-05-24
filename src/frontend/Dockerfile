FROM node:18.6.0
WORKDIR /app/frontend
COPY . .
RUN npm install
CMD npm run dev -- --host=0.0.0.0 --port=3000