FROM sagemath/sagemath:10.2 as builder 

ENV WD "/home/sage/app" 
ENV VENV "."
ENV PATH "$VENV/bin:$PATH"
WORKDIR "${WD}"
USER root
SHELL ["/bin/bash", "-c"]
RUN apt update && apt install -y --no-install-recommends --no-install-suggests python3-build python3-setuptools python3-venv python3-pip \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && chown -R sage:sage ${WD}
USER sage
COPY . ${WD}
RUN python3 -m venv $VENV && source bin/activate && pip install .

ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD [ "bin/rsarmageddon" ]
