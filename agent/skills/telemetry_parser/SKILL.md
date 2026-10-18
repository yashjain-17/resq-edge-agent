# Skill: Telemetry and Mission Log Parser

## Description
Parses incoming drone telemetry streams, GPS waypoints, and thermal sensor logs to extract anomalies, calculate search sectors, and answer tactical queries offline.

## Tools
- parse_flight_log: Reads JSON telemetry data and flags altitude or battery drops.
- nalyze_thermal_grid: Scans thermal sensor arrays for temperature spikes indicating human presence.
