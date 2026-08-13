# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
FROM ghcr.io/home-assistant/base:latest

# Execute during the build of the image
ARG BUILD_ARCH

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk --no-cache add \
    su-exec \
    ca-certificates \
    sqlite \
    bash \
    git \
    git-lfs \
    gnupg \
    tzdata \
    curl \
    openssh-client \
    openssh-keygen

RUN addgroup -S -g 1000 git \
    && adduser -S -H -D -h /data/git -s /bin/bash -u 1000 -G git git

ENV USER=git
ENV HOME=/data/git
ENV GITEA_CUSTOM=/data/gitea
ENV GODEBUG=netdns=go
ENV GITEA_WORK_DIR=/data/gitea

ARG GITEA_VERSION
ARG GITEA_GPG_KEYID
RUN \
    ARCH="${BUILD_ARCH}" \
    && if [ "${BUILD_ARCH}" = "aarch64" ]; then ARCH="arm64"; fi \
    && if [ "${BUILD_ARCH}" = "amd64" ]; then ARCH="amd64"; fi \
    && mkdir -p /app/gitea \
    && curl -SLo /app/gitea/gitea "https://github.com/go-gitea/gitea/releases/download/v${GITEA_VERSION}/gitea-${GITEA_VERSION}-linux-${ARCH}" \
    && curl -SLo /app/gitea/gitea.asc "https://github.com/go-gitea/gitea/releases/download/v${GITEA_VERSION}/gitea-${GITEA_VERSION}-linux-${ARCH}.asc" \
    && ( gpg --keyserver keys.openpgp.org --recv-keys "${GITEA_GPG_KEYID}" \
      || gpg --keyserver keyserver.ubuntu.com --recv-keys "${GITEA_GPG_KEYID}" \
      || gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys "${GITEA_GPG_KEYID}" ) \
    && gpg --verify /app/gitea/gitea.asc /app/gitea/gitea \
    && chmod 0755 /app/gitea/gitea \
    && ln -s /app/gitea/gitea /usr/local/bin/gitea \
    && rm -rf /root/.gnupg /tmp/* /var/cache/apk/*

# Copy root filesystem
COPY rootfs /

# Set permissions for s6 services and scripts
RUN chmod +x \
    /etc/s6-overlay/s6-rc.d/init-gitea/run \
    /etc/s6-overlay/s6-rc.d/init-gitea/up \
    /etc/s6-overlay/s6-rc.d/gitea/run \
    /etc/s6-overlay/s6-rc.d/gitea/finish

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
    org.opencontainers.image.vendor="Home Assistant Community Add-ons" \
    org.opencontainers.image.authors="Jean-Michel Picod <jmichel.p@gmail.com>" \
    org.opencontainers.image.licenses="Apache 2.0" \
    org.opencontainers.image.url="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
