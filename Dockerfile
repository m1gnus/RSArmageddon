FROM debian:bookworm-slim as build

WORKDIR /usr/src/app

RUN apt update && apt install -y --no-install-recommends --no-install-suggests python3-setuptools git sagemath \
    && git clone https://github.com/kaisersource/RSArmageddon.git \
    && cd RSArmageddon && python3 setup.py install \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/src/app/RSArmageddon

ENTRYPOINT ["/usr/local/bin/rsarmageddon"]
# docker run -t --rm -v $PWD/examples:/data rsarmageddon attack all -k /data/examples/wiener.pub --timeout 1m
