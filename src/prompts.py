IMAGE_PROMPT = """
<task>
- Classify the type of document in this image into one of the options below.
</task>

<options>
- drivers_license
- bank_statement
- invoice
- unknown
</options>

<rules>
- Return only the option name. Do not include any other text.
</rules>
"""