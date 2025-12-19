# HTTPS Deployment Configuration

## SSL/TLS Setup
This application is configured to run over HTTPS using SSL/TLS certificates.

### Nginx Example Configuration
```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/fullchain.pem;
    ssl_certificate_key /etc/ssl/private/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
