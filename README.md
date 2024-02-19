# Grappers
Use httpx to fetch sth

## Install Dependencies
```bash
poetry install --only=main --no-root
```

## Usage
```bash
wget http://g.waketzheng.top/https://raw.githubusercontent.com/Homebrew/homebrew-core/c5de89fc9934080854f8bfbcd999109ee2c738c4/Formula/e/erlang.rb
```

## Deployment
```bash
gunicorn app:app --bind 0.0.0.0:9337 --worker-class uvicorn.workers.UvicornWorker --daemon
```
