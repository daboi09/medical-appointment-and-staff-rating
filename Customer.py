import User


class Customer(User.User):
    count_id = 1

    def __init__(self, first_name, last_name, gender, membership, remarks, email, date_joined, address, phone, birth, password):
        super().__init__(first_name, last_name, gender, membership, remarks, email, date_joined, address, phone, birth, password)
        self.__customer_id = Customer.count_id
        self.__email = email
        self.__date_joined = date_joined
        self.__address = address
        self.__phone = phone
        self.__birth = birth
        self.__password = password

    def get_customer_id(self):
        return self.__customer_id

    def get_email(self):
        return self.__email

    def get_date_joined(self):
        return self.__date_joined

    def get_address(self):
        return self.__address

    def get_phone(self):
        return self.__phone

    def get_birth(self):
        return self.__birth

    def get_password(self):
        return self.__password

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_email(self, email):
        self.__email = email

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def set_address(self, address):
        self.__address = address

    def set_phone(self, phone):
        self.__phone = phone

    def set_birth(self, birth):
        self.__birth = birth

    def set_password(self, password):
        self.__password = password
