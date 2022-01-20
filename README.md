# pyshort
Url shortener on http://pyshort.ru

## Deployment
Generate RSA key pairs for JWT tokens generating:
```bash
ssh-keygen -t rsa -b 4096 -m PEM -f ./keys/rs256.key
```

Database migrations:
```bash
alembic upgrade head
alembic downgrade base
```
