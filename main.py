import asyncio
import json
import logging
from static_types import Product

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from config import (
    DEEPSEEK_API_KEY,
    LLM_PROVIDER,
    INSTRUCTION_TO_LLM,
    MAX_TOKENS,
    TEMPERATURE,
)


def create_extraction_strategy():
    return LLMExtractionStrategy(
        provider=LLM_PROVIDER,
        instruction=INSTRUCTION_TO_LLM,
        api_token=DEEPSEEK_API_KEY,
        extraction_type="schema",
        schema=Product.model_json_schema(),
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        extra_args={"temperature": TEMPERATURE, "max_tokens": MAX_TOKENS},
    )


def create_run_config(extraction_strategy):
    return CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        cache_mode=CacheMode.BYPASS,
        process_iframes=False,
        remove_overlay_elements=True,
        exclude_external_links=True,
    )


async def crawl_urls(crawler, urls, run_config):
    tasks = [crawler.arun(url=url, config=run_config) for url in urls]
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        logging.error("Exception occurred during crawler run", exc_info=True)
        return {}

    all_extracted = {}
    for idx, result in enumerate(results):
        current_url = urls[idx]
        if isinstance(result, Exception):
            logging.error(
                "Exception occurred while processing %s: %s", current_url, result
            )
            continue

        if result.success:
            data = json.loads(result.extracted_content)
            all_extracted[current_url] = data
            logging.info("Extracted items from %s collected.", current_url)
        else:
            logging.error("Error processing %s: %s", current_url, result.error_message)
    return all_extracted


def save_extracted_data(all_extracted, filename="extracted_aeterna_data.json"):
    with open(filename, "w") as outfile:
        json.dump(all_extracted, outfile, indent=4)
    logging.info("All extracted items saved to %s", filename)


async def run_crawler():
    extraction_strategy = create_extraction_strategy()
    browser_config = BrowserConfig(headless=True, verbose=True)
    run_config = create_run_config(extraction_strategy)

    urls = [
        "https://www.aeterna-aesthetics.com/services/facials",
        "https://www.aeterna-aesthetics.com/services/injections",
        "https://www.aeterna-aesthetics.com/services/contouring",
    ]

    async with AsyncWebCrawler(config=browser_config) as crawler:
        all_extracted = await crawl_urls(crawler, urls, run_config)
        save_extracted_data(all_extracted)
        extraction_strategy.show_usage()


async def main():
    await run_crawler()


if __name__ == "__main__":
    asyncio.run(main())
