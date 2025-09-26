# E-Farming Portal for Small Scale Farmers

A comprehensive Django-based web platform to empower Kenyan small-scale farmers, buyers, suppliers, and extension agents. The portal provides tools for farm management, crop marketing, input supply, advisory services, and more.

## Features

- User registration and profiles for farmers, buyers, suppliers, and agents
- Farm and crop management
- Product listing, reviews, and wishlists
- Shopping cart and order management
- Payment integration (M-Pesa, Airtel Money, Bank Transfer, Cash on Delivery)
- Delivery management and tracking
- Market prices and demand forecasts
- Agricultural input marketplace
- Training, advisory, and support ticketing
- County, sub-county, and ward-based location data

## Project Structure


```
E_Farming_portal_for_small_scale_farmers/ 
    ├── manage.py 
    ├── db.sqlite3 
    ├── E_Farming_portal_for_small_scale_farmers/ 
        │ 
        ├── settings.py 
        │ 
        ├── urls.py 
        │ 
        └── ... 
    ├── main_application/ 
    │ 
    ├── models.py 
    │ 
    ├── views.py 
    │ 
    ├── admin.py 
    │ 
    ├── management/ 
        │ 
        │ 
        └── commands/ 
            │ 
            │ 
            └── seed_data.py 
                │ 
                └── ... 
    ├── templates/ 
    ├── static/ 
    └── media/

```

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- [Django](https://www.djangoproject.com/) 5.x

### Installation

1. **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd E_Farming_portal_for_small_scale_farmers
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

4. **Seed the database with sample Kenyan agricultural data:**
    ```sh
    python manage.py seed_data
    ```
    - To clear existing data before seeding:
    ```sh
    python manage.py seed_data --clear
    ```

5. **Create a superuser (admin):**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

7. **Access the portal:**
    - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Custom Management Commands

- [seed_data](http://_vscodecontentref_/3): Seeds the database with realistic Kenyan agricultural data for development and testing.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License.

---

**Developed for Kenyan small-scale farmers and the agricultural ecosystem.**