# Kamalia Khaddar — E-Commerce Store

A professional, responsive full-stack e-commerce web application built with **Django** and **Tailwind CSS**. Sells premium Khaddar suits, fabrics, and textiles.

## Features

- **Product Catalog**: Browse products by category with search, sort, and pagination
- **Shopping Cart**: Session-based cart with AJAX add-to-cart and quantity management
- **Checkout**: Complete checkout flow with order creation and confirmation
- **User Authentication**: Registration, login, profile with order history
- **Admin Dashboard**: Manage products, orders, and inventory with image previews
- **REST API**: JSON endpoints for products, cart, and orders
- **Responsive Design**: Mobile-first with Tailwind CSS

## Tech Stack

- **Backend**: Django 6.0 (Python 3.12)
- **Frontend**: Tailwind CSS (via CDN), Font Awesome icons, Inter + Playfair Display fonts
- **Database**: SQLite (dev) / PostgreSQL (production)
- **API**: Django REST Framework

## Local Setup

### 1. Clone & Install

```bash
# Clone the repository
cd kamalia_store

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit:
- **Store**: https://www.kamaliakhaddark.com/

### 5. Add Products

1. Log in to the admin panel
2. Go to **Products → Add Product**
3. Fill in name, category, price, description, and upload an image
4. Mark products as **Featured** to show them on the home page

## Project Structure

```
├── kamalia_store/       # Django project settings
│   ├── settings.py      # Development settings
│   ├── settings_prod.py # Production settings (PostgreSQL, DEBUG=False)
│   └── urls.py          # Root URL configuration
├── products/            # Product catalog app
├── cart/                # Shopping cart app (session-based)
├── orders/              # Order & checkout app
├── users/               # Authentication & profile app
├── templates/           # All HTML templates (Tailwind CSS)
├── static/              # Static files (CSS, JS)
├── media/               # Uploaded product images
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
```

## API Endpoints

| Endpoint                      | Method | Description          |
|-------------------------------|--------|----------------------|
| `/api/products/`              | GET    | List all products    |
| `/api/products/{slug}/`       | GET    | Product detail       |
| `/api/cart/`                  | GET    | View cart            |
| `/api/cart/add/{id}/`         | POST   | Add to cart          |
| `/api/cart/remove/{id}/`      | POST   | Remove from cart     |
| `/api/orders/`                | GET    | List user orders     |
| `/api/orders/{id}/`           | GET    | Order detail         |

## Production Deployment (AWS EC2)

### 1. Server Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

### 2. Clone & Configure

```bash
cd /home/ubuntu
git clone <repo-url> kamalia_store
cd kamalia_store
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env
# Edit .env with your production values
nano .env
```

### 3. Database Setup

```bash
sudo -u postgres psql
CREATE DATABASE kamalia_store;
CREATE USER kamalia_user WITH PASSWORD 'your_password';
ALTER ROLE kamalia_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE kamalia_store TO kamalia_user;
\q
```

### 4. Django Setup

```bash
export DJANGO_SETTINGS_MODULE=kamalia_store.settings_prod
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### 5. Gunicorn

```bash
# /etc/systemd/system/kamalia.service
[Unit]
Description=Kamalia Store Gunicorn
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/kamalia_store
ExecStart=/home/ubuntu/kamalia_store/venv/bin/gunicorn kamalia_store.wsgi:application --bind 0.0.0.0:8000 --workers 3
Restart=always
Environment="DJANGO_SETTINGS_MODULE=kamalia_store.settings_prod"

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start kamalia
sudo systemctl enable kamalia
```

### 6. Nginx

```nginx
# /etc/nginx/sites-available/kamalia
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /home/ubuntu/kamalia_store/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/kamalia_store/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/kamalia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. HTTPS (Certbot)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## License

MIT License
