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
	return day, month, year


def to_date(value, spliter):
	day, month, year = spliter(value)
	return datetime.Date(day=day, month=month, year=year)


def row_to_fields(row):
	return {
		"id": row[0],
		"name": row[1].title(),
		"party": rows[2].title(),
		"incumbent": rows[3],
		"total_receipts": to_int(rows[4]),
		"total_individual": to_int(rows[5]),
		"total_pac": to_int(rows[6]),
		"total_party": to_int(rows[7]),
		"total_candidate": to_int(rows[8]),
		"disbursements": to_int(rows[9]),
		"cash_on_hand": to_int(rows[10]),
		"debt": to_int(rows[11]),
		"date_through": to_date(rows[12], candidate_dates),
	}


def row_to_contributor(row):
	return {
		"name": row[0].title(),
		"employer": row[1].title(),
		"city": row[2].title(),
		"state": row[3],
		"zipcode": row[4],
		"date": to_date(row[5], contrib_dates),
		"amount": to_int(row[6]),
	}

class Command(NoArgsCommand):
	def handle(self, **options):
		http = httplib2.Http()
		c = csv(open("./resources/senate.csv"))
		data, legend = [], None
		for row in c:
			if not legend:
				legend = row
				continue

			candidate = Candidate.objects.create(**row_to_fields(row))
			print "Loaded %s" % candidate

			response, body = http.request(candidate.filing_url("senate"))
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