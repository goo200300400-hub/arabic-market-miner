# Arabic E-commerce Review & Complaint Analyzer

Find recurring customer complaints, product requests, and keyword-based buying signals in Arabic and English e-commerce reviews.

**Arabic Market Miner** is an Apify Actor for store owners, e-commerce agencies, and market researchers who need to turn customer comments into a structured feedback summary. It works on pasted comments, a public CSV, or a dataset produced by another Apify scraper.

## What you can discover

- Repeated customer problems such as late delivery, damaged products, high prices, poor quality, and difficult product use.
- Comments containing keyword-based buying signals such as price questions, availability questions, and ordering questions.
- Product requests and recurring themes worth investigating.
- Possible solution directions linked to detected pain points.

## Run it

Choose one input method:

1. **Paste comments** into `comments`.
2. **Analyze a CSV** by providing a public direct `csv_url`.
3. **Analyze scraped reviews** by providing the `dataset_id` from a previous Apify scraper run.

Example input:

```json
{
  "comments": [
    "بكم هذا المنتج؟ وكيف أطلب؟",
    "المنتج وصل متأخر والجودة سيئة",
    "يا ريت توفروا حجم أكبر",
    "The product arrived broken and customer support did not reply."
  ]
}
```

For a scraper-to-analysis workflow, run a reviews or comments scraper first, then pass its dataset ID to this Actor. The Actor reads the dataset using the current Apify account token. The text column defaults to `comment`; common alternatives such as `text`, `تعليق`, and `التعليق` are detected automatically. Set `column_name` to override it.

## Output

The default dataset contains a summary record followed by one record per comment.

| Output | What it shows |
|---|---|
| Summary | Total comments and counts of buying indicators, complaints, and product requests |
| Top terms | Frequently matched complaint and purchase-intent keywords |
| Opportunity signals | Counts of detected pain-point types |
| Comment analysis | Matched categories, keywords, and possible solution directions for each comment |

## Sample report

See [an illustrative Arabic e-commerce feedback report](SAMPLE_REPORT.md). The example data is fictional and demonstrates the report format only.

## Important methodology note

This Actor uses transparent keyword matching and predefined rules. It does not understand context like a human, verify actual purchase intent, or perform advanced sentiment analysis. A detected buying phrase is an indicator in the text, not proof that the person will purchase. Opportunity hints are hypotheses based on recurring pain-point phrases, not validated product opportunities.

## Best use case

Use Arabic Market Miner after collecting product reviews, store comments, or customer feedback. It helps e-commerce teams quickly organize feedback and decide which issues deserve closer investigation.
