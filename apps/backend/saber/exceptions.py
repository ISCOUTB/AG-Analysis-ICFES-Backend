class DepartmentNotFoundError(Exception):
    def __init__(self, department_id: str) -> None:
        super().__init__(f"""|Department| with the given {
            department_id} doesn't exists""")


class MunicipalityNotFoundError(Exception):
    def __init__(self, municipality_id: str) -> None:
        super().__init__(f"""Municipality with the given {
            municipality_id} does not exists""")


class InstitutionNotFoundError(Exception):
    def __init__(self, institution_id: str) -> None:
        super().__init__(f"""Institution with the given {
            institution_id} does not exists""")
