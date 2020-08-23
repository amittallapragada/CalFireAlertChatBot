# Extend the official Rasa Image
FROM rasa/rasa:1.8.1-full

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
# COPY actions/requirements-actions.txt ./

# Change back to root user to install dependencies
USER root

# Copy actions folder to working directory
COPY ./source /app
# Install extra requirements for actions code, if necessary (uncomment next line)



# By best practices, don't run the code with root user
USER 1001

