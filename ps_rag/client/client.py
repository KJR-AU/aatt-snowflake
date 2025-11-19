import requests

class PracticeStatementRagClient:

    def __init__(self, endpoint_root: str):
        self.endpoint_root: str = endpoint_root
        self.invoke_endpoint: str = f"{endpoint_root}/query"
    
    def invoke(self, query: str):
        response = self.send_post_request(self.invoke_endpoint, { "query": query })
        if not (answer := response.get("answer")):
            raise ValueError()
        return answer

    @staticmethod
    def send_post_request(url: str, payload: dict, headers: dict | None = None, timeout: int = 10) -> dict[str, str]:
        """
        Send a POST request and parse the response.

        Args:
            url (str): The endpoint URL to send the POST request to.
            payload (dict): The request body (will be sent as JSON).
            headers (dict, optional): Additional request headers.
            timeout (int, optional): Timeout in seconds. Defaults to 10.

        Returns:
            dict | str: Parsed JSON response if available, otherwise raw text.

        Raises:
            requests.RequestException: For network-related issues.
            ValueError: If the response cannot be parsed as JSON.
        """
        try:
            # Default headers
            headers = headers or {"Content-Type": "application/json"}

            # Send POST request
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)

            # Raise an error for bad status codes (4xx, 5xx)
            response.raise_for_status()

            # Try to parse as JSON
            try:
                return response.json()
            except ValueError:
                # Fallback to raw text if not JSON
                return response.text

        except requests.RequestException as e:
            print(f"❌ Request failed: {e}")
            raise
