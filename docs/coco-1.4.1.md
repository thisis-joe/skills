# COCO 1.4.1: cover images for blog posts

This release adds a cover image step to coco-blog. Other skills, the skill count (30) and the installer interface are unchanged.

- When the consumer blog renders post thumbnails, coco-blog first discovers the thumbnail field, accepted formats and size, upload destination, layout crops and project colors.
- After the draft direction is settled, it offers two or three vector candidates rendered in the conversation. The author chooses one, asks for changes or supplies their own image. Unlicensed images and private screens are not used.
- The chosen image is previewed in the real layouts through a disposable copy outside the source tree; that copy is never committed.
- Upload happens only with authorization, with a warning first when the destination is public before the post is released. The public URL is confirmed before the post references it.
- Blogs without a thumbnail field skip the step.

## Installation after npm publication

```sh
npx --yes @thisis-joe/coco-skills@1.4.1 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.4.1 install --runtime claude
```

Choose the same scope as the existing installation and start a new client session. If this release fails, reinstall pinned 1.4.0 at the same explicit runtime and destination. Source version, GitHub merge and npm publication are separate states.
