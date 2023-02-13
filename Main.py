class Main:
    count_id = 1

    def __init__(self,name,email,phonenum, type, doctor, venue, time, date):
        self.__main_id = Main.count_id
        self.__name = name
        self.__email = email
        self.__phonenum = phonenum
        self.__type = type
        self.__doctor = doctor
        self.__venue = venue
        self.__time = time
        self.__date = date

    def get_main_id(self):
        return self.__main_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_phonenum(self):
        return self.__phonenum

    def get_type(self):
        return self.__type

    def get_doctor(self):
        return self.__doctor

    def get_venue(self):
        return self.__venue

    def get_time(self):
        return self.__time

    def get_date(self):
        return self.__date

    def set_main_id(self, main_id):
        self.__main_id = main_id

    def set_email(self,email):
        self.__email = email

    def set_name(self, name):
        self.__name = name

    def set_phonenum(self, phonenum):
        self.__phonenum = phonenum

    def set_type(self, type):
        self.__type = type

    def set_doctor(self, doctor):
        self.__doctor = doctor

    def set_venue(self, venue):
        self.__venue = venue

    def set_time(self, time):
        self.__time = time

    def set_date(self, date):
        self.__date = date
