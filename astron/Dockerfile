FROM thetestgame/astron:master

# Copy server directories into Docker image
COPY ./quest /app/quest
COPY ./astron/ /app/build/
WORKDIR /app

EXPOSE 6667
EXPOSE 7100

ENTRYPOINT [ "./build/astrond" ]