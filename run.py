import requests


def error_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception:
            ...

    return wrapper


class ServerClient:
    def __init__(self):
        self.base_url_clients = "http://ip172-18-0-35-cpgm3t0l2o9000960kd0-80.direct.labs.play-with-docker.com/api/v1"
        self.base_url_reservations = "http://127.0.0.1:8000/api/v1"
        self.session = requests.Session()
        self.session.headers.update({"x-api-secret": "HDHffpH3pqY64svULpEFhg=="})

    def print_error_if_needed(self, response):
        if response.status_code >= 400:
            print(response.json()["errors"][0]["message"])

    @error_decorator
    def register(self, fio, email, phone, password):
        url = f"{self.base_url_clients}/clients/register"
        payload = {
            "fio": fio,
            "email": email,
            "phone_number": phone,
            "password": password,
        }
        response = self.session.post(url, json=payload)
        self.print_error_if_needed(response)
        return response.json()

    @error_decorator
    def login(self, email, password):
        url = f"{self.base_url_clients}/clients/login"
        payload = {"email": email, "password": password}
        response = self.session.post(url, json=payload)
        self.print_error_if_needed(response)
        return response.json()

    @error_decorator
    def get_client(self, client_id):
        url = f"{self.base_url_clients}/clients/{client_id}"
        response = self.session.get(url)
        self.print_error_if_needed(response)
        return response.json()

    @error_decorator
    def get_clients_list(self):
        url = f"{self.base_url_clients}/clients"
        response = self.session.get(url)
        self.print_error_if_needed(response)
        return response.json()

    @error_decorator
    def get_tebles_list(self):
        url = f"{self.base_url_reservations}/tables"
        response = self.session.get(url)
        self.print_error_if_needed(response)
        return response.json()

    @error_decorator
    def get_tables_status(self, datetime_string):
        url = f"{self.base_url_reservations}/tables/status"
        params = {"reservation_start": datetime_string}
        response = self.session.get(url, params=params)
        self.print_error_if_needed(response)
        return response.json()

    @error_decorator
    def create_reservation(self, table_id, client_id, datetime_string, duration):
        url = f"{self.base_url_reservations}/reservations"
        response = self.session.post(
            url,
            json={
                "table_id": table_id,
                "client_id": client_id,
                "reservation_start": datetime_string,
                "duration": duration,
            },
            cookies=self.session.cookies.get_dict(),
        )
        self.print_error_if_needed(response)
        return response.json()

    @error_decorator
    def delete_reservation(self, reservation_id):
        url = f"{self.base_url_reservations}/reservations/{reservation_id}"
        response = self.session.delete(url)
        self.print_error_if_needed(response)
        return response.json()


def main():
    client = ServerClient()

    # Register a new client
    fio = "John Doe"
    email = "john.doe@example.com"
    phone = "123456789"
    password = "securepassword"
    print("Registering...")
    register_response = client.register(fio, email, phone, password)
    print(register_response)

    input("Press Enter to continue...")

    # Log in with the new client
    print("Logging in...")
    login_response = client.login(email, password)
    print(login_response)

    input("Press Enter to continue...")

    # Get client information
    client_id = 2
    print(f"Getting client information for ID {client_id}...")
    client_info = client.get_client(client_id)
    print(client_info)

    input("Press Enter to continue...")

    # Get clients list
    print("Getting clients list...")
    clients_list = client.get_clients_list()
    print(clients_list)

    input("Press Enter to continue...")

    # Get tables list
    print("Getting tables list...")
    tables_list = client.get_tebles_list()
    print(tables_list)

    input("Press Enter to continue...")

    # Check tables status
    datetime_string = "2024-06-09T12:00:00"
    print(f"Checking tables status for {datetime_string}...")
    tables_status = client.get_tables_status(datetime_string)
    print(tables_status)

    input("Press Enter to continue...")

    # Create a reservation
    print("Creating a reservation...")
    reservation_response = client.create_reservation(1, client_id, datetime_string, 30)
    print(
        reservation_response
        if len(str(reservation_response)) < 300
        else "Error creating reservation"
    )

    input("Press Enter to continue...")

    # Delete a reservation
    reservation_id = 1
    print(f"Deleting reservation with ID {reservation_id}...")
    delete_response = client.delete_reservation(reservation_id)
    print(delete_response)


# Example usage
if __name__ == "__main__":
    main()
