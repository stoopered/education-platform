## Dockerfile for the frontend service
#
# This image installs Node.js dependencies and runs the webpack
# development server to serve the React application.  It expects the
# API endpoint to be available under the hostname `backend` on port
# 3001 when running inside a docker-compose network.  The environment
# variable REACT_APP_API_URL can be overridden to point at a
# different backend URL.

FROM node:18-alpine

# Install base dependencies
WORKDIR /app

# Copy package files first to leverage Docker layer caching
COPY package.json package-lock.json* ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Set environment variables for the React application
ENV PORT=3000
ENV REACT_APP_API_URL=http://backend:3001

# Expose the development server port
EXPOSE 3000

# Launch the development server.  In production you may prefer
# `npm run build` followed by serving the static files with Nginx or
# another web server.
CMD ["npm", "start"]