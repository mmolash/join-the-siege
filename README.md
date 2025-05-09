# File Classifier

## Overview & Approach
I focused on improving the classifier in a few ways:
1. Incorporating an LLM to make classifications based on document context instead of file name
2. Supporting additional file types (.txt and .docx)
3. Adding an industry-based config to simplify scalability to new industries

## Implementation Flow
- The server receives classification request with a file and industry
- Server pre-processes the file
    - If the file is an image (jpg, png), it is converted to base64
    - If the file is a document (pdf, docx, txt), its text is extracted
- Server dynically generates a prompt based on the industry config (defined in `config/categories.yaml`) which specifies acceptable categories for the specified industry.
- Server sends a request to another service (ollama) which provides access to a locally running LLM (in this case, LLaVA, which supports multimodal data) with the prompt and processed file.
- Server checks for a valid response (one of the industry's options) and retries once if not valid
- Server returns response

## Future Enchancements & Other Ideas Considered
- Set up an evaluation suite for LLM performance that can test effectiveness across models and over time
    - Add more test files + expected result for each supported industry 
- Prepare service for production deployment
    - Set up a Dockerfile for containerizing the Flask server
    - Add Kubernetes manifests for production deployment (using official ollama container)
- Add CI (lint, test, and build) using GitHub Actions
- Remove dependency on ollama to enable use of frontier (close source) models
- Add simple UI for hitting classification service and/or monitoring past classifications

## Setup
1. **Install python dependencies**
   ```shell
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Install and run ollama** (for Mac):
   ```shell
   brew install ollama
   brew services start ollama
   ```
3. **Pull the LLaVA model** (with ollama running):
   ```shell
   ollama pull llava:7b
   ```
4. **Create .env file** with ollama URL (based on `.env.example`)

## Configuration
To add or modify industries and their accepted categories, edit `config/categories.yaml`:

```yaml
finance:
  - drivers_license
  - bank_statement
  - invoice
  - unknown

<industry name (as it should be included in classify_file request)>:
  - <classification option>
  - ...

...
```

Note: industries and categories are loaded at runtime (currently on each request), so they can be updated dynamically without restarting the server.

## Testing
Run tests with
```shell
pytest
```

## Usage
Run the Flask app:
```shell
python -m src.app
```

Send a POST request to `/classify_file` with a file and industry name:
```sh
curl -X POST -F 'file=@path_to_file.pdf' -F 'industry=finance' http://127.0.0.1:5000/classify_file
```
Note: the default supported industries are `finance` and `legal`
