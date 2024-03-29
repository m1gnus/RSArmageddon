FROM debian:bookworm-slim

VOLUME /workdir
WORKDIR /workdir

RUN apt-get update \
 && apt-get install -y --no-install-recommends --no-install-suggests \
    python3 python3-build python3-setuptools python3-pip sagemath \
 && apt-get clean

COPY ./ /usr/local/src/rsarmageddon/
RUN pip install --break-system-packages /usr/local/src/rsarmageddon/

ENTRYPOINT ["/usr/local/bin/rsarmageddon", "--no-user-attacks"]
