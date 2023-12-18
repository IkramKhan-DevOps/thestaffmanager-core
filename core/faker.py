from src.administration.admins.models import (
    Client, AbsenseType, ReportType, Position, Department, Employee, Site
)


def main():
    # Department.fake()
    # Position.fake()
    # ReportType.fake(5)
    # AbsenseType.fake(5)
    # Client.fake(20)
    # Site.fake(10)
    Employee.fake_employees(10)
    # pass


if __name__ == "__main__":
    main()
