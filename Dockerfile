ARG ALPINE_VERSION=latest
ARG WORKDIR_APP=/app

FROM yidoughi/pythopine:${ALPINE_VERSION} AS builder

ARG WORKDIR_APP

ARG VIRTUAL_ENV=${WORKDIR_APP}/venv

ARG BUILD_TARGET=pg
ARG APP_ENV=dev

ARG MAIN_REQUIREMENT_FILE=requirements.${BUILD_TARGET}.txt

ARG DEPS_FILE_PATH=requirement/${APP_ENV}/${MAIN_REQUIREMENT_FILE}

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR ${VIRTUAL_ENV}

COPY --chown=1001:1001 requirements.txt  ${DEPS_FILE_PATH} ${VIRTUAL_ENV}

RUN pip install -r requirements.txt -r ${MAIN_REQUIREMENT_FILE} && pip install email-validator && ls -la 


COPY --chown=1001:1001 env ${VIRTUAL_ENV}/env
COPY --chown=1001:1001 db ${VIRTUAL_ENV}/db 
COPY --chown=1001:1001 model ${VIRTUAL_ENV}/model

COPY --chown=1001:1001  *.py ${VIRTUAL_ENV}

RUN rm requirements.txt -r ${MAIN_REQUIREMENT_FILE}  

RUN ls ./lib/python3.*/site-packages/ | grep email_validator


FROM yidoughi/fastpine:latest

ARG WORKDIR_APP=/app
ARG VIRTUAL_ENV=${WORKDIR_APP}/venv

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR ${WORKDIR_APP}

# COPY --from=builder /usr/lib /usr/lib
COPY --from=builder --chown=1001 ${VIRTUAL_ENV} ${VIRTUAL_ENV} 


RUN rm -rf /var/cache/apk/* /tmp/* && fastapi --help
#dev --host 0.0.0.0 ${WORKDIR_APP}/status.py

CMD ["tail", "-f", "/dev/null"]