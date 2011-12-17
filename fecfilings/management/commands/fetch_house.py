import csv
import datetime
import httplib2
import sys

from django.core.management.base import NoArgsCommand

from fecfilings.models import Candidate
from fecfilings.models import Contributor


def to_int(value):
    return int(value.replace("$", ""))


def candidate_dates(value):
    return value.split("/")


def contrib_dates(value):
    year, month, day = value.split("-")
    return month, day, year


def to_date(value, spliter):
    month, day, year = spliter(value)
    return datetime.date(day=int(day), month=int(month), year=int(year))


def row_to_fields(row):
    if to_int(row[4]) is 0:
        return False
    return {
        "id": row[0],
        "name": row[1].title(),
        "party": row[2].title(),
        "incumbent": row[3],
        "total_receipts": to_int(row[4]),
        "total_individual": to_int(row[5]),
        "total_pac": to_int(row[6]),
        "total_party": to_int(row[7]),
        "total_candidate": to_int(row[8]),
        "disbursements": to_int(row[9]),
        "cash_on_hand": to_int(row[10]),
        "debt": to_int(row[11]),
        "date_through": to_date(row[12], candidate_dates),
        "committee_calendar_year": to_int(row[13]),
        "transfers": to_int(row[14]),
    }


def row_to_contributor(row):
    def empty(list, key):
        try:
            return row[key]
        except IndexError:
            return ""

    return {
        "name": row[0].title(),
        "employer": row[1].title(),
        "city": row[2].title(),
        "state": row[3],
        "zipcode": row[4],
        "date": to_date(row[5], contrib_dates),
        "amount": to_int(row[6]),
        "memo_code": empty(row, 7),
        "description": empty(row, 8),
    }

class Command(NoArgsCommand):
    def handle(self, **options):
        http = httplib2.Http()
        c = csv.reader(open("./resources/house.csv").read().strip().split("\n")[1:])
        for row in c:
            sys.stdout.write("Creating candidate... ")
            sys.stdout.flush()
            data = row_to_fields(row)
            if data is False:
                print "Unable to load %s" % (row[1].title())
                continue
            candidate = Candidate.objects.create(**data)
            print "DONE!"
            print "Loaded %s" % candidate

            response, body = http.request(candidate.filing_url("house"))
            if response["status"] != "200":
                print "ERROR!"
                print response
                continue

            actual_csv = body.strip().split("\n")[1:]
            if actual_csv:
                for a in csv.reader(actual_csv):
                    Contributor.objects.create(candidate=candidate, **row_to_contributor(a))
                    sys.stdout.write(".")
                    sys.stdout.flush()
            print "\n-" * 80