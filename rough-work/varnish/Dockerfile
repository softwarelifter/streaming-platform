FROM varnish:latest
COPY default.vcl /etc/varnish/default.vcl
EXPOSE 80
CMD ["varnishd", "-F", "-f", "/etc/varnish/default.vcl", "-s", "malloc,256m"]
