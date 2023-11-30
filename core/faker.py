from src.administration.admins.models import (
    Client, AbsenseType, ReportType, Position, Department,
)


def main():
    Department.fake()
    Position.fake()
    ReportType.fake(5)
    AbsenseType.fake(5)
    Client.fake(20)


if __name__ == "__main__":
    main()
