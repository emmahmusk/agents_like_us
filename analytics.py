from os import environ

import requests

import pandas as pd

from datetime import datetime

from openai import OpenAI

def get_crypto_data(symbol, market, start_date, end_date):
    # Calculate the total time span in days
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end_date_obj - start_date_obj).days

    if total_days == 0:
        interval = "30MIN"
    elif total_days <= 7:
        interval = "1HRS"
    elif total_days <= 30:
        interval = "1DAY"
    elif total_days <= 365:
        interval = "7DAY"
    else:
        interval = "1MTH"

    # Download the data
    base_url = "https://rest.coinapi.io/v1/ohlcv"
    symbol_id = f"BITSTAMP_SPOT_{symbol}_{market}"  # Adjust based on your desired exchange

    url = f"{base_url}/{symbol_id}/history"
    headers = {"X-CoinAPI-Key": environ.get("COINAPI_API_KEY")}

    params = {
        "period_id": interval,
        "time_start": start_date,
        "time_end": end_date,
        "limit": 100000
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Convert JSON to DataFrame
        df = pd.DataFrame(data)
        # Format DataFrame
        df = df.rename(columns={
            "time_period_start": "date",
            "price_open": "open",
            "price_close": "close",
            "price_high": "high",
            "price_low": "low",
            "volume_traded": "volume"
        })
        df = df[["date", "open", "close", "high", "low", "volume"]]
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        return df
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except ValueError as e:
        print(f"Data processing error: {e}")

    return pd.DataFrame()


def google_search(query, api_key, search_engine_id):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": search_engine_id,
        "num": 5,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def extract_search_results(search_response):
    results = search_response.get("items", [])
    return [f"Title: {item['title']}\nSnippet: {item['snippet']}\nLink: {item['link']}\n"
            for item in results]


def summarize_with_gpt(content):
    prompt = f"Provide an indepth detailed summary with a proper analysis for following search results:\n{content}\n Summary:"

    client = OpenAI(api_key=environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
          {
              "role": "user",
              "content": prompt,
          }
        ]
    )

    return response.choices[0].message.content


def google_search_with_summary(query):
    search_response = google_search(query, environ.get("GOOGLE_API_KEY"), environ.get("SEARCH_ENGINE_ID"))

    search_results = extract_search_results(search_response)
    search_content = "\n\n".join(search_results)

    summary = summarize_with_gpt(search_content)
    return summary, search_results


if __name__ == "__main__":
    user_query = input("Enter your search query: ")
    summary, search_results = google_search_with_summary(user_query)

    print("\nSummary:")
    print(summary)