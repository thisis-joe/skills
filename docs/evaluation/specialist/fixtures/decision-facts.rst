Selected fixture design: add ``email`` alongside ``contact_email``.
``email`` uses strip and lowercase; ``contact_email`` preserves the raw input.
The backfill batch condition is ``0 <= batch_size <= 500``.
New writes update both fields and increment ``revision``.
A backfill skips/retries any row whose revision changed after scanning.
Normalization is not reversible. Production backups and restore have not been tested.
