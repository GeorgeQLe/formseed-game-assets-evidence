# FormSeed Game Assets — evidence archive

Public, append-only archive of generated review evidence for
[formseed-game-assets](https://github.com/GeorgeQLe/formseed-game-assets):
every gated attempt, including rejected and abandoned ones. See
[ADR 0008](https://github.com/GeorgeQLe/formseed-game-assets/blob/main/docs/decisions/0008-public-lfs-evidence-repository.md).

## License

Everything authored here is released under [CC0 1.0](LICENSE) (public domain
dedication), like Kenney's assets. Third-party reference images are **not**
stored here; manifests record only their URL, sha256, author and license.

## Layout

```
attempts/<assetId>/<jobId>/r<revision>-<gate>/
  manifest.json      # identity, hashes, gate outcome
  review/*.png       # named review render set
  gameplay-256/*.png
  *.labeled.png      # provenance-labeled review sheet
```

Binaries are stored with Git LFS. Verify any file against the sha256 in its
`manifest.json`. An archived attempt is evidence only; it never grants or
implies approval, promotion or integration.
