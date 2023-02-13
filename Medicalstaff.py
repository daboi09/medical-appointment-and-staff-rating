class Medicalstaff:
    count_id = 1

    def __init__(self,name,email,phonenum, venue, date, note):
        self.__medical_id = Medicalstaff.count_id
        self.__name = name
        self.__email = email
        self.__phonenum = phonenum
        self.__venue = venue
        self.__date = date
        self.__note = note

    def get_medical_id(self):
        return self.__medical_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_phonenum(self):
        return self.__phonenum

    def get_venue(self):
        return self.__venue

    def get_date(self):
        return self.__date

    def get_note(self):
        return self.__note

    def set_medical_id(self, medical_id):
        self.__medical_id = medical_id

    def set_email(self,email):
        self.__email = email

    def set_name(self, name):
        self.__name = name

    def set_phonenum(self, phonenum):
        self.__phonenum = phonenum

    def set_venue(self, venue):
        self.__venue = venue

    def set_date(self, date):
        self.__date = date

    def set_note(self, note):
        self.__note = note

