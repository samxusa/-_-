---
name: GitHub connector pushes
description: How repository pushes work when the workspace has an added GitHub connector but no shell credential.
---

When authenticated shell git credentials are unavailable, use the added GitHub connector to create blobs for changed files, build a tree from the remote branch head, create a commit, and fast-forward the branch ref through the Git Data API.

**Why:** The connector keeps GitHub credentials out of the workspace and still supports a complete multi-file push without exposing tokens.

**How to apply:** Resolve the GitHub integration first, read the remote branch head before writing, preserve the remote tree as `base_tree`, and verify the updated branch ref after the commit.