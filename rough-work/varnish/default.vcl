vcl 4.0;

backend default {
    .host = "nginx";
    .port = "80";
}

sub vcl_recv {
    if (req.method == "GET" || req.method == "HEAD") {
        return (hash);
    }
    return (pass);
}

sub vcl_backend_response {
    set beresp.ttl = 5m;
}
