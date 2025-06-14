# FastAPI + WordPress Example

This example shows how to run WordPress with `nginx` and `php-fpm` while exposing extra pages implemented with FastAPI.  User authentication is shared with WordPress so existing WordPress logins also protect API routes.

## Services

- **nginx** – serves WordPress and proxies `/api` requests to FastAPI
- **wordpress** – standard PHP-FPM WordPress container
- **db** – MariaDB for WordPress content
- **fastapi** – REST/GraphQL/RSS services implemented with FastAPI

All services are orchestrated with `docker-compose` and run on both Windows (via WSL2/Docker Desktop) and Linux.

## Usage

1. Copy `.env.example` to `.env` in the `fastapi` directory and adjust database settings if necessary.

```powershell
cp fastapi/.env.example fastapi/.env
```

2. Start the stack:

```powershell
docker-compose up -d --build
```

3. Visit `http://localhost` for WordPress. FastAPI is available under `http://localhost/api`.

## FastAPI Endpoints

- `GET /api/posts/` – list published WordPress posts (requires WordPress credentials via HTTP Basic)
- `GET /api/rss` – RSS feed of the latest posts
- `POST /api/graphql` – GraphQL endpoint exposing posts
- `GET /api/protected` – sample protected route

## WordPress GraphQL

Install the [WPGraphQL](https://www.wpgraphql.com/) plugin in WordPress to expose WordPress data through GraphQL directly.  The FastAPI service provides an additional lightweight GraphQL layer using the same database.

## Best Practices

- Keep WordPress and FastAPI containers stateless by mounting persistent volumes for the database and `wp-content`.
- Use HTTPS in production and configure strong secrets for database and application services.
- Consider a plugin such as "JWT Authentication for WP REST API" if token-based auth is preferred.
- Separate configuration from code using environment variables as shown in `.env.example`.
