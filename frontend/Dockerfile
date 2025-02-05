# Use Node.js as base image
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Copy configuration files
COPY *.config.js ./
COPY index.html ./

# Install dependencies including dev dependencies for testing
RUN npm install && \
    npm install axios bcryptjs && \
    npm install --save-dev @testing-library/react @testing-library/jest-dom \
    @testing-library/user-event @babel/preset-react @babel/preset-env \
    jest jest-environment-jsdom babel-jest

# Expose port 5173 (default Vite port)
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev", "--", "--host"]
