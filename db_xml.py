import xml.etree.ElementTree as ET
import random

XML_FILE = "questions.xml"

def get_all_questions():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    questions = []

    for q in root.findall("question"):
        questions.append({
            "id": q.get("id"),
            "category": q.find("category").text,
            "subcategory": q.find("subcategory").text,
            "question_text": q.find("question_text").text,
            "image_path": q.find("image_path").text,
            "active": q.find("active").text
        })

    return questions


def get_active_questions(category=None, subcategory=None):
    data = get_all_questions()

    filtered = []

    for q in data:
        if q["active"] != "1":
            continue

        if category and q["category"] != category:
            continue

        if subcategory and q["subcategory"] != subcategory:
            continue

        filtered.append(q)

    random.shuffle(filtered)

    return filtered