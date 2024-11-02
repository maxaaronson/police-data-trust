import pytest
import math
from backend.database import Agency


mock_officers = {
    "severe": {
        "first_name": "Bad",
        "last_name": "Cop",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "M",
        "known_employers": []
    },
    "light": {
        "first_name": "Decent",
        "last_name": "Cop",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "M",
        "known_employers": []
    },
    "none": {
        "first_name": "Good",
        "last_name": "Cop",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "M",
        "known_employers": []
    },
}

mock_agencies = {
    "cpd": {
        "name": "Chicago Police Department",
        "website_url": "https://www.chicagopolice.org/",
        "hq_address": "3510 S Michigan Ave",
        "hq_city": "Chicago",
        "hq_zip": "60653",
        "jurisdiction": "MUNICIPAL"
    },
    "nypd": {
        "name": "New York Police Department",
        "website_url": "https://www1.nyc.gov/site/nypd/index.page",
        "hq_address": "1 Police Plaza",
        "hq_city": "New York",
        "hq_zip": "10038",
        "jurisdiction": "MUNICIPAL"
    }
}

new_agency = {
    "name": "New Agency",
    "website_url": "https://www.newagency.com/",
    "hq_address": "123 Main St",
    "hq_city": "New York",
    "hq_zip": "10001",
    "jurisdiction": "MUNICIPAL"
}


@pytest.fixture
def example_agencies(db_session):
    agencies = {}

    for name, mock in mock_agencies.items():
        a = Agency(**mock).save()
        agencies[name] = a
    return agencies


def test_create_agency(db_session, client, contributor_access_token):
    test_agency = new_agency

    res = client.post(
        "/api/v1/agencies/",
        json=test_agency,
        headers={"Authorization": "Bearer {0}".format(
            contributor_access_token)},
    )
    assert res.status_code == 200

    agency_obj = Agency.nodes.get(uid=res.json["uid"])

    assert agency_obj.name == test_agency["name"]
    assert agency_obj.website_url == test_agency["website_url"]
    assert agency_obj.hq_address == test_agency["hq_address"]
    assert agency_obj.hq_city == test_agency["hq_city"]
    assert agency_obj.hq_zip == test_agency["hq_zip"]
    assert agency_obj.jurisdiction == test_agency["jurisdiction"]


def test_unauthorized_create_agency(client, access_token):
    test_agency = mock_agencies["nypd"]

    res = client.post(
        "/api/v1/agencies/",
        json=test_agency,
        headers={"Authorization": "Bearer {0}".format(
            access_token)},
     )
    assert res.status_code == 403


def test_get_agency(client, access_token, example_agency):
    # Test that we can get example_agency
    res = client.get(
        f"/api/v1/agencies/{example_agency.uid}",
        headers={"Authorization": "Bearer {0}".format(access_token)})
    assert res.status_code == 200
    assert res.json["name"] == example_agency.name
    assert res.json["website_url"] == example_agency.website_url


def test_get_all_agencies(client, access_token, example_agencies):
    # Create agencies in the database
    total_agencies = Agency.nodes.all().__len__()

    # Test that we can get agencies
    res = client.get(
        "/api/v1/agencies/",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json["results"].__len__() == total_agencies


def test_agency_pagination(client, example_agencies, access_token):
    per_page = 1
    total_agencies = Agency.nodes.all().__len__()
    expected_total_pages = math.ceil(total_agencies//per_page)
    for page in range(1, expected_total_pages + 1):
        res = client.get(
            f"/api/v1/agencies/?per_page={per_page}&page={page}",
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )

        assert res.status_code == 200
        assert res.json["page"] == page
        assert res.json["total"] == expected_total_pages

        incidents = res.json["results"]
        assert len(incidents) == per_page

    res = client.get(
        (
            f"/api/v1/agencies/?per_page={per_page}"
            f"&page={expected_total_pages + 1}"
        ),
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404
