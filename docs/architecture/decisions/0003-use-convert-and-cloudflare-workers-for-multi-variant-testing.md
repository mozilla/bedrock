# 3. Use Convert and Cloudflare Workers for multi-variant testing

Date: 2019-10-09

## Status

Accepted

## Context

Our current method for implementing multi-variant tests involves frequent, often non-trivial code changes to our most high traffic download pages. Prioritizing and running concurrent experiments on such pages is also often complex, increasing the risk of accidental breakage and making longer-term changes harder to roll out. Our current tool, [Traffic Cop](https://github.com/mozilla/trafficcop/), also requires significant custom code to accomodate these types of situations. Accurately measuring and reporting on the outcome of experiments is also a time consuming step of the process for our data science team, often requiring custom instrumentation and analysis.

We would like to make our end-to-end experimentation process faster, with increased capacity, whilst also minimizing the performance impact and volume of code churn related to experiments running on our most important web pages.

## Decision

We will implement a (vetted and approved) third-party experimentation tool called [Convert](https://www.convert.com/) for use on standalone, experimental pages only. We will then use [Cloudflare Workers](https://www.cloudflare.com/en-gb/products/cloudflare-workers/) to redirect a small percentage of traffic to the experimental pages. The worker code will live in the [www-workers](https://github.com/mozmeao/www-workers) repository.

## Consequences

Convert experiment code will not touch our main web pages, where the vast majority of our traffic is routed. This will minimize code churn on our most important conversion funnels, and also reduce the performance impact and risks involved in using a third-party experimentation tool. Using Cloudflare Workers to redirect only a small percentage of traffic to experimental pages also has significant performance benefits over handling redirection client-side.

Convert features a custom dashboard for configuring, prioritizing, and running multi-variant tests. It also has built-in analysis and reporting features, which are all areas where we hope to see significant savings in time and resources.
