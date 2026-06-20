import os
import random
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

# Built-in SEO keyword database for common product categories
KEYWORD_DATABASE = {
    "headphones": ["best wireless headphones 2024", "noise canceling headphones review", "premium audio gear", "bluetooth headphones deal"],
    "phone": ["best smartphone deals", "flagship phone review", "mobile phone comparison", "unlocked phone deal"],
    "laptop": ["best gaming laptop", "laptop review 2024", "affordable gaming laptop", "high performance laptop"],
    "watch": ["best smartwatch", "fitness tracker review", "wearable technology", "smart watch deals"],
    "camera": ["best action camera", "4K camera review", "vlogging camera guide", "waterproof camera deal"],
    "drone": ["best drone for beginners", "4K drone review", "aerial photography drone", "fly more combo deal"],
    "tv": ["best OLED TV", "smart TV review 2024", "4K television deal", "home entertainment setup"],
    "vacuum": ["best cordless vacuum", "robot vacuum review", "home cleaning gadgets", "smart vacuum deal"],
    "earbuds": ["best wireless earbuds", "noise canceling earbuds review", "premium earbuds", "true wireless earbuds deal"],
    "tablet": ["best tablet 2024", "tablet review comparison", "affordable tablet", "tablet deals online"],
    "speaker": ["best bluetooth speaker", "portable speaker review", "smart speaker deal", "wireless speaker comparison"],
    "default": ["best tech deals 2024", "trending products online", "top rated gadgets", "must have electronics"],
}

BLOG_TEMPLATES = [
    """## {title}: Your Next Must-Have

Looking for the perfect addition to your tech collection? The **{title}** is making waves across the internet, and for good reason. This {category} has been trending on major e-commerce platforms, and savvy shoppers are taking notice.

When it comes to **{kw1}**, this product stands out from the crowd. Industry experts agree that finding the right **{kw2}** can transform your daily experience, and this offering delivers on every front.

What makes this a standout choice? First, the build quality is exceptional. Second, the performance metrics rival products costing twice as much. Whether you're researching **{kw3}** or simply want the best value, this product checks every box.

Don't miss out on this opportunity. With prices fluctuating daily, now is the perfect time to explore **{kw4}** and secure this deal before it's gone.

**👉 [Check Current Price & Availability]({url})**""",

    """## Why Everyone is Talking About {title}

The buzz around **{title}** is real — and it's well-deserved. As one of the most searched items in the **{kw1}** category, this product has captured the attention of tech enthusiasts and casual buyers alike.

In a market flooded with options, finding a reliable **{kw2}** guide is essential. This product rises above the noise with its combination of cutting-edge features and competitive pricing. Users consistently rate it among the top choices when searching for **{kw3}**.

The verdict? Whether you're upgrading your current setup or buying for the first time, this is a {category} that delivers premium quality without the premium price tag. Smart shoppers who stay ahead of **{kw4}** trends know that timing is everything.

**Ready to make the smart choice? [Get Yours Today]({url})**""",

    """## {title} — The Deal You Can't Ignore

Still on the fence? Let us break it down. The **{title}** has been dominating **{kw1}** searches, and after testing it ourselves, we understand the hype completely.

For anyone diving into the world of **{kw2}**, this {category} offers an unbeatable combination of performance, design, and value. It's the kind of product that makes you wonder why you didn't upgrade sooner.

Expert reviewers searching for **{kw3}** consistently place this at the top of their lists. The features-to-price ratio is simply outstanding, making it accessible for budget-conscious buyers and quality seekers alike.

The bottom line: if **{kw4}** is on your radar, this is the product to beat in 2024. Availability is limited, so act fast.

**🔥 [Grab This Deal Now]({url})**""",
]


def _detect_category(title: str) -> str:
    title_lower = title.lower()
    for category in KEYWORD_DATABASE:
        if category in title_lower:
            return category
    brand_category_map = {
        "airpods": "earbuds", "galaxy": "phone", "iphone": "phone",
        "macbook": "laptop", "rog": "laptop", "zephyrus": "laptop",
        "gopro": "camera", "hero": "camera", "dji": "drone",
        "dyson": "vacuum", "roomba": "vacuum", "oled": "tv",
        "lg": "tv", "samsung": "tv", "sony": "headphones",
        "wh-1000": "headphones", "apple watch": "watch",
        "lego": "default", "ipad": "tablet", "echo": "speaker",
    }
    for brand, cat in brand_category_map.items():
        if brand in title_lower:
            return cat
    return "default"


class SEOEngine:
    def __init__(self):
        self.openai_client = None
        self.gemini_client = None
        self.mode = "built-in"

        # Try OpenAI first
        if OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-"):
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
                self.mode = "openai"
                print("✅ OpenAI GPT connected")
            except Exception as e:
                print(f"⚠️ OpenAI not available: {e}")

        # Try Gemini as second option
        if not self.openai_client and GENAI_API_KEY and len(GENAI_API_KEY) > 10:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=GENAI_API_KEY)
                self.mode = "gemini"
                print("✅ Gemini AI connected")
            except Exception as e:
                print(f"⚠️ Gemini not available: {e}")

        if self.mode == "built-in":
            print("ℹ️ Using built-in SEO engine (no API key required)")

    async def _openai_generate(self, prompt: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content

    async def _gemini_generate(self, prompt: str) -> str:
        response = self.gemini_client.models.generate_content(
            model='gemini-2.0-flash', contents=prompt
        )
        return response.text

    async def _ai_generate(self, prompt: str) -> str:
        if self.openai_client:
            return await self._openai_generate(prompt)
        elif self.gemini_client:
            return await self._gemini_generate(prompt)
        return None

    async def generate_keywords(self, product_title: str):
        try:
            result = await self._ai_generate(
                f'Act as an SEO expert. For the product: "{product_title}", provide 4 high-performing SEO keywords. '
                f'For each keyword, provide: keyword, search_intent, competition (Low/Medium/High), and a brief SEO strategy. '
                f'Return as a bulleted list where each line is: keyword | intent | competition | strategy'
            )
            if result:
                keywords_data = []
                lines = [l.strip() for l in result.strip().split("\n") if "|" in l]
                for line in lines[:4]:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 4:
                        keywords_data.append({
                            "keyword": parts[0].replace("-", "").replace("*", "").strip(),
                            "intent": parts[1],
                            "competition": parts[2],
                            "strategy": parts[3]
                        })
                if keywords_data:
                    return keywords_data
        except Exception as e:
            print(f"AI keyword error (falling back): {e}")

        # Fallback
        category = _detect_category(product_title)
        fallback_keywords = KEYWORD_DATABASE.get(category, KEYWORD_DATABASE["default"])
        return [
            {
                "keyword": kw,
                "intent": "Commercial",
                "competition": "Medium",
                "strategy": f"Target long-tail searches for {category}."
            } for kw in fallback_keywords
        ]

    async def generate_blog_post(self, product_title: str, keywords: list):
        try:
            keyword_list = [k["keyword"] for k in keywords]
            keyword_str = ", ".join(keyword_list)
            result = await self._ai_generate(
                f'Act as a professional copywriter. Write a 150-200 word engaging blog post for: "{product_title}". Naturally incorporate these SEO keywords: {keyword_str}. Include a catchy headline and a call to action.'
            )
            if result:
                return result
        except Exception as e:
            print(f"AI content error (falling back): {e}")

        # Fallback
        category = _detect_category(product_title)
        template = random.choice(BLOG_TEMPLATES)
        keyword_list = [k["keyword"] for k in keywords]
        return template.format(
            title=product_title, category=category,
            kw1=keyword_list[0] if len(keyword_list) > 0 else "trending products",
            kw2=keyword_list[1] if len(keyword_list) > 1 else "top deals",
            kw3=keyword_list[2] if len(keyword_list) > 2 else "best picks",
            kw4=keyword_list[3] if len(keyword_list) > 3 else "online shopping",
            url="https://www.ebay.com"
        )


seo_engine = SEOEngine()
