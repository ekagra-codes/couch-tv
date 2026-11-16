// Tests for Issue #216: Phone remote: make "type on the TV" findable
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const root = path.join(__dirname, '..');
const remoteJsx = fs.readFileSync(path.join(root, 'remote', 'src', 'Remote.jsx'), 'utf8');
const sheetsJsx = fs.readFileSync(path.join(root, 'remote', 'src', 'Sheets.jsx'), 'utf8');
const appJsx = fs.readFileSync(path.join(root, 'remote', 'src', 'App.jsx'), 'utf8');
const stylesCss = fs.readFileSync(path.join(root, 'remote', 'src', 'styles.css'), 'utf8');
const remoteDoc = fs.readFileSync(path.join(root, 'docs', 'REMOTE.md'), 'utf8');

// 1. Controls in Remote.jsx includes the type-key button with keyboard icon
assert(
  /export\s+function\s+Controls\(\s*\{\s*tv,\s*onKey,\s*onVolume,\s*onType\s*\}\s*\)/.test(remoteJsx),
  'Controls should accept onType prop'
);
assert(
  /className="round big glass type-key"/.test(remoteJsx),
  'Controls should render button with class round big glass type-key'
);
assert(
  /<Ic\.Keyboard\s*\/>/.test(remoteJsx),
  'type-key button should render Ic.Keyboard icon'
);

// 2. TypeSheet exported from Sheets.jsx
assert(
  /export\s+const\s+TypeSheet\s*=\s*forwardRef/.test(sheetsJsx),
  'Sheets.jsx should export TypeSheet component'
);
assert(
  /className="type-sheet"/.test(sheetsJsx),
  'TypeSheet should use type-sheet className'
);
assert(
  /onText\(typed\.trim\(\)\)/.test(sheetsJsx),
  'TypeSheet submit should invoke onText callback'
);

// 3. App.jsx renders TypeSheet and hooks openType
assert(
  /import\s*\{[^}]*TypeSheet[^}]*\}\s*from\s*'\.\/Sheets\.jsx'/.test(appJsx),
  'App.jsx should import TypeSheet from Sheets.jsx'
);
assert(
  /const\s+openType\s*=\s*\(\)\s*=>\s*\{[^}]*setSheet\('type'\)/.test(appJsx),
  'App.jsx should define openType opening sheet === "type"'
);
assert(
  /<Controls\s+[^>]*onType=\{openType\}/.test(appJsx),
  'App.jsx should pass onType={openType} to Controls'
);
assert(
  /<TypeSheet\s+ref=\{typeInput\}\s+open=\{sheet\s*===\s*'type'\}/.test(appJsx),
  'App.jsx should render TypeSheet with typeInput ref and open condition'
);

// 4. Styles in styles.css
assert(
  /\.controls\s+\.type-key\s*\{[^}]*color:\s*#f5a623/.test(stylesCss),
  'styles.css should style .controls .type-key with amber color'
);

// 5. Documentation in docs/REMOTE.md
assert(
  /## Typing on the TV/.test(remoteDoc),
  'docs/REMOTE.md should have a section on Typing on the TV'
);
assert(
  /ASCII/.test(remoteDoc),
  'docs/REMOTE.md should document the ASCII limitation for input text'
);

console.log('Phone remote typing tests (#216) passed.');
