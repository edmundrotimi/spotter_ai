==========================
Spotter AI Project
==========================

The code builds a Django (v3.2.23) based API to find optimal fuel stations along a driving route in the USA. 
A CSV file of fuel stations is loaded and updated with latitude/longitude using geocoding based on addresses using mapquest. 
After, *OpenRouteService* API fetches route coordinates with a *Random Forest* model is trained to predict nearest 
cost-effective fuel stops based on features like fuel price. Using vehicle constraints (500-mile range, 10 MPG), 
the total cost, valid route points are then found using efficient methods for performance. the response also  
 a *Google Maps* link of the valid route. 

==========

Setup
==========

Set environment variable for Django Secret Key, Debug, Allowed Host, Django ENV, Admin Path, and Idle logout timeout. 
Also add configuration for Database, *Defender* (documentation Link: https://django-defender.readthedocs.io/en/latest) 
and *Maintenance mode* (documentation Link: https://github.com/fabiocaccamo/django-maintenance-mode). 
Ensure *Redis* is installed, for quick install use: https://github.com/tporadowski/redis/releases


.. code-block:: bash

    # Security
    SECRET_KEY = '...'
    DEBUG = ...
    ALLOWED_HOSTS = '..'
    DJANGO_ENV = ... # either 'Production' or 'Development' 
    ADMIN_PATH = ...
    AUTO_LOGOUT_IDLE_TIME = ... # in seconds


    # Database
    ENGINE = ...
    NAME = ...
    HOST = ...
    USER = ...
    PASSWORD = ...
    PORT = ...

    # Defender Settings (Documentation Link: https://django-defender.readthedocs.io/en/latest/)
    DEFENDER_LOGIN_FAILURE_LIMIT = ...
    DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME = ...
    DEFENDER_COOLOFF_TIME = ...
    DEFENDER_ATTEMPT_COOLOFF_TIME = ...
    DEFENDER_LOCKOUT_URL = ... 
    DEFENDER_USERNAME_FORM_FIELD = ... # use email based on documentation and since a custom user is used
    DEFENDER_STORE_ACCESS_ATTEMPTS = ...
    DEFENDER_ACCESS_ATTEMPT_EXPIRATION = ...
    DEFENDER_REDIS_URL = ... # use 'redis://localhost:6379/0' based on documentation
    DEFENDER_GET_USERNAME_FROM_REQUEST_PATH = ... # use 'defender.utils.username_from_request' based on documentation
    DEFENDER_REVERSE_PROXY_HEADER = ... # use 'HTTP_X_FORWARDED_FOR' based on documentation
    DEFENDER_BEHIND_REVERSE_PROXY = ...

    # Documentation Link: https://github.com/fabiocaccamo/django-maintenance-mode
    MAINTENANCE_MODE = ...
    MAINTENANCE_MODE_STATE_BACKEND = ...
    MAINTENANCE_MODE_STATE_FILE_PATH = ...
    MAINTENANCE_MODE_IGNORE_ADMIN_SITE = ...
    MAINTENANCE_MODE_IGNORE_ANONYMOUS_USER = ...
    MAINTENANCE_MODE_IGNORE_AUTHENTICATED_USER = ...
    MAINTENANCE_MODE_IGNORE_STAFF = ...
    MAINTENANCE_MODE_IGNORE_SUPERUSER = ...
    MAINTENANCE_MODE_GET_CLIENT_IP_ADDRESS = ...
    MAINTENANCE_MODE_GET_CONTEXT = ...
    MAINTENANCE_MODE_IGNORE_TESTS = ...
    MAINTENANCE_MODE_LOGOUT_AUTHENTICATED_USER = ...
    MAINTENANCE_MODE_RESPONSE_TYPE = ... # use 'html' base on documentation
    MAINTENANCE_MODE_STATUS_CODE = ...
    MAINTENANCE_MODE_RETRY_AFTER = ...
    MAINTENANCE_MODE_IGNORE_URLS = ...




Additional Setup
-----------------

Set config for *Sentry* and *OpenRouteService* API Key.

.. code-block:: bash

    # Sentry DNS and Report(CSP) url
    SENTRY_DNS= '...'
    SENTRY_REPORT_URL = '...'

    # api key
    OPENROUTESERVICE_API_KEY =''

    # mapquest api key (https://developer.mapquest.com/)
    MAPQUEST_API_KEY = ''



Running Project
----------------

Setup
^^^^^^^^^^^
This make command will run six commands needed to setup everythin. First it installs all poetry packages, then perform Django
makemigrations and migrate. It also installs pre-commit. It lastly runs a Django custom management command to first
load and update CSV file of fuel stations with latitude/longitude using geocoding based on addresses  
(the updated file is  already created and this action will be skipped) and 
save a trained *Random Forest* model (the pickle file is  already created and this action will be skipped)

.. code-block:: bash

    make setup


create Superuser
^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    make superuser


run Unit Test
^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    make unit-test



run Integrared Test
^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    make integrated-test


Run Server
^^^^^^^^^^^
.. code-block:: bash

    make runserver




Other Setups
^^^^^^^^^^^^^^
If deployed to a live server ensure you collect static assets

.. code-block:: bash

    make collectstatic

