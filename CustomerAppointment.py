import UserAppointment

class Customer(UserAppointment.UserAppointment):
    count_id = 1

    def __init__(self, type, doctor, venue, time, date, email, phonenum, name, status):
        super().__init__(type, doctor, venue, time, date , name, email, phonenum)
        self.__customer_id = Customer.count_id
        self.__status = status

    def get_customer_id(self):
        return self.__customer_id
    def get_status(self):
        return self.__status
    def set_customer_id(self,customer_id):
        self.__customer_id = customer_id
    def set_status(self, status):
        self.__status = status

