from django.db import models


class Character(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, '男'),
        (FEMALE, '女'),
    ]

    ROLE_CHOICES = [
        ('SALE', '带货'),
        ('PERFORMANCE', '才艺'),
        ('KNOWLEDGE', '知识'),
        ('AFFECTION', '情感'),
    ]

    EDUCATION_CHOICES = [
        ('DOCTOR', '博士'),
        ('MASTER', '硕士'),
        ('BACHELOR', '本科'),
        ('JUNIOR_COLLEGE', '大专'),
        ('HIGH_SCHOOL', '高中'),
        ('VOCATIONAL_SCHOOL', '中专'),
        ('OTHER', '其他'),
    ]

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    topic = models.CharField(max_length=100)
    created_datetime = models.DateTimeField(auto_now_add=True, editable=False)
    updated_datetime = models.DateTimeField(auto_now=True, editable=False)
    birth_date = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=30, choices=EDUCATION_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    personality = models.CharField(max_length=30, null=True, blank=True)
    habit = models.CharField(max_length=50, null=True, blank=True)
    hobby = models.CharField(max_length=50, null=True, blank=True)
    advantage = models.CharField(max_length=50, null=True, blank=True)
    speaking_style = models.CharField(max_length=50, null=True, blank=True)
    audience_type = models.CharField(max_length=30, null=True, blank=True)
    world_view = models.TextField(max_length=400, null=True, blank=True)
    personal_statement = models.TextField(max_length=400, null=True, blank=True)

    # @classmethod
    # def from_dict(cls, data: dict, user):
    #     character = cls()
    #     character.copy_from_dict(data)
    #     character.user = user
    #     return character

    # def copy_from_dict(self, data: dict):
    #     self.name = data.get('name')
    #     self.gender = data.get('gender')
    #     self.role = data.get('role')
    #     self.topic = data.get('topic')
    #     self.birth_date = date.fromisoformat(data.get('birthDate'))
    #     self.education = data.get('education')
    #     self.marital_status = data.get('maritalStatus')
    #     self.personality = data.get('personality')
    #     self.habit = data.get('habit')
    #     self.hobby = data.get('hobby')
    #     self.advantage = data.get('advantage')
    #     self.speaking_style = data.get('speakingStyle')
    #     self.audience_type = data.get('audienceType')
    #     self.world_view = data.get('worldView')
    #     self.personal_statement = data.get('personalStatement')

    # def to_dict(self) -> dict:
    #     return {
    #         'id': self.pk,
    #         'name': self.name,
    #         'gender': self.gender,
    #         'role': self.role, 
    #         'topic': self.topic,
    #         'birthDate': self.birth_date,
    #         'education': self.education,
    #         'maritalStatus': self.marital_status,
    #         'personality': self.personality,
    #         'habit': self.habit,
    #         'hobby': self.hobby,
    #         'advantage': self.advantage,
    #         'speakingStyle': self.speaking_style,
    #         'audienceType': self.audience_type,
    #         'worldView': self.world_view,
    #         'personalStatement': self.personal_statement,
    #     }

