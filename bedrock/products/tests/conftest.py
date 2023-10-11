from django.utils.dateparse import parse_date, parse_datetime

import pytest

from bedrock.products.models import Breach


@pytest.fixture
def breach(db):
    return Breach.objects.create(
        name="Twitter",
        title="Twitter",
        domain="twitter.com",
        breach_date=parse_date("2022-01-01"),
        added_date=parse_datetime("2022-08-01T01:23:45Z"),
        modified_date=parse_datetime("2022-08-01T01:23:45Z"),
        pwn_count=6682453,
        logo_path="/path/to/twitter.com.ico",
        data_classes=["Bios", "Email addresses", "Geographic locations", "Names", "Phone numbers", "Profile photos", "Usernames"],
        is_verified=True,
        is_fabricated=False,
        is_sensitive=False,
        is_retired=False,
        is_spam_list=False,
        is_malware=False,
    )
