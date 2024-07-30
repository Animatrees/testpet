# "Famous Women" Website

A website dedicated to famous women in history and modern times. 
Developed as part of a Django course.

## Contents

- [Brief Description](#brief-description)
- [Technologies](#technologies)
- [Main Features](#main-features)
- [Installation and Running](#installation-and-running)
- [Contributing](#contributing)
- [License](#license)
- [Contacts](#contacts)

## Brief Description

This project is a web application that contains information 
about outstanding women from various fields. 
Users can view profiles of women, filter information by categories
and countries, and add new entries after logging in.

## Technologies
* Django
* PostgreSQL
* Redis
* OAuth

## Main Features

- Viewing a list of famous women
- Filtering by categories and countries
- Adding new entries
- Basic authentication system

## Installation and Running

1. Clone the repository:
    ```sh
    git clone https://github.com/Animatrees/testpet.git
    cd testpet
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # For Unix or MacOS
    # or
    venv\Scripts\activate  # For Windows
    ```

3. Create a `.env` file and set the environment variables:
    ```env
    SECRET_KEY='your-secret-key'
    DEBUG=True
    DATABASE_URL='your-database-url'
    ```

4. Install dependencies and apply migrations:
    ```sh
    pip install -r requirements.txt
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Start Redis:
    ```sh
    sudo service redis-server start
    ```

7. Run the server:
    ```sh
    python manage.py runserver
    ```

8. Open your browser and navigate to `http://localhost:8000`

## Contributing

This is just a learning project, but if you want to contribute...))

1. Fork the repository
2. Create a new branch:
    ```sh
    git checkout -b feature/AmazingFeature
    ```
3. Make changes and commit them:
    ```sh
    git commit -am 'Add some AmazingFeature'
    ```
4. Push the branch:
    ```sh
    git push origin feature/AmazingFeature
    ```
5. Create a new Pull Request

## License
This project is licensed under the [MIT License](LICENSE.md).

## Contacts
If you have any questions or suggestions, please open an issue in this repository.