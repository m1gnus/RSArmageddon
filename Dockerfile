FROM sagemath/sagemath:10.2

USER root
ENV HOME /root
VOLUME /workdir
WORKDIR /workdir

COPY ./ /usr/local/src/rsarmageddon/

RUN apt-get update \
 && apt-get install -y --no-install-recommends --no-install-suggests \
    python3-build python3-setuptools python3-pip \
 && apt-get clean \
 && pip install /usr/local/src/rsarmageddon/ \
 && rm -rf /usr/local/src/rsarmageddon/

ENTRYPOINT ["/usr/local/bin/rsarmageddon"]