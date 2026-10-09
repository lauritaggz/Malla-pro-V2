import re


def career_key_from_url(url: str) -> str:
    """Python port of getCareerId() (frontend/src/utils/storageKeys.js) for a legacy malla URL.

    The frontend keys every user's saved progress on this value, so it must never diverge.
    """
    url = url.strip()
    uni_match = re.search(r"/mallas/([^/]+)/", url, flags=re.IGNORECASE)
    uni = (uni_match.group(1) if uni_match else "unab").lower()
    file = re.sub(r"\.json$", "", re.sub(r"^.*/", "", url), flags=re.IGNORECASE).lower()
    return re.sub(r"[^a-z0-9]+", "-", f"{uni}-{file}").strip("-")


def career_key_for_new_program(university_slug: str, program_slug: str) -> str:
    return f"{university_slug}-{program_slug}"
