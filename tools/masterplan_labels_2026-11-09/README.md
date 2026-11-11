# Masterplan labels tools (9-11 Nov 2026)

These are Claude's helper scripts for the masterplan label layers. They are not part of the GH board kit, so Aras doesn't run them and they are not listed in kit/.

- roads/: layer 8 (clean roads), layer 9 (Kışla/bridge corrections), layer 10 (Kızıl Avlu circulation) and layer 11 (red dotted paths south of the Selinos). The roads are drawn from OSM (feat.json) on the 9 Nov 09:00 plan (B19_setB_layers2_0600.svg).
- zones/: zone explanations.
  - zsnap.py snaps Aras's marked zones to the plan buildings and OSM places inside them (zones_v2.json). Zone 4 uses the OSM Kızıl Avlu boundary.
  - build_zones.py draws the 9 style previews plus style 4 v5.
  - zones_layer.py writes the layer-only SVG (layer_12_zones_v5.svg) on the plan file's page size and coordinates.
- Paths point at the project folder /mnt/project-files/planting_masterplan_2026-11-08/masterplan_labels_2026-11-08/, where the outputs and INDEX.md are.
