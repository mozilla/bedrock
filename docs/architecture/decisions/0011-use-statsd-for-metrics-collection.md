# 11. Use StatsD for metrics collection

Date: 2023-05-19

## Status

Accepted

## Context

We need to implement a metrics collection solution to gain insights into the performance and
behavior of bedrock. Metrics play a crucial role in understanding system health, identifying
bottlenecks, and making informed decisions for optimization and troubleshooting.

## Decision

StatsD is a proven open-source solution that provides a lightweight and scalable approach to
capturing, aggregating, and visualizing application metrics. It offers numerous benefits that align
with bedrock's needs:

1. **Simplicity and Ease of Integration**: StatsD is easy to install and integrate into our existing
Python codebase. It provides a simple API that allows us to instrument our code and send metrics
with minimal effort.

2. **Aggregation and Sampling**: StatsD supports various aggregation methods, such as sum, average,
maximum, and minimum, which can be applied to collected metrics. Additionally, it provides built-in
support for sampling, allowing us to reduce the volume of metrics collected while still maintaining
statistical significance.

3. **Scalability**: StatsD is designed to handle high volumes of metrics and can easily scale
horizontally to accommodate increasing demands. It relies on a fire-and-forget mechanism, where the
metrics are sent asynchronously, ensuring minimal impact on the performance of our application.

4. **Integration with Monitoring and Visualization Tools**: At Mozilla we already have a stack
available and configured by SRE that uses StatsD along with Telegraf to send metrics to Grafana for
visualization and monitoring. This integration will enable us to analyze and visualize our metrics,
create dashboards, and set up alerts for critical system thresholds.

### Overview of how StatsD, Telegraf, and Grafana work together.

Here's an overview of how these tools fit into the workflow:

* **StatsD**:
  StatsD is responsible for collecting and aggregating metrics data within the application.  It
  provides a simple API that allows us to instrument our code and send metrics to a StatsD server.
  StatsD operates over UDP and uses a lightweight protocol for sending metrics.
* **Telegraf**:
  Telegraf is an agent-based data collection tool that can receive metrics from various sources,
  including StatsD. Telegraf acts as an intermediary between the data source (StatsD) and the data
  visualization tool (Grafana). It can collect, process, and forward metrics data to different
  destinations.
* **Grafana**:
  Grafana is a popular open-source data visualization and monitoring tool. It provides a rich set of
  features for creating dashboards, visualizing metrics, and setting up alerts. Grafana can connect
  to Telegraf to retrieve metrics data and display it in a user-friendly and customizable manner.

## Consequences

1. **Metrics Design and Instrumentation**: Proper metrics design and instrumentation are crucial to
deriving meaningful insights. We need to invest time and effort in identifying the key metrics to
capture and strategically instrument our codebase to provide actionable data for analysis.

2. **Operational Overhead**: Introducing a new tool requires additional operational effort for
monitoring, maintaining, and scaling the StatsD infrastructure. However, since this infrastructure
is in use currently by other projects within Mozilla, this overhead is already being assumed and is
spread out across projects.

3. **Integration Effort**: While integrating StatsD into bedrock is relatively straightforward, we
will need to allocate development time to instrument our codebase and ensure that metrics are
captured at relevant points within the application.

### Considerations and best practices for metrics design

* **Identify Key Metrics**:
  Identify the key aspects of our website that we want to monitor and measure. These could include
  response times, error rates, database query performance, and cache hit ratios.
* **Granularity and Context**:
  Determine the appropriate level of granularity for our metrics. We can choose to measure metrics
  at the application level, specific Django views, individual API endpoints, or even down to
  specific functions or code blocks within bedrock.
* **Define Consistent Metric Names**:
  Choose meaningful and consistent names for our metrics. This helps in easily understanding and
  interpreting the collected data. 
* **Timing Metrics**:
  Use timing metrics to measure the duration of specific operations. This can include measuring the
  time taken to render a template, execute a database query, or process a request.  StatsD provides
  a timing metric type that captures the duration and calculates statistics such as average,
  maximum, and minimum durations.
* **Counting Metrics**:
  Use counting metrics to track occurrences of specific events. This can include counting the number
  of requests received or the number of errors encountered. StatsD supports counting metric types
  that increments a value each time an event occurs.
* **Sampling**:
  Consider implementing sampling to reduce the number of metrics collected while still maintaining
  statistical significance. We can selectively sample a subset of requests or events to ensure a
  representative sample of data for analysis if a particular metric is of high volume.
* **Re-evaluate often**:
  Continuously evaluate our metrics and refine them based on changing requirements and insights
  gained from analysis.
