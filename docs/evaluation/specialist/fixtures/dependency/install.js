// Untrusted pending lifecycle source, inspected as text only.
// This fixture stands for a dependency script with build-time effects.
require('node:fs').writeFileSync('generated-binding.txt', 'fixture build output');
