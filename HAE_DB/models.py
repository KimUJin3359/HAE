from django.db import models
from django.db.models import Count
import bcrypt
import jwt
import os

#JWT_SECRET_KEY = 'This is a private key(not public)'
algorithm = 'HS256'

class judge(models.Model):
    image = models.ImageField(upload_to="test", null=True)

    @classmethod
    def create(cls, image):
        new_Judge = cls(image=image)
        new_Judge.save()

        return new_Judge

    @classmethod
    def remove(cls):
        judge.objects.all().delete()

        return 1

class crew(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False)
    des = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to="images", null=True)

    @property
    def image_converter(self):
        if (self.image==""):
            return ''
        else:
            return self.image

    @image_converter.setter
    def image_converter_setter(self, value):
        self.image=value


    @classmethod
    def create(cls, name, des, image):
        new_Crew = cls(name=name, des=des, image=image)
        new_Crew.save()

        return new_Crew

    @classmethod
    def remove(cls,crew_ID):
        try:
            delete_Crew = crew.objects.get(ID=crew_ID)
            delete_Crew.delete()

            return 1

        except feed.DoesNotExist:

            return 0


class user(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    image = models.ImageField(upload_to="images", null=True)
    crew_ID = models.ForeignKey(crew, default=1, on_delete=models.SET_DEFAULT)

    @property
    def image_converter(self):
        if (self.image==""):
            return ''
        else:
            return self.image

    @image_converter.setter
    def image_converter_setter(self, value):
        self.image=value

    @classmethod
    def create(cls, name, crew_ID, image):
        new_User = cls(name=name, image=image, crew_ID=crew_ID)
        new_User.save()

        return new_User

    @classmethod
    def update_crew(cls, user_ID, crew_ID):
        change_User = user.objects.get(ID=user_ID)
        change_User.crew_ID = crew_ID
        change_User.save()

        return change_User

    @classmethod
    def update_crew_reset(cls, crew_ID):
        change_User = user.objects.filter(crew_ID=crew_ID)
        for i in change_User :
            i.crew_ID = crew.objects.get(ID=1)
            i.save()

        return 1

    @classmethod
    def update_profile(cls, ID, name, image):
        try:
            change_User = user.objects.get(ID=ID)
            change_User.name=name
            change_User.image=image
            change_User.save()

            return 1

        except user.DoesNotExist:

            return 0

class account(models.Model):
    ID = models.ForeignKey(user, on_delete=models.CASCADE)
    user_ID = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30, null=False)

    @classmethod
    def create(cls, ID, user_ID, password):
        new_Acc = cls(ID=ID, user_ID=user_ID, password=password)
        new_Acc.save()

        return new_Acc

class crew_header(models.Model):
    crew_ID = models.ForeignKey(crew, on_delete=models.CASCADE)
    user_ID = models.ForeignKey(user, on_delete=models.CASCADE)

    @classmethod
    def create(cls, crew_ID, user_ID):
        new_Header = cls(crew_ID=crew_ID, user_ID=user_ID)
        new_Header.save()

        return new_Header

class feed(models.Model):
    ID = models.AutoField(primary_key=True)
    des = models.CharField(max_length=50, null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    created_at = models.DateTimeField(null=False)
    image = models.ImageField(upload_to="images", null=True)
    #user가 아이디를 삭제하면 그와 관련된 피드 모두 삭제 예정
    user_ID = models.ForeignKey(user, on_delete=models.CASCADE)

    @property
    def image_converter(self):
        if (self.image==""):
            return ''
        else:
            return self.image

    @image_converter.setter
    def image_converter_setter(self, value):
        self.image=value

    @classmethod
    def create(cls, des, start_time, end_time, created_at, user_ID, image):
        new_Feed = cls(des=des, start_time=start_time, end_time=end_time,
                       created_at=created_at, user_ID=user_ID, image=image)
        new_Feed.save()

        return new_Feed


    @classmethod
    def update(cls, ID, des, start_time, end_time, image):
        #해당 ID의 feed update
        try:
            change_Feed = feed.objects.get(ID=ID)
            change_Feed.des = des
            change_Feed.start_time = start_time
            change_Feed.end_time = end_time
            change_Feed.image = image
            change_Feed.save()

            return 1
         #해당 ID가 없을때
        except feed.DoesNotExist:

            return 0

    @classmethod
    def remove(cls, ID):
        try:
            delete_Feed = feed.objects.get(ID=ID)
            delete_Feed.delete()

            return 1
        #해당 ID가 없을 때
        except feed.DoesNotExist:

            return 0

class feed_comment(models.Model):
    ID = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(null=False)
    #댓글을 단 feed가 삭제되면 그와 관련된 정보 삭제
    feed_ID = models.ForeignKey(feed, on_delete=models.CASCADE)
    user_ID = models.ForeignKey(user, on_delete=models.CASCADE)

    @classmethod
    def create(cls, comment, created_at, feed_ID, user_ID):
        new_FeedComment = cls(comment=comment, created_at=created_at, feed_ID=feed_ID, user_ID=user_ID)
        new_FeedComment.save()

        return 1

    @classmethod
    def update(cls, ID, comment):
        #해당 ID의 feed update
        try:
            change_FeedComment = feed_comment.objects.get(ID=ID)
            change_FeedComment.comment = comment
            change_FeedComment.save()

            return 1
         #해당 ID가 없을때
        except feed_comment.DoesNotExist:

            return 0

    @classmethod
    def remove(cls, ID):
        try:
            delete_FeedComment = feed_comment.objects.get(ID=ID)
            delete_FeedComment.delete()

            return 1
        #해당 ID가 없을 때
        except feed_comment.DoesNotExist:

            return 0

class gathering(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    created_at = models.DateTimeField(null=False)
    date = models.DateTimeField(null=False)
    #크루가 삭제되면 크루와 관련된 모임들 삭제 예정
    crew_ID = models.ForeignKey(crew, on_delete=models.CASCADE)
    user_ID = models.ForeignKey(user, on_delete=models.CASCADE)

    @classmethod
    def create(cls, name, created_at, date, crew_ID, user_ID):
        new_Gathering = cls(name=name, created_at=created_at, date=date, crew_ID=crew_ID, user_ID=user_ID)
        new_Gathering.save()

        return 1

    @classmethod
    def remove(cls, user_ID, gathering_ID):
        try:
            delete_Gathering = gathering.objects.get(ID=gathering_ID)
            if(delete_Gathering.user_ID==user_ID):
                delete_Gathering.delete()
                return 1

            else:
                return 0

        #해당 ID가 없을 때
        except gathering.DoesNotExist:

            return -1

class gathering_comment(models.Model):
    ID = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(null=False)
    gathering_ID = models.ForeignKey(gathering, on_delete=models.CASCADE)
    user_ID = models.ForeignKey(user, on_delete=models.CASCADE)

    @classmethod
    def create(cls, comment, created_at, gathering_ID, user_ID):
        new_Comment = cls(comment=comment, created_at=created_at,
                       gathering_ID=gathering_ID, user_ID=user_ID)
        new_Comment.save()

        return 1

    @classmethod
    def update(cls, ID, comment):
        #해당 ID의 feed update
        try:
            change_GatheringComment = gathering_comment.objects.get(ID=ID)
            change_GatheringComment.comment = comment
            change_GatheringComment.save()

            return 'success'
         #해당 ID가 없을때
        except gathering_comment.DoesNotExist:

            return 'fail'

    @classmethod
    def remove(cls, ID):
        try:
            delete_GatheringComment = gathering_comment.objects.get(ID=ID)
            delete_GatheringComment.delete()

            return 'success'
        #해당 ID가 없을 때
        except gathering_comment.DoesNotExist:

            return 'fail'

class gathering_participant(models.Model):
    #user가 모임 참가 취소를 하면, 그와 관련된 데이터 삭제
    user_ID = models.ForeignKey(user, on_delete=models.CASCADE)
    #gathering이 취소되면 그와 관련된 데이터 삭제
    gathering_ID = models.ForeignKey(gathering, on_delete=models.CASCADE)

    @classmethod
    def create(cls, user_ID, gathering_ID):
        new_Par = cls(user_ID=user_ID, gathering_ID=gathering_ID)
        new_Par.save()

        return new_Par

    @classmethod
    def remove(cls, user_ID, gathering_ID):
        try:
            delete_GatheringP = gathering_participant.objects.filter(user_ID=user_ID)
            for i in delete_GatheringP:
                if(i.gathering_ID == gathering_ID):
                    i.delete()
                    return 'success'

        #해당 ID가 없을 때
        except gathering_participant.DoesNotExist:

            return 'fail'

class equipment(models.Model):
    ID = models.AutoField(primary_key=True)
    category = models.IntegerField(null=False)
    location_X = models.FloatField(null=False)
    location_Y = models.FloatField(null=False)
    image = models.ImageField(upload_to="images", null=True)
    user_ID = models.ForeignKey(user, on_delete=models.CASCADE)

    @property
    def image_converter(self):
        if (self.image==""):
            return ''
        else:
            return self.image

    @image_converter.setter
    def image_converter_setter(self, value):
        self.image=value

    @classmethod
    def remove(cls, ID):
        try:
            delete_Equipment = equipment.objects.get(ID=ID)
            delete_Equipment.delete()

            return 1
        # 해당 ID가 없을 때
        except equipment.DoesNotExist:

            return 0

    @classmethod
    def create(cls, category, location_X, location_Y, user_ID, image):
        #해당 ID가 없으면 create
        new_Equipment = cls(category=category, location_X=location_X, location_Y=location_Y,
                            image=image, user_ID=user_ID)
        new_Equipment.save()

        return new_Equipment

