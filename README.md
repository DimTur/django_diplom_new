#  Graduation work to Python-developer "API Service for ordering goods for retail chain"

## Discription

The app using for automatic purchases in retail chain. Service user - buyer (trade network manager, 
who can purchase goods for sale in the shop) and goods supplier.

**The client (buyer):**

- Trade network manager through API makes daily catalog purchases. 
  There are goods from several suppliers are presented.
- In one order, you can choose goods from different suppliers. This will depend on the cost.
- User can registration, login and change information about himself using the API.
    
**Supplier:**

- Through the API, informs the service about the price update.
- Enable/Disable order taking.
- Может получать список оформленных заказов (с товарами из его прайса).
- Receive a list of completed orders (with goods from its price list).

## Launch

**Install dependencies**

    pip install -r requirements.txt

**Create a base and run migrations:**

    manage.py makemigrations

    manage.py migrate

    manage.py createsuperuser
  
**Run Redis and Celery**

    docker run -d -p 6379:6379 redis

    python -m celery -A orders worker -l info

**Run command**

    python manage.py runserver

**[Request documentation in Postman](https://www.postman.com/docking-module-engineer-24329358/workspace/my-diplom)**

**Request documentation in drf-spectacular**

Generate API schema with the CLI:

    $ ./manage.py spectacular --color --file schema.yml
    
    $ docker run -p 80:8080 -e SWAGGER_JSON=/schema.yml -v ${PWD}/schema.yml:/schema.yml swaggerapi/swagger-ui

use address:

    /api/schema/

    /api/schema/swagger-ui/

    /api/schema/redoc/
