from django.urls import reverse

from bedrock.careers.tests import PositionFactory
from bedrock.mozorg.tests import TestCase


class PositionTests(TestCase):
    """Tests static pages for careers"""

    def test_position_case_sensitive_match(self):
        """
        Validate that a position match is returned from a case-sensitive job id and it doesn't
        raise a multiple records error.
        """
        job_id_1 = "oflWVfwb"
        job_id_2 = "oFlWVfwB"
        PositionFactory.create(job_id=job_id_1)
        PositionFactory.create(job_id=job_id_2)

        url = reverse("careers.position", kwargs={"job_id": job_id_1, "source": "gh"})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["position"].job_id, job_id_1)

        url = reverse("careers.position", kwargs={"job_id": job_id_2, "source": "gh"})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["position"].job_id, job_id_2)
