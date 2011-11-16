from django.db import models


FEC_FILING_URL = "http://fec.gov/disclosurehs/HSContrbTran.do?format=%(format)s&candId=%(candidate_id)s&electionYr=%(year)s&contCategory=INDIVIDUAL&candOfficeSt=%(state)s&category=state%(chamber)s_all&contComeFrom=candlist&detailComeFrom=candlist"

class Candidate(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)
    party = models.CharField(max_length=50)

    # TODO: can this be made a foreign key?
    incumbent = models.CharField(max_length=20)

    # Precalculated totals from the FEC
    total_receipts = models.IntegerField()
    total_individual = models.IntegerField()
    total_pac = models.IntegerField()
    total_party = models.IntegerField()
    total_candidate = models.IntegerField()

    disbursements = models.IntegerField()
    cash_on_hand = models.IntegerField()
    debt = models.IntegerField()

    date_through = models.DateField()

    committee_calendar_year = models.IntegerField()
    transfers = models.IntegerField()


    def __unicode__(self):
        return self.name


    def filing_url(self, chamber, format="csv", state="TX", year=2012):
        return FEC_FILING_URL % {
            "format": format,
            "candidate_id": self.id,
            "year": year,
            "state": state,
        }


class Contributor(models.Model):
    candidate = models.ForeignKey(Candidate)

    name = models.CharField(max_length=250)
    employer = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    date = models.DateField()
    amount = models.IntegerField()

    # Fields that don't appear to have anything in them
    memo_code = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
