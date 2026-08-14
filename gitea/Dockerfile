# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
FROM ${BUILD_FROM}

# Execute during the build of the image
ARG TEMPIO_VERSION=2026.07.0
ARG TARGETARCH
RUN \
    if [ -z "${TARGETARCH}" ]; then \
        echo "TARGETARCH is not set, please use Docker BuildKit for the build." && exit 1; \
    fi \
    && case "${TARGETARCH}" in \
        amd64) tempio_arch="amd64" ;; \
        arm64) tempio_arch="aarch64" ;; \
        *) echo "Unsupported TARGETARCH: ${TARGETARCH}" && exit 1 ;; \
    esac \
    && curl -sSLf -o /usr/bin/tempio \
        "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${tempio_arch}" \
    && chmod a+x /usr/bin/tempio

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk --no-cache add \
    git \
    gitea \
    sqlite \
    su-exec \
    bash \
    curl \
    openssh-client \
    openssh-server \
    openssh-sftp-server \
    openssh-keygen \
    mailcap \
    tzdata \
    ca-certificates \
    nginx

# Ensure git user/group exists with proper home directory
RUN if ! getent group git >/dev/null 2>&1; then addgroup -S -g 1000 git; fi \
    && if ! getent passwd git >/dev/null 2>&1; then adduser -S -H -D -h /data/git -s /bin/bash -u 1000 -G git git; fi

ENV USER=git
ENV HOME=/data/git
ENV GITEA_CUSTOM=/data/gitea
ENV GITEA_WORK_DIR=/data/gitea

# Setup directories and compatibility symlinks
RUN mkdir -p /app/gitea /data/git/.gnupg /var/log/nginx /var/lib/nginx /run/nginx /run/sshd /var/empty \
    && chmod 755 /run/sshd /var/empty \
    && ln -sf /usr/bin/gitea /app/gitea/gitea \
    && ln -sf /usr/bin/gitea /usr/local/bin/gitea

# Copy root filesystem
COPY rootfs /

# Set permissions for s6 services and scripts
RUN chmod +x \
    /etc/s6-overlay/s6-rc.d/init-gitea/run \
    /etc/s6-overlay/s6-rc.d/init-gitea/up \
    /etc/s6-overlay/s6-rc.d/gitea/run \
    /etc/s6-overlay/s6-rc.d/gitea/finish \
    /etc/s6-overlay/s6-rc.d/nginx/run \
    /etc/s6-overlay/s6-rc.d/sshd/run

# Build arguments
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="Jean-Michel Picod <jmichel.p@gmail.com>" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Home Assistant Community Apps" \
    org.opencontainers.image.authors="Jean-Michel Picod <jmichel.p@gmail.com>" \
    org.opencontainers.image.licenses="Apache 2.0" \
    org.opencontainers.image.url="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
