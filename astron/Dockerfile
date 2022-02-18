FROM thetestgame/astron:master

# Copy server directories into Docker image
COPY ./quest /app/quest
COPY ./astron /app/astron
WORKDIR /app

ENTRYPOINT [ "./build/astrond" ]