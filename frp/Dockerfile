FROM alpine:latest

ARG frp_version=0.52.3
ENV FRP_VERSION=$frp_version

COPY ./scripts/* /frp/scripts/
COPY ./frp_${FRP_VERSION}_linux_amd64.tar.gz /frp/

WORKDIR /frp
RUN apk update && apk add --no-cache bash && \
    chmod +x /frp/scripts/*.sh && \
    bash /frp/scripts/install.sh &&\
    rm -f /frp/scripts/install.sh &&\
    rm -f /frp/frp_${FRP_VERSION}_linux_amd64.tar.gz

VOLUME [ "/frp/conf" ]

ENTRYPOINT [ "/frp/scripts/run.sh" ]
