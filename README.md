# Arabic Market Miner

An Apify Actor that analyzes Arabic and English customer comments and identifies keyword-based indicators of purchase intent, complaints, and product requests.

## Input

Provide a `comments` array, a publicly accessible direct `csv_url`, or an Apify `dataset_id` from a previous scraper run. For CSV or dataset input, the text column defaults to `comment`; common alternatives `text`, `تعليق`, and `التعليق` are also detected. Set `column_name` to override this.

Example:

```json
{
  "comments": [
    "بكم هذا المنتج؟ وكيف أطلب؟",
    "المنتج وصل متأخر والجودة سيئة",
    "يا ريت توفروا حجم أكبر"
  ]
}
```

For a scraper-to-analysis workflow, run a comments/reviews scraper first, copy its default dataset ID, and pass it as `dataset_id`. The Actor reads the dataset using the current Apify account token.

## Output

The default dataset contains one summary record followed by one analysis record per comment. Fields include purchase-intent indicators, complaint indicators, product-request indicators, matched keywords, and `opportunity_hints` when predefined pain-point phrases are detected. The summary also includes counts by opportunity issue type.

## Important limitation

This Actor is designed as a lightweight second step after a comments/reviews scraper: it can read an Apify dataset directly, then identify buyer-intent indicators and recurring customer problems. It uses transparent keyword matching and predefined rules to suggest possible solution directions for recurring pain points. These are research hints, not validated product opportunities. It does not understand context like a human, verify actual purchase intent, or perform advanced sentiment analysis. Review source comments and validate demand before making business decisions.


## Paid pilot: $5 Market Opportunity Report

Want a deeper analysis for a specific market or product? The proposed **$5 USD** report summarizes recurring complaints, product requests, purchase-intent keyword signals, and possible opportunity areas from your comments/reviews dataset.

This is a pilot offer. It is a research aid based on the supplied data and keyword rules—not proof of demand or a guarantee of sales. **No payment is collected through this request form.** We are first checking whether users genuinely want this report at $5.

[Request the $5 report / register your interest](https://github.com/goo200300400-hub/arabic-market-miner/issues/new?template=paid-report.yml)

## Run locally

Install dependencies with `pip install -r requirements.txt`, then run with the Apify platform or Apify CLI.
