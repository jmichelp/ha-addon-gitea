# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Execute during the build of the image
ARG TEMPIO_VERSION
ARG BUILD_ARCH
RUN \
    curl -sSLf -o /usr/bin/tempio \
    "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk --no-cache add \
    su-exec \
    ca-certificates \
    sqlite \
    bash \
    git \
    subversion \
    linux-pam \
    s6 \
    curl \
    openssh \
    tzdata \
    gettext && \
    PATH=$PATH:/usr/bin/ 

RUN addgroup \
    -S -g 1000 \
    git && \
  adduser \
    -S -H -D \
    -h /data/git \
    -s /bin/bash \
    -u 1000 \
    -G git \
    git && \
  echo "git:$(dd if=/dev/urandom bs=24 count=1 status=none | base64)" | chpasswd

ENV USER git
ENV GITEA_CUSTOM /data/git
ENV GODEBUG=netdns=go

COPY data /data
VOLUME ["/data"]

ARG GITEA_VERSION
RUN  \
     ARCH="${BUILD_ARCH}" \
     && if [ "${BUILD_ARCH}" = "aarch64" ]; then ARCH="arm64"; fi \
     && if [ "${BUILD_ARCH}" = "armv7" ]; then ARCH="arm-6"; fi \
     && if [ "${BUILD_ARCH}" = "armhf" ]; then ARCH="arm-5"; fi \
     && if [ "${BUILD_ARCH}" = "amd64" ]; then ARCH="amd64"; fi \
     && if [ "${BUILD_ARCH}" = "i368" ]; then ARCH="368"; fi \
     \
    && mkdir -p /app/gitea \
    && curl -SLo /app/gitea/gitea https://github.com/go-gitea/gitea/releases/download/v${GITEA_VERSION}/gitea-${GITEA_VERSION}-linux-${ARCH}  \
    && chmod 0755 /app/gitea/gitea \
    && ln -s /app/gitea/gitea /usr/local/bin/gitea \
    && apk del subversion  \
    && rm -fr \
        /tmp/* \
        /var/{cache,log}/* \
        /var/lib/apt/lists/* 

# Copy root filesystem
COPY rootfs /

RUN for file in /etc/services.d/*/*; do \
dos2unix $file; \
chmod a+xwr $file; \
done


# Build arguments
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
   io.hadd.type="addon" \
   io.hass.name="${BUILD_NAME}" \
   io.hass.description="${BUILD_DESCRIPTION}" \
   io.hass.arch="${BUILD_ARCH}" \
   io.hass.version=${BUILD_VERSION} \
   maintainer="Jean-Michel Picod <jmichel.p@gmail.com>" \
   org.opencontainers.image.title="${BUILD_NAME}" \
   org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
   org.opencontainers.image.vendor="Home Assistant Community Add-ons" \
   org.opencontainers.image.authors="Jean-Michel Picod <jmichel.p@gmail.com>" \
   org.opencontainers.image.licenses="MIT" \
   org.opencontainers.image.url="https://addons.community" \
   org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
   org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
   org.opencontainers.image.created=${BUILD_DATE} \
   org.opencontainers.image.revision=${BUILD_REF} \
   org.opencontainers.image.version=${BUILD_VERSION}
