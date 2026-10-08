# Compatibility

## Tested local runtime

- Screenpipe desktop path with local writable Pi runtime
- `@earendil-works/pi-coding-agent` `0.84.1`
- `@earendil-works/pi-ai` `0.84.1`
- Apple Silicon macOS

## Assumptions

1. Screenpipe installs or uses a writable local Pi runtime under:
   - `~/.screenpipe/pi-agent`
2. The target file still contains a recognizable `modelFromJson()` anchor
3. Screenpipe is launched through this healer wrapper or installed launcher

## Not guaranteed

1. arbitrary upstream file layout changes
2. Windows or Linux launcher UX
3. future runtime versions whose patch target no longer resembles the tested file

## Upgrade guidance

After a Screenpipe or Pi runtime update:

```bash
tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --check
```

If the result is `anchor_miss`, inspect the new target file and update the manifest or patch logic.
