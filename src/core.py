import httpx
import pandas as pd

def format_payload(comments):
    """
    """
    
    payload = {
        "user_id": [],
        "comment_id": [],
        "comments": []
    }
    for comment in comments:
        payload["user_id"].append(comment["user_id"])
        payload["comment_id"].append(comment["comment_id"])
        payload["comments"].append(comment["comment"])

    return payload

def call_sentiment_endpoint(payload, sentiment_url):
    """
    """
    
    try:
        response = httpx.post(sentiment_url, json=payload, timeout=60)
    except httpx.ConnectError:
        return {"error": "connection error"}
    except httpx.TimeoutException:
        return {"error": "timeout error"}
    
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

    response = call_sentiment_endpoint(payload, sentiment_url)

    # NOTE: final_result is sentiment count + averaged confidence
    final_result = calculate_final_sentiment(response)

    comments_table = pd.DataFrame(payload)
    final_result_table = pd.DataFrame(response)

    # NOTE: merged_results_table is of individual comment sentiment
    merged_results_table = pd.merge(final_result_table, comments_table, 
                              on="comment_id", how="left").to_html()

    return final_result, merged_results_table

if __name__ == "__main__":
    result = orchestrate_pipeline("", "")
    print(result)