from flask_admin.contrib.peewee import ModelView

from model import *


class UserAdmin(ModelView):
    pass


class UMKMAdmin(ModelView):
    pass


class CampaignAdmin(ModelView):
    pass


class VerificationAdmin(ModelView):
    pass


class QuestionAnswerAdmin(ModelView):
    pass


class UMKMStatisticAdmin(ModelView):
    pass


class UMKMValidatorAdmin(ModelView):
    pass


ADMIN_VIEWS = [
    UserAdmin(User),
    UMKMAdmin(UMKM),
    CampaignAdmin(Campaign),
    VerificationAdmin(Verification),
    QuestionAnswerAdmin(QuestionAnswer),
    UMKMStatisticAdmin(UMKMStatistic),
    UMKMValidatorAdmin(UMKMValidator)
]
