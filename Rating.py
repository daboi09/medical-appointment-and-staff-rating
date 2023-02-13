class Rating:
    count_id = 1

    def __init__(self,doctor, rating, comments):
        self.__rating_id = Rating.count_id
        self.__doctor = doctor
        self.__rating = rating
        self.__comments = comments

    def get_rating_id(self):
        return self.__rating_id

    def get_doctor(self):
        return self.__doctor

    def get_rating(self):
        return self.__rating

    def get_comments(self):
        return self.__comments

    def set_rating_id(self, rating_id):
        self.__rating_id = rating_id

    def set_doctor(self, doctor):
        self.__doctor = doctor

    def set_rating(self,rating):
        self.__rating = rating

    def set_comments(self, comments):
        self.__comments = comments
