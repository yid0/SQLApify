ARG ALPINE_VERSION=latest
ARG WORKDIR_APP=/app
ARG BUILD_TARGET=postgres

ARG BUID_DEPS=sqlite-libs 

FROM yidoughi/pythopine:${ALPINE_VERSION} AS builder

ARG WORKDIR_APP

ARG VIRTUAL_ENV=${WORKDIR_APP}/venv

ARG BUID_DEPS
ARG BUILD_TARGET
ARG APP_ENV=dev

ARG MAIN_REQUIREMENT_FILE=requirements.${BUILD_TARGET}.txt

ARG DEPS_FILE_PATH=requirement/${APP_ENV}/${MAIN_REQUIREMENT_FILE}

WORKDIR ${VIRTUAL_ENV}

COPY --chown=1001:1001 requirements.txt  ${DEPS_FILE_PATH} ${VIRTUAL_ENV}

RUN mkdir ${VIRTUAL_ENV}/src && pip --no-cache-dir install -r requirements.txt -r ${MAIN_REQUIREMENT_FILE}

COPY --chown=1001:1001 env ${VIRTUAL_ENV}/env
COPY --chown=1001:1001  src ${VIRTUAL_ENV}/src
COPY --chown=1001 --chmod=755 scripts/start.sh ${VIRTUAL_ENV}/bin/start.sh

FROM yidoughi/fastpine:latest

ARG WORKDIR_APP=/app
ARG VIRTUAL_ENV=${WORKDIR_APP}/venv
ARG ARG BUILD_TARGET
ENV PYTHONPATH=${VIRTUAL_ENV}/src

ENV PATH="$VIRTUAL_ENV/bin:$PYTHONPATH:$PATH" \
    BUILD_TARGET=${BUILD_TARGET} \
    HOME=${VIRTUAL_ENV} \
    SQLAPIFY_ENV="dev" \
    SQLAPIFY_HOST="0.0.0.0" \
    SQLAPIFY_PORT="8000" \
    POSTGRES_PROTOCOL="postgresql" \
    POSTGRES_HOST="localhost" \
    POSTGRES_PORT="5432" \
    POSTGRES_ADMIN_USERNAME="postgres"\
    POSTGRES_ADMIN_PASSWORD="P@ssword" \
    POSTGRES_DATABASE="postgres" \
    LOG_LEVEL="DEBUG" \
    LOG_FORMAT="ecs" \
    SQLAPIFY_DB_SCHEMA="test" \
    SQLAPIFY_DB_USER="sqlapify_user" \
    SQLAPIFY_DB_PASSWORD="sqlapify0_P@ssword" \
    SQLAPIFY_DB_NAME="db_management"

WORKDIR ${HOME}

COPY --from=builder --chown=1001 ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN rm -rf /usr/lib/python**/__pycache__** && \
    find ${VIRTUAL_ENV} -type d -name "tests" -exec rm -rf {} + && \
    find /usr/lib/ -type d -name "tests" -exec rm -rf {} + && \
    find /usr/lib/ -type d -name "docs" -exec rm -rf {} + && \
    find ${VIRTUAL_ENV} -type d -name "__pycache__" -exec rm -rf {} + && \
    rm -rf /var/cache/apk/* /tmp/* /**/.cache/pip ${VIRTUAL_ENV}/requirement*


USER 1001

EXPOSE ${SQLAPIFY_PORT}

ENTRYPOINT ["start.sh"]