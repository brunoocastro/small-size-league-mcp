test_client:
	uv run mcp_client_tester.py

server:
	uv run mcp_server.py

dev:
	uv run mcp dev mcp_server.py
