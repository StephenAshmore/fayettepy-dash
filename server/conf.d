worker_processes 1;

events {
  worker_connections 1024;
  accept_mutex off;
}

http {
  include mime.types;
  client_max_body_size 10m;

  gzip on;
  gzip_vary on;
  gzip_static on;
  gzip_types
    text/plain
    text/css
    application/json
    application/javascript
    application/x-javascript;

  server {
    listen 8002;

    location = /hi {
      access_log off;
      return 200 'Hi';
    }

    location / {
      # checks for static file, if not found proxy to app
      try_files $uri @proxy_to_app;
    }

    location @proxy_to_app { 
        proxy_set_header      X-Real_IP $remote_addr;
        proxy_set_header      X-Forwarded-Host $server_name;
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        proxy_pass http://app:8002;
    }
  }
}
