# Arabic Market Miner

An Apify Actor that analyzes Arabic and English customer comments and identifies keyword-based indicators of purchase intent, complaints, and product requests.

## Input

Provide either a `comments` array or a publicly accessible direct `csv_url`. For CSV input, the comment column defaults to `comment`; common alternatives `text`, `تعليق`, and `التعليق` are also detected. Set `column_name` to override this.

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

## Output

The default dataset contains one summary record followed by one analysis record per comment. Fields include purchase-intent indicators, complaint indicators, product-request indicators, matched keywords, and `opportunity_hints` when predefined pain-point phrases are detected. The summary also includes counts by opportunity issue type.

## Important limitation

This Actor uses transparent keyword matching and predefined rules to suggest possible solution directions for recurring pain points. These are research hints, not validated product opportunities. It does not understand context like a human, verify actual purchase intent, or perform advanced sentiment analysis. Review source comments and validate demand before making business decisions.

## Run locally

Install dependencies with `pip install -r requirements.txt`, then run with the Apify platform or Apify CLI.
