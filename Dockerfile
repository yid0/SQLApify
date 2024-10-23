ARG ALPINE_VERSION=latest
ARG WORKDIR_APP=/app

ARG BUID_DEPS=sqlite-libs 

FROM yidoughi/pythopine:${ALPINE_VERSION} AS builder

ARG WORKDIR_APP

ARG VIRTUAL_ENV=${WORKDIR_APP}/venv

ARG BUID_DEPS
ARG BUILD_TARGET=postgres
ARG APP_ENV=dev

ARG MAIN_REQUIREMENT_FILE=requirements.${BUILD_TARGET}.txt

ARG DEPS_FILE_PATH=requirement/${APP_ENV}/${MAIN_REQUIREMENT_FILE}

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR ${VIRTUAL_ENV}

COPY --chown=1001:1001 requirements.txt  ${DEPS_FILE_PATH} ${VIRTUAL_ENV}

RUN mkdir ${VIRTUAL_ENV}/src && pip --no-cache-dir install -r requirements.txt -r ${MAIN_REQUIREMENT_FILE}

COPY --chown=1001:1001 env ${VIRTUAL_ENV}/env
# COPY --chown=1001:1001 db ${VIRTUAL_ENV}/db 
# COPY --chown=1001:1001 model ${VIRTUAL_ENV}/model

COPY --chown=1001:1001  src ${VIRTUAL_ENV}/src
# COPY --chown=1001:1001  main.py ${VIRTUAL_ENV}/main.py

RUN rm requirements.txt -r ${MAIN_REQUIREMENT_FILE}  

# RUN ls ./lib/python3.*/site-packages/ | grep email_validator && apk --purge del .build-deps


FROM yidoughi/fastpine:latest

ARG WORKDIR_APP=/app
ARG VIRTUAL_ENV=${WORKDIR_APP}/venv

ENV HOME=${VIRTUAL_ENV}

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR ${HOME}

RUN ls -la /usr/lib

COPY --from=builder --chown=1001 ${VIRTUAL_ENV} ${VIRTUAL_ENV} 


RUN rm -rf /var/cache/apk/* /tmp/* && fastapi --help

# fastapi run src/main.py --host 0.0.0.0

# CMD ["fastapi", "run", "src/main.py", "--host 0.0.0.0"]

CMD ["tail", "-f", "/dev/null"]