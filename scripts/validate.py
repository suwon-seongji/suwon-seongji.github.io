"""Dependency-free publishing checks. Front matter is JSON (a YAML subset).
This does not replace source verification or semantic editorial review.
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOS = {"htglove/htglove.github.io", "suwon-seongji/suwon-seongji.github.io"}
SUWON = "suwon-seongji/suwon-seongji.github.io"

def parts(text):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match:
        raise ValueError("Missing front matter")
    return match.group(1), text[match.end():]

def norm(text):
    return re.sub(r"[^a-z0-9가-힣]", "", text.lower())

def grams(text, n=5):
    text = norm(text)
    return {text[i:i+n] for i in range(max(0, len(text)-n+1))}

def similarity(a, b):
    x, y = grams(a), grams(b)
    return len(x & y) / max(1, len(x | y))

def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if len(norm(p)) >= 110
            and not p.lstrip().startswith(("#", "|", "<"))]

def title_of(text):
    raw, _ = parts(text)
    try:
        return json.loads(raw).get("title", "")
    except json.JSONDecodeError:
        m = re.search(r"^title:\s*[\"']?(.*?)[\"']?\s*$", raw, re.M)
        return m.group(1) if m else ""

def same_day_conflict(path, references):
    return [p["path"] for p in references if p["repository"] == SUWON
            and p["path"] != path and Path(p["path"]).name[:10] == Path(path).name[:10]]

def check(reference):
    errors, reports = [], []
    if set(r["name"] for r in reference.get("repositories", [])) != REPOS:
        errors.append("Both complete repository inventories are required.")
    references = []
    for repo in reference.get("repositories", []):
        if not re.fullmatch(r"[0-9a-f]{40}", repo.get("head", "")):
            errors.append("Missing current HEAD: " + repo["name"])
        for p in repo.get("posts", []):
            references.append(dict(p, repository=repo["name"]))
    topics = json.loads((ROOT / "editorial/topics.json").read_text(encoding="utf-8"))
    ids = [t["id"] for t in topics]
    if len(set(ids)) != len(ids):
        errors.append("Duplicate topic IDs")
    posts = sorted((ROOT / "_posts").glob("*.md"))
    used_days, used_topics = {}, {}
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).date()
    for file in posts:
        rel = file.relative_to(ROOT).as_posix()
        text = file.read_text(encoding="utf-8")
        try:
            raw, body = parts(text)
            fm = json.loads(raw)
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{rel}: {exc}")
            continue
        for key in ("title","date","last_modified_at","category","topic_id","primary_keyword",
                    "secondary_keyword","keywords","summary","description","faq","sources"):
            if not fm.get(key):
                errors.append(f"{rel}: missing {key}")
        if errors:
            continue
        if fm.get("layout") != "post":
            errors.append(f"{rel}: layout must be post")
        day = file.name[:10]
        try:
            date = dt.date.fromisoformat(str(fm["date"])[:10])
            if str(date) != day or date > today:
                errors.append(f"{rel}: filename/date mismatch or future date")
            if dt.date.fromisoformat(str(fm["last_modified_at"])[:10]) < date:
                errors.append(f"{rel}: modification date predates publication")
        except ValueError:
            errors.append(f"{rel}: invalid date")
        if day in used_days:
            errors.append(f"{rel}: second post on {day}")
        used_days[day] = rel
        if fm["topic_id"] in used_topics:
            errors.append(f"{rel}: reused topic ID")
        used_topics[fm["topic_id"]] = rel
        topic = next((t for t in topics if t["id"] == fm["topic_id"]), None)
        expected_url = f"https://suwon-seongji.github.io/guide/{file.name[11:-3]}/"
        if not topic or topic.get("status") != "published" or topic.get("published_url") != expected_url or topic.get("published_date") != day:
            errors.append(f"{rel}: topic ledger not synchronized")
        if re.search(r"20\d{2}|\d{1,2}\s*월", fm["title"]):
            errors.append(f"{rel}: year/month in title")
        if fm["primary_keyword"] not in fm["title"] or fm["secondary_keyword"] not in fm["title"]:
            errors.append(f"{rel}: keywords missing from title")
        if fm["primary_keyword"] not in fm["summary"] or fm["primary_keyword"] not in body.split("\n\n")[0]:
            errors.append(f"{rel}: keyword missing from opening")
        if len(body) < 1500 or len(re.findall(r"^## ", body, re.M)) < 5:
            errors.append(f"{rel}: insufficient substantive body/sections")
        if not re.search(r"^\|\s*:?-{3,}", body, re.M):
            errors.append(f"{rel}: comparison table missing")
        if not 3 <= len(fm["faq"]) <= 5 or any(not f.get("q") or not f.get("a") for f in fm["faq"]):
            errors.append(f"{rel}: FAQ invalid")
        for source in fm["sources"]:
            if not all(source.get(k) for k in ("title","publisher","url","checked")):
                errors.append(f"{rel}: incomplete source")
            if not re.match(r"^https://", source.get("url","")):
                errors.append(f"{rel}: source must be HTTPS")
            try:
                checked = dt.date.fromisoformat(source["checked"])
                if checked > today or checked < date:
                    errors.append(f"{rel}: source was not checked at publication")
            except (KeyError, ValueError):
                errors.append(f"{rel}: invalid source date")
        if re.search(r"<\s*/?script|\{%|\{\{", text, re.I):
            errors.append(f"{rel}: executable template/script content prohibited")
        if same_day_conflict(rel, references):
            errors.append(f"{rel}: remote post already exists for this day")
        max_para, nearest = 0.0, None
        for old in references:
            if old["repository"] == SUWON and old["path"] == rel:
                continue
            try:
                _, old_body = parts(old["content"])
            except ValueError:
                errors.append("Unparseable reference: " + old["path"])
                continue
            if norm(fm["title"]) == norm(title_of(old["content"])):
                errors.append(f"{rel}: duplicate title with {old['path']}")
            for p in paragraphs(body):
                for q in paragraphs(old_body):
                    score = similarity(p, q)
                    if score > max_para:
                        max_para, nearest = score, old["path"]
                    if score >= 0.72 or (len(norm(p)) >= 140 and norm(p) in norm(q)):
                        errors.append(f"{rel}: similar paragraph with {old['path']} ({score:.2f})")
        reports.append({"post":rel,"characters":len(body),"sections":len(re.findall(r"^## ",body,re.M)),
                        "reference_posts":len(references),"highest_paragraph_similarity":round(max_para,3),"nearest":nearest})
    for t in topics:
        if t["status"] == "published" and t["id"] not in used_topics:
            errors.append("Published topic has no article: " + t["id"])
    return errors, reports

def self_test():
    assert similarity("수원에서 길을 확인한 뒤 방문합니다."*10, "수원에서 길을 확인한 뒤 방문합니다."*10) == 1
    assert similarity("수원역에서 방문 주소와 출구 확인"*10, "도서관 전자책 대출과 회원증 발급"*10) < 0.3
    refs=[{"repository":SUWON,"path":"_posts/2026-11-04-other.md"}]
    assert same_day_conflict("_posts/2026-11-04-new.md",refs)
    assert not same_day_conflict("_posts/2026-11-05-new.md",refs)
    assert not same_day_conflict(refs[0]["path"],refs)
    try:
        parts("# no front matter")
        raise AssertionError("Malformed post accepted")
    except ValueError:
        pass
    print("Regression checks passed: duplicate paragraph, date idempotency, malformed front matter.")

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--reference",type=Path)
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:
        self_test()
    if args.reference:
        errors,reports=check(json.loads(args.reference.read_text(encoding="utf-8")))
        print(json.dumps({"reports":reports,"errors":errors},ensure_ascii=False,indent=2))
        sys.exit(1 if errors else 0)
    elif not args.self_test:
        parser.error("--reference is required; refusing to skip duplicate checks")
