# Singlestat

The Singlestat panel allows you to show the one main summary stat of a single time series.

**Note:** Singlestat has been superseded by the [Stat panel](https://grafana.com/docs/grafana/latest/panels/visualizations/stat-panel/) and is no longer available from Grafana 8.0. For more information on how to migrate, refer to [Migrate to the new Stat panel](#migrate-to-the-new-stat-panel).

## Features

- Reduce a time series into a single numeric value
- Configure thresholds to color the stat or the panel background
- Translate the numeric value into a text value
- Show a sparkline summary of the time series

## Installation

To install using the Grafana CLI, run the following command in the terminal:

```bash
grafana-cli plugins install grafana-singlestat-panel
```

For more ways to install the plugin, refer to [Install Grafana plugins](https://grafana.com/docs/grafana/latest/plugins/installation/).

## Documentation

For more information on how to use the Singlestat panel, refer to [Singlestat Panel
](https://grafana.com/docs/grafana/v6.6/features/panels/singlestat/).

## Migrate to the new Stat panel

Starting with Grafana 8.0, panels using the Singlestat visualization will be automatically migrated to the new Stat panel.

If you don't want to switch to the Stat panel just yet, you can prevent the migration by installing this plugin before you start Grafana.

