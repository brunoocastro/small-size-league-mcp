# Small Size League MCP

A comprehensive toolset designed to help developers understand and work with RoboCup Small Size League rules, software, and team information. This project provides tools for processing, storing, and querying league documentation and resources.

## Features

- Automated website source management
- Document processing and text extraction
- Vector-based document storage and retrieval
- Query interface for league information
- Regular updates from official sources

## Setup

This project uses UV for Python package management. Follow these steps to set up the project:

1. Install UV (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone https://github.com/brunoocastro/small-size-league-mcp.git
cd small-size-league-mcp
```

3. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate  # On Windows
```

4. Install dependencies:
```bash
uv sync
```

## Available Commands

The project provides several commands through `main.py`:

### Update Website Sources
```bash
python main.py update-sources [--sitemap-url URL] [--output FILE]
```
Updates the list of website sources from the sitemap. By default, it uses the official Small Size League sitemap.

### Update Documents
```bash
python main.py update-documents [--sources FILE]
```
Processes the website sources and extracts document content. The default sources file is `processed_urls.txt`.

### Update Database
```bash
python main.py update-database --documents DOC1 [DOC2 ...]
```
Updates the vector database with processed documents.

### Test Vector Store
```bash
python main.py test-vector-store [--query "Your query"]
```
Tests the vector store with a sample query. Default query is "How to submit a paper?"

### Run All Updates
```bash
python main.py run-all [--query "Your query"]
```
Executes all update commands in sequence and tests the vector store with the provided query.

## Project Structure

- `main.py`: Main command-line interface
- `config.py`: Configuration settings
- `db_management.py`: Database management utilities
- `text_handler.py`: Text processing utilities
- `website_sources.py`: Website source management
- `providers.py`: LLM provider configurations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms specified in the LICENSE file.
