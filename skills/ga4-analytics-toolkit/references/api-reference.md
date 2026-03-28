# GA4 API Reference

Complete reference for GA4 Analytics and Search Console API functions.

## GA4 Analytics Functions

### Core Reporting

| Function | Description |
|----------|-------------|
| `runReport(propertyId, dateRange, dimensions, metrics)` | Run a custom GA4 report |
| `getAvailableMetrics()` | List all available GA4 metrics |
| `getAvailableDimensions()` | List all available GA4 dimensions |

### Pre-Built Reports

| Function | Description |
|----------|-------------|
| `siteOverview(dateRange)` | Comprehensive site snapshot |
| `trafficSources(dateRange)` | Traffic source breakdown |
| `pagePerformance(dateRange)` | Page-by-page metrics |
| `userDemographics(dateRange)` | User age, gender, interests |
| `deviceAnalysis(dateRange)` | Device category breakdown |
| `geographicReport(dateRange)` | Country/region/city data |
| `conversionTracking(dateRange)` | Goal completions and values |

### Real-Time

| Function | Description |
|----------|-------------|
| `liveSnapshot()` | Current active users |
| `realtimeActiveUsers()` | Count of active users |

### Engagement

| Function | Description |
|----------|-------------|
| `eventAnalysis(dateRange)` | Event-based metrics |
| `engagementRate(dateRange)` | Engagement calculations |
| `sessionDuration(dateRange)` | Session length analysis |

---

## Search Console Functions

### Core

| Function | Description |
|----------|-------------|
| `searchAnalytics(siteUrl, dateRange)` | Core search data |
| `topQueries(siteUrl, dateRange)` | Top search queries |
| `topPages(siteUrl, dateRange)` | Top performing pages |
| `searchAppearance(dateRange)` | Search appearance data |

### Advanced

| Function | Description |
|----------|-------------|
| `keywordAnalysis(dateRange)` | Keyword performance with device breakdown |
| `seoPagePerformance(dateRange)` | Page-level SEO metrics |
| `countryBreakdown(dateRange)` | Geographic performance |

---

## Indexing API

| Function | Description |
|----------|-------------|
| `reindexUrls(urls)` | Request URL re-indexing |
| `checkIndexStatus(urls)` | Check indexing status |
| `getIndexingErrors()` | List indexing errors |

---

## Date Range Object

```javascript
// GA4 format
{ startDate: "30daysAgo", endDate: "today" }

// Explicit dates
{ startDate: "2026-01-01", endDate: "2026-03-27" }

// Shorthand (used in high-level functions)
"7d"   // Last 7 days
"30d"  // Last 30 days
"90d"  // Last 90 days
```

---

## Response Format

All functions return structured JSON:

```javascript
{
  success: true,
  data: { ... },           // Response data
  metadata: {
    propertyId: "123456789",
    dateRange: "30d",
    generatedAt: "2026-03-27T13:00:00Z"
  }
}
```

Error format:

```javascript
{
  success: false,
  error: {
    code: "NOT_FOUND",
    message: "Property not found"
  }
}
```
