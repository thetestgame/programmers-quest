FROM python:latest

# Copy server and asset directories into Docker image
COPY . /server/
WORKDIR /server

# Install our pip dependencies
RUN pip install -r quest/docs/requirements.txt

# Setup our entry point and command
ENTRYPOINT ["python"]
CMD ["-m", "quest.ai"]