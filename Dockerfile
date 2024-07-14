FROM python:3.9-slim

WORKDIR /app


# These commands install the cv2 dependencies that are normally present on the local machine, but might be missing in your Docker container causing the issue.
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY backend/requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Copy the FastAPI app code into the container
COPY ./backend ./backend/

# Copy the frontend files into the container
COPY ./frontend ./frontend

# Expose the port that the FastAPI app runs on
EXPOSE 8000
#
# # Copy the start script
# COPY start.sh .
#
# # Make the start script executable
# RUN chmod +x start.sh
#
# Command to run the start script
CMD [ "python", "backend/app.py" ]

