# NFTs Art

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/umidrza/NFTs_Art.git
    cd NFTs_Art
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create the `.env` file for email configuration:

    Create a `.env` file in the root directory of your project with the following variables to set up email functionality:

    ```plaintext
    EMAIL_HOST_USER='your-email-address'
    EMAIL_HOST_PASSWORD='your-password'
    ```

5. Set up the database:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser (for admin access):

    ```bash
    python manage.py createsuperuser
    ```

7. Run the server:

    ```bash
    python manage.py runserver
    ```

## Admin Setup for Full Functionality

After completing the steps above, log in to the admin panel at `http://localhost:8000/admin` using the superuser credentials. You'll need to add the following data for the site to work properly:

1. **Categories**: Define different categories for Collections. (e.g., 'Art', 'Collectibles')
2. **Currencies**: Add the currencies supported by the platform (e.g., ETH, BTC).
3. **Avatars**: Upload default avatars for users.
4. **Blockchains**: Define the blockchains for NFTs. (e.g., 'Solona', 'Tezos')
5. **Providers**: Add wallet providers for blockchain interactions. (e.g., 'Wallet Connect', 'Metamask')

Once this data is added, the site will be fully functional.
