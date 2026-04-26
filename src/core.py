import httpx
import pandas as pd

def format_payload(comments):
    """
    """
    if not comments:
        return {"error": "posts does not contain comments"}

    texts = []
    for comment in comments:
        text_entry = {"text": comment["comment"], 
                      "text_id": comment["comment_id"]}
        texts.append(text_entry)

    return {"texts": texts}

def call_sentiment_endpoint(payload, sentiment_url):
    """
    """
    if sentiment_url is None:
        return {"error": "api key cannot be located"}
    
    try:
        response = httpx.post(sentiment_url, json=payload, timeout=60)
        if response.status_code == 404:
            return {"error": "incorrect api url"}
    except httpx.ConnectError:
        return {"error": "sentiment api connection error"}
    except httpx.TimeoutException:
        return {"error": "timeout error"}
    except httpx.RequestError:
        return {"error": "request error"}
    
    return response.json()

def calculate_final_sentiment(response_json):
    """
    """
    sentiment_count = {"NEGATIVE": 0, "POSITIVE": 0}
    sentiment_confidence = float(0)

    for result in response_json:

        sentiment_confidence+=max(result["sentiment_confidence"])

        if result["sentiment_classification"] == "NEGATIVE":
            sentiment_count["NEGATIVE"]+=1
        else:
            sentiment_count["POSITIVE"]+=1

    mean_conf = sentiment_confidence/len(response_json)
    return [{"sentiment_count": sentiment_count},
            {"sentiment_confidence": round(mean_conf, 3)}]


def orchestrate_pipeline(comments, sentiment_url):
    """
    """
    payload = format_payload(comments)
    if isinstance(payload, dict) & ("error" in payload):
            return payload, pd.DataFrame().to_html()

    response = call_sentiment_endpoint(payload, sentiment_url)
    if isinstance(response, dict) & ("error" in response):
            return response, pd.DataFrame().to_html()

    # NOTE: final_result is sentiment count + averaged confidence
    final_result = calculate_final_sentiment(response["sentiment"])

    comments_table = pd.DataFrame(payload["texts"])
    final_result_table = pd.DataFrame(response["sentiment"])

    # NOTE: merged_results_table is of individual comment sentiment
    merged_results_table = pd.merge(final_result_table, comments_table, 
                              on="text_id", how="left")
    merged_results_table["sentiment_confidence"] = round(merged_results_table["sentiment_confidence"].apply(max) * 100, 2)
    columns = ["sentiment_classification", "sentiment_confidence", "text"]
    merged_results_table = merged_results_table[columns]
    merged_results_table = merged_results_table.to_html()

    return final_result, merged_results_table
