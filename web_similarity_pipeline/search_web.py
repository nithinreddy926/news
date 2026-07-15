from ddgs import DDGS

def search_web(query, max_results=10):
    urls = []

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

        for r in results:
            if "href" in r:
                urls.append(r["href"])

    return urls
