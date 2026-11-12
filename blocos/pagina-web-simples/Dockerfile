# Bloco Página web simples: imagem padrão da esteira V3A.
# Servidor web estático (busybox httpd), sem root, porta interna fixa 8080.
# Nenhum repositório escreve este arquivo: a esteira o usa como está.
FROM busybox:1.37.0@sha256:a7dbc319b1438115a207e11930dc4bb3e643dcb3ec0bdd694bb36cd8fad289ec
ARG HEALTHCHECK=/
ENV V3A_HEALTHCHECK=${HEALTHCHECK}
COPY site/ /www/
COPY v3a-projeto.yml /v3a/v3a-projeto.yml
USER 65534:65534
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -q -O /dev/null "http://127.0.0.1:8080${V3A_HEALTHCHECK}" || exit 1
ENTRYPOINT ["httpd", "-f", "-v", "-p", "8080", "-h", "/www"]
