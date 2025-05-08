IMAGE_PROMPT = """
You are a document classifier.

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
- Return only the option name. Do not include any other text, quotes, or escape characters.
</rules>

<file filename="{filename}" />
"""

TEXT_PROMPT = """
You are a document classifier.

<task>
- You are reviewing the text of a document.
- Based on the text content, classify the type of document into one of the options below.
</task>

<options>
- drivers_license
- bank_statement
- invoice
- unknown
</options>

<rules>
- Return only the option name. Do not include any other text, quotes, or escape characters.
</rules>

<document_text filename="{filename}">
{text}
</document_text>
"""