import requests
import os
from dotenv import load_dotenv

load_dotenv()

class BlogPublisher:
    def __init__(self):
        self.wp_url = os.getenv("WORDPRESS_URL")
        self.wp_user = os.getenv("WORDPRESS_USER")
        self.wp_password = os.getenv("WORDPRESS_PASSWORD")
        self.medium_token = os.getenv("MEDIUM_TOKEN")

    async def publish_to_wordpress(self, title: str, content: str):
        if not all([self.wp_url, self.wp_user, self.wp_password]):
            return {"status": "skipped", "reason": "No WordPress credentials found"}
        
        # WordPress REST API endpoint
        url = f"{self.wp_url.rstrip('/')}/wp-json/wp/v2/posts"
        
        # Basic auth is often used for demos (with Application Passwords)
        try:
            response = requests.post(
                url,
                auth=(self.wp_user, self.wp_password),
                json={
                    "title": title,
                    "content": content,
                    "status": "publish"
                }
            )
            response.raise_for_status()
            return {"status": "success", "url": response.json().get("link")}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def publish_to_medium(self, title: str, content: str):
        if not self.medium_token:
            return {"status": "skipped", "reason": "No Medium token found"}
            
        # Medium API
        # First get author id
        headers = {"Authorization": f"Bearer {self.medium_token}"}
        try:
            author_res = requests.get("https://api.medium.com/v1/me", headers=headers)
            author_id = author_res.json()["data"]["id"]
            
            post_url = f"https://api.medium.com/v1/users/{author_id}/posts"
            post_res = requests.post(
                post_url,
                headers=headers,
                json={
                    "title": title,
                    "content": content,
                    "contentFormat": "markdown",
                    "publishStatus": "draft"
                }
            )
            post_res.raise_for_status()
            return {"status": "success", "url": post_res.json()["data"]["url"]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

publisher = BlogPublisher()
