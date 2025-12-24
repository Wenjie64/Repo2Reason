def generate_code_qa(parsed):
    qas = []
    path = parsed["path"]

    for f in parsed["functions"]:
        qas.append({
            "question": f"What is the purpose of function `{f['name']}`?",
            "answer": f"The function `{f['name']}` implements a specific unit of logic.",
            "context": {
                "code": f["code"],
                "location": path
            },
            "reasoning": (
                "The function name and its implementation indicate its responsibility. "
                "By analyzing the code body, we infer how it processes inputs and affects system behavior."
            )
        })

    for c in parsed["classes"]:
        qas.append({
            "question": f"What is the responsibility of class `{c['name']}`?",
            "answer": f"The class `{c['name']}` encapsulates related behaviors and data.",
            "context": {
                "code": c["code"],
                "location": path
            },
            "reasoning": (
                "The class definition groups methods and attributes. "
                "This structure reveals its architectural role in the system."
            )
        })

    return qas