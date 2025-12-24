def build_design_prompt(summary, key_files, requirement):
    prompt = f"""
You are a senior backend architect.

You are analyzing a real Django REST Framework repository.
You MUST ground your design strictly in the provided code evidence.
Do NOT invent modules or layers that are not implied by the repository.

=== Framework ===
{summary['framework']}

=== Existing Layers ===
{', '.join(summary['layers'])}

=== Existing Modules ===
{', '.join(summary['modules'].keys())}

=== Key Code Evidence ===
"""

    for f in key_files:
        prompt += f"\n--- File: {f['path']} ---\n"
        for item in f["snippet"]:
            prompt += item["code"] + "\n\n"

    prompt += f"""
=== User Requirement ===
{requirement}

=== Task ===
1. Describe the current system architecture based on the code
2. Identify responsibilities of existing modules
3. Propose an improved design satisfying the requirement
4. Explain how existing code will be reused or extended
5. Describe API and data flow
6. Discuss scalability and maintainability

Use clear section headers.
All reasoning must be grounded in the given repository.
"""

    return prompt