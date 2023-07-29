"""
A script to automate downloading CircleCI artifacts.

Usage: python3 pull_circleci_artifacts.py <TOKEN> <PIPELINE_ID> <SAVE_DIR>
    TOKEN: 
        CircleCI "personal access token" of a github (preferably machine) user.
        This is secret!

    PIPELINE_ID:
        A unique string id that represents the CircleCI pipeline, whose artifacts this
        script pulls.
        This pipeline must have exactly one workflow and that workflow must have exactly
        one job. This script waits for the pipeline to finish, and pulls artifacts from
        this job. If the pipeline isn't successful on finish, this script exits with an
        error.

    SAVE_DIR:
        The downloaded artifacts are saved to this directory

CircleCI API docs: https://circleci.com/docs/api/v2/index.html (useful for understanding
this code)
"""

# yup, all these are stdlib modules incase you are wondering
import concurrent.futures
import http.client
import json
import sys
import time
from pathlib import Path
from urllib import request

_, token, pipeline_id, save_dir = sys.argv

headers = {"Circle-Token": token}
save_dir = Path(save_dir)

print(
    f"Starting for {pipeline_id = } (and {save_dir = }), now establishing connection..."
)

cci_api = http.client.HTTPSConnection("circleci.com")


def paginate_get_items_and_next(url, next_page=""):
    """
    Helper to get "items" and "next_page_token" from CircleCI API, used to handle
    pagination.
    """

    # page-token is used for pagination. Initially, it is unspecified.
    url_query = f"{url}?page-token={next_page}" if next_page else url
    cci_api.request("GET", f"/api/v2/{url_query}", headers=headers)
    response = cci_api.getresponse()
    if response.status != 200:
        raise RuntimeError(
            f"Request to '{url}' not successful: {response.status} ({response.reason})"
        )

    response_dict = json.loads(response.read())
    if "message" in response_dict:
        raise RuntimeError(
            f"Request to '{url}' failed with message - {response_dict['message']}"
        )

    return response_dict["items"], response_dict["next_page_token"]


def paginate_get_single_item(url):
    """
    Helper to get exactly one item from CircleCI paginated APIs
    """
    items, _ = paginate_get_items_and_next(url)
    if len(items) != 1:
        raise RuntimeError(f"Expected one item, got {len(items)}")

    return items[0]


def paginate_get_all_items(url):
    """
    Helper to get all "items" from CircleCI paginated APIs
    """
    prev_page_tag = ""
    while True:
        items, prev_page_tag = paginate_get_items_and_next(url, prev_page_tag)
        if not items:
            # all artifacts are probably downloaded at this point
            break

        yield from items
        if not prev_page_tag:
            # done with pagination, exit
            break


def download_artifact(artifact):
    """
    Helper to download an artifact given an "artifact dict". This can be concurrently
    called in multiple threads to speed up downloads.
    """
    path = Path(artifact["path"])
    save_path = save_dir / path.name
    print(f"Downloading {path.name}")
    request.urlretrieve(artifact["url"], save_path)
    print(f"Done with saving {path.name}")


cnt = 1
while True:
    print(f"\nAttempt {cnt}")
    workflow = paginate_get_single_item(f"/pipeline/{pipeline_id}/workflow")
    if workflow["status"] != "running":
        if workflow["status"] != "success":
            # workflow failed
            raise RuntimeError(f"The workflow has status '{workflow['status']}'")

        # successfully finished workflow at this point
        job = paginate_get_single_item(f"/workflow/{workflow['id']}/job")

        # shouldn't really happen, but test anyways
        if job["status"] != "success":
            raise RuntimeError(f"The job has status '{workflow['status']}'")

        print(f"Downloading artifacts (they will all be saved in {str(save_dir)})")
        with concurrent.futures.ThreadPoolExecutor() as pool:
            pool.map(
                download_artifact,
                paginate_get_all_items(
                    f"/project/{job['project_slug']}/{job['job_number']}/artifacts"
                ),
            )

        break

    cnt += 1
    print("Job is still running (now sleeping for 30s before retrying)")
    time.sleep(30)
