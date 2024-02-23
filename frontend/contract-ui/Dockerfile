# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory in the container
WORKDIR /frontend

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./frontend

# Copy the rest of your application code to the working directory
COPY . .

# Install app dependencies
RUN npm install

# Expose a port to communicate with the React app
EXPOSE 5173

# Start your React app
CMD ["npm", "run", "dev"]
