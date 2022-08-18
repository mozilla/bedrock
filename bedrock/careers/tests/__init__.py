# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

import factory
import pytz

from bedrock.careers.models import Position


class PositionFactory(factory.django.DjangoModelFactory):
    job_id = factory.Faker("pyint")
    internal_job_id = factory.Faker("pyint")
    title = factory.Faker("job")
    department = factory.Faker("random_element", elements=["Data Analytics", "Engineering"])
    location = factory.Faker("random_element", elements=["Mountain View", "San Francisco", "Toronto"])
    description = factory.Faker("sentence")
    source = "gh"
    position_type = factory.Faker("random_element", elements=["Full-Time", "Part-Time", "Contractor", "Intern"])
    updated_at = factory.Faker("date_time", tzinfo=pytz.UTC)

    class Meta:
        model = Position

    @factory.lazy_attribute
    def apply_url(self):
        if self.source == "gh":
            url = f"https://boards.greenhouse.io/{settings.GREENHOUSE_BOARD}/jobs/{self.job_id}"
            return url.format(self.job_id)
