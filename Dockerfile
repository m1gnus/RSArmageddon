FROM sagemath/sagemath:10.2
USER root
SHELL [ "/bin/bash", "-c" ]

ENV PATH "$PATH:/home/sage/.local/bin"

RUN apt update && apt install -y --no-install-recommends --no-install-suggests python3-build python3-setuptools python3-venv python3-pip \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && chown -R sage:sage .
USER sage
COPY . .
RUN pip install .

ENTRYPOINT [ "rsarmageddon" ]

