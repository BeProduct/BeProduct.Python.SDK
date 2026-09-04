# Tracking API

Tracking plans hold one timeline per style / material (or per colorway / SKU)
with milestone dates.

```python
client.tracking.folders()                       # tracking folders
plans = client.tracking.plan_list()             # enumerator, optional filters / folder_id
plan = client.tracking.plan_get(plan_id)

# Timelines and views
client.tracking.plan_style_timeline_list(plan_id, filters=None)
client.tracking.plan_style_timeline_update(plan_id, timelines)
client.tracking.plan_style_tracking_view(plan_id, view_id, filters=None)
# (the same three exist with plan_material_ for materials)

# Progress and revision history
client.tracking.plan_style_progress(plan_id)
client.tracking.plan_material_progress(plan_id)
client.tracking.plan_style_revisions(plan_id, filters=None)      # enumerator
client.tracking.plan_material_revisions(plan_id, filters=None)   # enumerator

# Adding items to a plan
client.tracking.plan_style_add(plan_id, [style_id])                       # one timeline per style
client.tracking.plan_style_by_colorway_add(plan_id, [style_id])            # one timeline per colorway of each style
client.tracking.plan_style_by_sku_add(plan_id, [                          # one timeline per SKU
    {"headerId": style_id, "sku": [{"colorwayId": colorway_id, "sizes": ["S", "M"]}]},
])
client.tracking.plan_material_add(plan_id, [material_id])
client.tracking.plan_material_by_colorway_add(plan_id, [material_id])      # one timeline per colorway of each material

# Removing timelines
client.tracking.plan_style_timelines_archive(plan_id, [timeline_id])
client.tracking.plan_style_timelines_delete(plan_id, [timeline_id])
client.tracking.plan_material_timelines_delete(plan_id, [timeline_id])
```
