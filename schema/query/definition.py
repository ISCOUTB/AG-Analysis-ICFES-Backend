import graphene
from saber.exceptions import DepartmentNotFoundError, MunicipalityNotFoundError, HighschoolNotFoundError, CollegeNotFoundError
import schema.types as types
import saber.models as saber_models
from django.core.exceptions import ObjectDoesNotExist
from typing import Literal


class Query(graphene.ObjectType):
    # -----------------------------------------------------------------------------|>
    # Department
    # -----------------------------------------------------------------------------|>

    departments = graphene.List(types.DepartmentType)
    department = graphene.Field(types.DepartmentType, id=graphene.ID())

    def resolve_departments(self, info):
        return saber_models.Department.objects.all()

    def resolve_department(self, info, id):
        try:
            return saber_models.Department.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise DepartmentNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # Municipality
    # -----------------------------------------------------------------------------|>

    municipalities = graphene.List(types.MunicipalityType)
    municipality = graphene.Field(types.MunicipalityType, id=graphene.ID())

    def resolve_municipalities(self, info):
        return saber_models.Municipality.objects.all()

    def resolve_municipality(self, info, id):
        try:
            return saber_models.Municipality.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise MunicipalityNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # Highschool
    # -----------------------------------------------------------------------------|>

    highschools = graphene.List(types.HighschoolType)
    highschool = graphene.Field(types.HighschoolType, id=graphene.ID())

    def resolve_highschools(self, info):
        return saber_models.Highschool.objects.all()

    def resolve_highschool(self, info, id):
        try:
            return saber_models.Highschool.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise HighschoolNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # College
    # -----------------------------------------------------------------------------|>

    colleges = graphene.List(types.CollegeType)
    college = graphene.Field(types.CollegeType, id=graphene.ID())

    def resolve_colleges(self, info):
        return saber_models.College.objects.all()

    def resolve_college(self, info, id):
        try:
            return saber_models.College.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise CollegeNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # Highschool Student
    # -----------------------------------------------------------------------------|>

    highschool_students = graphene.List(
        types.HighschoolStudentType,
        type=graphene.String(default_value="paginated"),
        period=graphene.String(default_value=None),
        start_period=graphene.String(default_value=None),
        end_period=graphene.String(default_value=None),
        page=graphene.Int(default_value=1),
        page_size=graphene.Int(default_value=1000)
    )

    def resolve_highschool_students(self, info, type: Literal['paginated', 'single_period', 'period_range'],
                                    period: str, start_period: str, end_period: str, page: int = 1, page_size: int = 1000):
        return Query.handler_students(
            qs=saber_models.HighschoolStudent.objects.all(),
            type=type,
            period=period,
            start_period=start_period,
            end_period=end_period,
            page=page,
            page_size=page_size
        )

    # -----------------------------------------------------------------------------|>
    # College Student
    # -----------------------------------------------------------------------------|>

    college_students = graphene.List(
        types.CollegeStudentType,
        type=graphene.String(default_value="paginated"),
        period=graphene.String(default_value=None),
        start_period=graphene.String(default_value=None),
        end_period=graphene.String(default_value=None),
        page=graphene.Int(default_value=1),
        page_size=graphene.Int(default_value=100)
    )

    def resolve_college_student(self, info, type: Literal['paginated', 'single_period', 'period_range'],
                                period: str, start_period: str, end_period: str, page: int = 1, page_size: int = 1000):

        return Query.handler_students(
            qs=saber_models.CollegeStudent.objects.all(),
            type=type,
            period=period,
            start_period=start_period,
            end_period=end_period,
            page=page,
            page_size=page_size
        )

    # -----------------------------------------------------------------------------|>
    # Misc
    # -----------------------------------------------------------------------------|>

    @staticmethod
    def handler_students(qs: list[saber_models.CollegeStudent | saber_models.HighschoolStudent],
                         type: Literal['paginated', 'single_period', 'period_range'], period: str, start_period: str, end_period: str,
                         page: int, page_size: int):
        if type == 'paginated':
            start = (page - 1) * page_size
            end = start + page_size

            return qs[start:end]

        if type == 'single_period':
            if not period:
                raise Exception(':period is required')

            try:
                period_object = saber_models.Period.objects.get(label=period)
                return qs.filter(period=period_object)
            except ObjectDoesNotExist:
                return []

        if type == 'period_range':
            if not start_period or not end_period:
                raise Exception(':start_period, :end_period are required')

            try:
                periods = saber_models.Period.objects.filter(
                    label__gte=start_period,
                    label__lte=end_period
                )

                if not periods.exists():
                    return []

                qs = qs.filter(period__in=periods)
                start = (page - 1) * page_size
                end = start + page_size
                return qs[start:end]
            except:
                return []
        return []
