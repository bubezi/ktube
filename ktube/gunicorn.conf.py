import multiprocessing

bind = "127.0.0.1:8000"  # Replace with the appropriate bind address for your application
workers = multiprocessing.cpu_count() * 2 + 1  # Adjust the number of workers as per your system's configuration
# Add other Gunicorn options as needed
