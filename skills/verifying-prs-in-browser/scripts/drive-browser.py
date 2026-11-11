#!/usr/bin/env -S uv run --script
"""
Drive a browser using Playwright via persistent sessions.

Session lifecycle:
    ./drive-browser.py start --session ID [--port PORT] [--width W] [--height H] [--headful]
    ./drive-browser.py stop --session ID
    ./drive-browser.py status [--session ID]

Navigation & interaction:
    ./drive-browser.py open --session ID URL [--timeout MS] [--no-wait-for-idle]
    ./drive-browser.py click --session ID SELECTOR [--native]
    ./drive-browser.py fill --session ID SELECTOR VALUE
    ./drive-browser.py hover --session ID SELECTOR
    ./drive-browser.py press --session ID KEY
    ./drive-browser.py scroll --session ID SELECTOR
    ./drive-browser.py scroll --session ID --container SEL --top PX
    ./drive-browser.py resize --session ID --width W --height H
    ./drive-browser.py wait --session ID SELECTOR [--hidden] [--timeout MS]
    ./drive-browser.py auth --session ID --auth-url URL --username U --password P

Inspection & capture:
    ./drive-browser.py screenshot --session ID [--output PATH] [--full-page]
    ./drive-browser.py text --session ID SELECTOR
    ./drive-browser.py html --session ID [SELECTOR]
    ./drive-browser.py js --session ID EXPRESSION

Accessibility:
    ./drive-browser.py a11y --session ID [--level A|AA|AAA] [--severity critical|serious|moderate|minor] [--verbose]

Video recording:
    ./drive-browser.py start-recording --session ID [--output PATH]
    ./drive-browser.py stop-recording --session ID

Action recording (for headful sessions):
    ./drive-browser.py record --session ID [--output PATH]
    ./drive-browser.py stop-record --session ID

Batch execution:
    ./drive-browser.py batch --session ID < commands.txt

Other:
    ./drive-browser.py detect-servers
"""

# /// script
# requires-python = ">=3.9"
# dependencies = ["playwright"]
# ///

from __future__ import annotations

import argparse
import http.server
import json
import os
import shlex
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "Error: Playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr
    )
    sys.exit(1)


def authenticate(page, auth_url: str, username: str, password: str):
    """Navigate to auth URL and log in.

    Supports both single-step and two-step (Vue.js style) login flows.
    """
    page.goto(auth_url)
    page.wait_for_load_state("networkidle")

    # Wait for Vue/React to render
    page.wait_for_timeout(1000)

    # Common login form patterns (order matters - more specific first)
    username_selectors = [
        "#username input",
        'input[name="username"]',
        'input[name="email"]',
        'input[type="email"]',
        "#id_username",
        "#email",
    ]
    password_selectors = ["#password input", 'input[name="password"]', 'input[type="password"]', "#id_password"]
    submit_selectors = ['button[type="submit"]', 'input[type="submit"]', "#login-button", ".login-button"]
    next_selectors = [".login-btn", 'button:has-text("Next")', 'button:has-text("next")']

    # Find and fill username
    username_filled = False
    for selector in username_selectors:
        try:
            locator = page.locator(selector).first
            if locator.is_visible():
                locator.fill(username)
                username_filled = True
                break
        except Exception:
            continue

    if not username_filled:
        return  # No username field found

    # Check if password field is visible (single-step login)
    password_visible = False
    for selector in password_selectors:
        try:
            locator = page.locator(selector).first
            if locator.is_visible():
                password_visible = True
                break
        except Exception:
            continue

    # Two-step login: click Next button first
    if not password_visible:
        for selector in next_selectors:
            try:
                locator = page.locator(selector).first
                if locator.is_visible():
                    locator.click()
                    # Wait for password form to appear
                    page.wait_for_timeout(1000)
                    break
            except Exception:
                continue

    # Find and fill password
    for selector in password_selectors:
        try:
            locator = page.locator(selector).first
            if locator.is_visible():
                locator.fill(password)
                break
        except Exception:
            continue

    # Submit
    for selector in submit_selectors:
        try:
            locator = page.locator(selector).first
            if locator.is_visible():
                locator.click()
                break
        except Exception:
            continue

    # Wait for navigation
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)


def execute_actions(page, actions: list, pace: int = 0):
    """Execute a sequence of actions on the page.

    Args:
        page: Playwright page object
        actions: List of action dicts
        pace: Milliseconds to pause between actions (0 = fast, 500 = human-like for videos)
    """
    for i, action in enumerate(actions):
        if "click" in action:
            page.locator(action["click"]).evaluate(SYNTHETIC_CLICK_JS)
        elif "fill" in action:
            selector, value = action["fill"]
            page.fill(selector, value)
        elif "wait" in action:
            page.wait_for_timeout(action["wait"])
        elif "scroll" in action:
            page.locator(action["scroll"]).scroll_into_view_if_needed()
        elif "hover" in action:
            page.hover(action["hover"])
        elif "press" in action:
            page.keyboard.press(action["press"])
        elif "goto" in action:
            url = action["goto"]
            if not url.startswith(("http://", "https://")):
                print(f"Warning: goto URL missing scheme: {url}", file=sys.stderr)
            page.goto(url)
            page.wait_for_load_state("networkidle")
        else:
            print(f"Warning: unknown action type: {action}", file=sys.stderr)

        # Add pause between actions for natural pacing in videos
        if pace > 0 and "wait" not in action and i < len(actions) - 1:
            page.wait_for_timeout(pace)


RECORDER_JS = """
(function() {
  // Restore actions saved to sessionStorage before a page unload
  var savedActions = JSON.parse(sessionStorage.getItem('__captureUIActions') || '[]');
  if (savedActions.length > 0) {
    window.__capturedActions = savedActions.concat(window.__capturedActions || []);
    sessionStorage.removeItem('__captureUIActions');
  } else {
    window.__capturedActions = window.__capturedActions || [];
  }

  // Don't re-register event handlers on the same page
  if (window.__captureUIRecorderInstalled) return;
  window.__captureUIRecorderInstalled = true;

  function record(action) {
    window.__capturedActions.push(action);
  }

  // Persist actions across full page loads via sessionStorage
  window.addEventListener('beforeunload', function() {
    if (window.__capturedActions && window.__capturedActions.length > 0) {
      sessionStorage.setItem('__captureUIActions', JSON.stringify(window.__capturedActions));
    }
  });

  // Recording indicator overlay
  const indicator = document.createElement('div');
  indicator.textContent = '⏺ Recording';
  indicator.style.cssText = 'position:fixed;top:8px;right:8px;z-index:999999;' +
    'background:rgba(220,38,38,0.9);color:white;padding:4px 10px;border-radius:4px;' +
    'font:12px/1.4 system-ui,sans-serif;pointer-events:none;';
  document.body.appendChild(indicator);

  // Selector generation with priority
  function getSelector(el) {
    // 1. data-testid
    if (el.dataset && el.dataset.testid) {
      return '[data-testid="' + el.dataset.testid + '"]';
    }
    // 2. id (skip auto-generated — heuristic: ids with 5+ hex chars or uuids)
    if (el.id && !/[0-9a-f]{5,}/i.test(el.id) && !/^:/.test(el.id)) {
      return '#' + CSS.escape(el.id);
    }
    // 3. ARIA role + accessible name (aria-label only, NOT textContent which
    //    concatenates all descendant text and produces unmatchable selectors)
    var role = el.getAttribute('role') || (el.tagName === 'BUTTON' ? 'button' : '');
    var ariaName = el.getAttribute('aria-label');
    if (role && ariaName && ariaName.length <= 60) {
      return 'role=' + role + '[name="' + ariaName.replace(/"/g, '\\\\"') + '"]';
    }
    // 4. placeholder (inputs)
    if (el.placeholder) {
      return '[placeholder="' + el.placeholder.replace(/"/g, '\\\\"') + '"]';
    }
    // 5. name attribute (inputs)
    if (el.tagName === 'INPUT' && el.name) {
      return 'input[name="' + el.name.replace(/"/g, '\\\\"') + '"]';
    }
    // 6. Text content (short, clickable elements)
    var tag = el.tagName.toLowerCase();
    var text = el.textContent.trim();
    if (['a','button','label','th','td','li','span','h1','h2','h3','h4','h5','h6'].includes(tag)
        && text.length > 0 && text.length <= 40 && !text.includes('\\n')) {
      return 'text=' + text;
    }
    // 7. CSS path fallback
    var path = [];
    var current = el;
    while (current && current !== document.body) {
      var seg = current.tagName.toLowerCase();
      if (current.className && typeof current.className === 'string') {
        var cls = current.className.trim().split(/\\s+/).filter(function(c) {
          return c && !/[0-9a-f]{5,}/i.test(c);
        });
        if (cls.length > 0) seg += '.' + cls[0];
      }
      var parent = current.parentElement;
      if (parent) {
        var siblings = Array.from(parent.children).filter(function(s) {
          return s.tagName === current.tagName;
        });
        if (siblings.length > 1) {
          seg += ':nth-child(' + (Array.from(parent.children).indexOf(current) + 1) + ')';
        }
      }
      path.unshift(seg);
      current = current.parentElement;
    }
    return path.join(' > ');
  }

  // Walk up from target to nearest interactive element (button, link, input, etc.)
  // so clicks on inner <span>/<svg> record the parent button's selector
  function findInteractive(el) {
    var tags = ['A','BUTTON','INPUT','SELECT','TEXTAREA'];
    var cur = el;
    while (cur && cur !== document.body) {
      if (tags.includes(cur.tagName) || cur.getAttribute('role')) return cur;
      cur = cur.parentElement;
    }
    return el;
  }

  // Click handler — skip INPUT/TEXTAREA/SELECT (captured by blur handler as fill)
  document.addEventListener('click', function(e) {
    var el = findInteractive(e.target);
    if (['INPUT','TEXTAREA','SELECT'].includes(el.tagName)) return;
    var sel = getSelector(el);
    record({click: sel});
  }, true);

  // Blur handler for inputs — captures final value as a single fill action
  document.addEventListener('blur', function(e) {
    var el = e.target;
    if ((el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT')
        && el.value !== el.defaultValue) {
      var sel = getSelector(el);
      record({fill: [sel, el.value]});
    }
  }, true);

  // Key press handler for special keys
  document.addEventListener('keydown', function(e) {
    if (['Escape','Enter','Tab','ArrowDown','ArrowUp','ArrowLeft','ArrowRight',
         'Backspace','Delete'].includes(e.key)) {
      record({press: e.key});
    }
  }, true);

  // SPA navigation detection via location.href polling + MutationObserver
  var lastHref = location.href;
  var observer = new MutationObserver(function() {
    if (location.href !== lastHref) {
      var newUrl = location.href;
      lastHref = newUrl;
      record({goto: newUrl});
    }
  });
  observer.observe(document.body, {childList: true, subtree: true});
  // Also poll for history.pushState/replaceState changes
  setInterval(function() {
    if (location.href !== lastHref) {
      var newUrl = location.href;
      lastHref = newUrl;
      record({goto: newUrl});
    }
  }, 500);

  // Scroll handler — debounced, emits {scroll: selector} for the element
  // near the bottom of the viewport (what the user scrolled to see)
  var scrollTimer = null;
  window.addEventListener('scroll', function() {
    if (scrollTimer) clearTimeout(scrollTimer);
    scrollTimer = setTimeout(function() {
      var el = document.elementFromPoint(
        window.innerWidth / 2,
        window.innerHeight * 0.75
      );
      if (el && el !== document.body && el !== document.documentElement) {
        var sel = getSelector(el);
        record({scroll: sel});
      }
    }, 300);
  }, true);
})();
"""


SYNTHETIC_CLICK_JS = """
(el) => {
    const opts = {bubbles: true, cancelable: true};
    el.dispatchEvent(new PointerEvent('pointerdown', opts));
    el.dispatchEvent(new MouseEvent('mousedown', opts));
    el.dispatchEvent(new PointerEvent('pointerup', opts));
    el.dispatchEvent(new MouseEvent('mouseup', opts));
    el.dispatchEvent(new MouseEvent('click', opts));
}
"""

PAGE_SNAPSHOT_JS = """
() => {
    const INTERACTIVE = new Set([
        'link', 'button', 'textbox', 'checkbox', 'radio', 'combobox',
        'listbox', 'menuitem', 'tab', 'switch', 'slider', 'spinbutton',
        'searchbox', 'option', 'menuitemcheckbox', 'menuitemradio',
    ]);
    const SKIP = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'SVG', 'PATH']);
    const TAG_ROLE = {
        'A': 'link', 'BUTTON': 'button', 'INPUT': null, 'SELECT': 'combobox',
        'TEXTAREA': 'textbox', 'NAV': 'navigation', 'MAIN': 'main',
        'HEADER': 'banner', 'FOOTER': 'contentinfo', 'ASIDE': 'complementary',
        'FORM': 'form', 'TABLE': 'table', 'THEAD': 'rowgroup', 'TBODY': 'rowgroup',
        'TR': 'row', 'TH': 'columnheader', 'TD': 'cell', 'UL': 'list',
        'OL': 'list', 'LI': 'listitem', 'DIALOG': 'dialog', 'IMG': 'img',
    };
    const INPUT_ROLE = {
        'text': 'textbox', 'email': 'textbox', 'password': 'textbox',
        'search': 'searchbox', 'tel': 'textbox', 'url': 'textbox',
        'number': 'spinbutton', 'range': 'slider', 'checkbox': 'checkbox',
        'radio': 'radio', 'submit': 'button', 'reset': 'button',
        'button': 'button',
    };

    const vw = window.innerWidth, vh = window.innerHeight;

    function getRole(el) {
        const r = el.getAttribute('role');
        if (r) return r;
        if (el.tagName === 'INPUT') return INPUT_ROLE[el.type] || 'textbox';
        if (/^H[1-6]$/.test(el.tagName)) return 'heading';
        return TAG_ROLE[el.tagName] || null;
    }

    function onScreen(el) {
        const r = el.getBoundingClientRect();
        return r.bottom > 0 && r.top < vh && r.right > 0 && r.left < vw && r.width > 0 && r.height > 0;
    }

    function isVisible(el) {
        const s = getComputedStyle(el);
        return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
    }

    function bestSelector(el) {
        const t = el.getAttribute('data-testid') || el.getAttribute('data-test-id');
        if (t) return '[data-testid="' + t + '"]';
        if (el.id) return '#' + CSS.escape(el.id);
        const a = el.getAttribute('aria-label');
        if (a) return '[aria-label="' + a.replace(/"/g, '\\\\"') + '"]';
        const txt = getName(el);
        if (txt && txt.length <= 50) return 'text=' + txt;
        return null;
    }

    function getName(el) {
        const aria = el.getAttribute('aria-label');
        if (aria) return aria.trim();
        const placeholder = el.getAttribute('placeholder');
        if (placeholder) return placeholder.trim();
        // Direct text nodes first, fall back to full textContent
        let direct = '';
        for (const n of el.childNodes) if (n.nodeType === 3) direct += n.textContent;
        direct = direct.trim();
        if (direct) return direct;
        const full = el.textContent.trim().replace(/\\s+/g, ' ');
        return full;
    }

    function walk(el, depth) {
        if (SKIP.has(el.tagName)) return [];
        if (!isVisible(el)) return [];

        const role = getRole(el);
        const lines = [];
        let emitted = false;

        if (role && onScreen(el)) {
            const p = ['  '.repeat(depth) + '[' + role + ']'];
            if (role === 'heading') p.push('level=' + el.tagName[1]);

            const name = getName(el);
            if (name && name.length <= 80) p.push('"' + name.replace(/\\s+/g, ' ').trim() + '"');

            if (el.value !== undefined && el.value !== '') p.push('value="' + String(el.value).substring(0, 40) + '"');
            if (el.disabled) p.push('disabled');
            if (el.checked) p.push('checked');
            if (el.getAttribute('aria-expanded') === 'true') p.push('expanded');
            if (el.getAttribute('aria-selected') === 'true') p.push('selected');

            if (INTERACTIVE.has(role)) {
                const s = bestSelector(el);
                if (s) p.push('-> ' + s);
            }

            lines.push(p.join(' '));
            emitted = true;
        }

        for (const child of el.children) {
            lines.push(...walk(child, emitted ? depth + 1 : depth));
        }
        return lines;
    }

    const lines = walk(document.body, 0);
    return lines.join('\\n');
}
"""

DEFAULT_PORTS = [3000, 4200, 5000, 5173, 8000, 8080, 8888, 9000]


def detect_servers(ports: list[int] = None) -> list[dict]:
    """Check common localhost ports for active HTTP servers."""
    ports = ports or DEFAULT_PORTS
    active = []
    for port in ports:
        try:
            urllib.request.urlopen(f"http://localhost:{port}/", timeout=1.5)
            active.append({"port": port, "url": f"http://localhost:{port}/"})
        except urllib.error.HTTPError:
            # Server is running but returned an error status — still active
            active.append({"port": port, "url": f"http://localhost:{port}/"})
        except (urllib.error.URLError, ConnectionError, OSError, TimeoutError):
            continue
    return active


# --- Session infrastructure ---

SESSIONS_DIR = Path.home() / ".drive-browser" / "sessions"


def _save_state(session_id: str, pid: int, port: int) -> Path:
    """Write session state to disk."""
    session_dir = SESSIONS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "session_id": session_id,
        "pid": pid,
        "port": port,
        "started_at": datetime.now().isoformat(),
    }
    state_file = session_dir / "state.json"
    state_file.write_text(json.dumps(state, indent=2))
    return state_file


def _load_state(session_id: str) -> dict | None:
    """Load session state from disk. Returns None if not found."""
    state_file = SESSIONS_DIR / session_id / "state.json"
    if not state_file.exists():
        return None
    return json.loads(state_file.read_text())


def _remove_state(session_id: str):
    """Remove session state from disk."""
    session_dir = SESSIONS_DIR / session_id
    state_file = session_dir / "state.json"
    if state_file.exists():
        state_file.unlink()
    # Remove log file too
    log_file = session_dir / "daemon.log"
    if log_file.exists():
        log_file.unlink()
    # Remove directory if empty
    try:
        session_dir.rmdir()
    except OSError:
        pass


def _list_sessions() -> list[dict]:
    """List all sessions with state files, annotated with liveness."""
    if not SESSIONS_DIR.exists():
        return []
    sessions = []
    for session_dir in sorted(SESSIONS_DIR.iterdir()):
        state_file = session_dir / "state.json"
        if state_file.exists():
            state = json.loads(state_file.read_text())
            state["alive"] = _is_process_alive(state["pid"])
            sessions.append(state)
    return sessions


def _is_process_alive(pid: int) -> bool:
    """Check if a process is running."""
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def _is_port_available(port: int) -> bool:
    """Check if a TCP port is available for binding."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def _find_available_port(start: int = 9222) -> int:
    """Find the first available port starting from `start`."""
    for port in range(start, start + 100):
        if _is_port_available(port):
            return port
    raise RuntimeError(f"No available port found in range {start}-{start + 99}")


def _get_session_id(args) -> str:
    """Get session ID from args or DRIVE_BROWSER_SESSION env var."""
    session_id = getattr(args, "session", None) or os.environ.get("DRIVE_BROWSER_SESSION")
    if not session_id:
        print("Error: --session ID required (or set DRIVE_BROWSER_SESSION)", file=sys.stderr)
        sys.exit(1)
    return session_id


def _send_command(session_id: str, command: str, **args) -> dict:
    """Send a command to a session daemon. Returns response dict."""
    state = _load_state(session_id)
    if not state:
        print(f"Error: No active session '{session_id}'", file=sys.stderr)
        sys.exit(1)
    if not _is_process_alive(state["pid"]):
        _remove_state(session_id)
        print(
            f"Error: Session '{session_id}' daemon (PID {state['pid']}) is not running. State cleaned up.",
            file=sys.stderr,
        )
        sys.exit(1)
    payload = {"command": command, "args": args}
    req = urllib.request.Request(
        f"http://127.0.0.1:{state['port']}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=120)
    except (ConnectionRefusedError, urllib.error.URLError) as e:
        # Daemon might have crashed between the alive check and the request
        if _is_process_alive(state["pid"]):
            print(f"Error: Session '{session_id}' daemon not responding: {e}", file=sys.stderr)
        else:
            _remove_state(session_id)
            print(f"Error: Session '{session_id}' daemon crashed. State cleaned up.", file=sys.stderr)
        sys.exit(1)
    result = json.loads(resp.read())
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    return result


# --- Session daemon (HTTP server) ---


class SessionHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for the session daemon."""

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length)) if length else {}
        result = self.server.dispatch(data.get("command", ""), data.get("args", {}))
        body = json.dumps(result).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        """Suppress default stderr logging."""
        pass


SEVERITY_ORDER = ["critical", "serious", "moderate", "minor"]

AXE_CDN_URL = "https://cdn.jsdelivr.net/npm/axe-core@latest/axe.min.js"
AXE_CACHE_PATH = Path.home() / ".drive-browser" / "axe-core.min.js"


class SessionServer(http.server.HTTPServer):
    """HTTP server that owns a Playwright browser and dispatches commands."""

    def __init__(self, port: int, playwright, browser, context, page, viewport: tuple):
        self.pw = playwright
        self.browser = browser
        self.context = context
        self.page = page
        self.viewport = viewport
        self.console_messages: list[dict] = []
        self.recording = False
        self.recording_context = None
        self.base_context = None
        self.recording_actions = False
        self._record_output: str | None = None
        self._accumulated_actions: list[dict] = []
        self._setup_console_listener()
        super().__init__(("127.0.0.1", port), SessionHandler)

    def _setup_console_listener(self):
        """Attach console message listener to current page."""
        self.console_messages.clear()
        self.page.on(
            "console",
            lambda msg: self.console_messages.append({"type": msg.type, "text": msg.text, "location": msg.location}),
        )

    def _page_snapshot(self) -> str:
        """Return a compact text representation of visible on-screen elements."""
        return self.page.evaluate(PAGE_SNAPSHOT_JS)

    def dispatch(self, command: str, args: dict) -> dict:
        handler = getattr(self, f"cmd_{command}", None)
        if not handler:
            return {"error": f"Unknown command: {command}"}
        try:
            return handler(**args)
        except Exception as e:
            return {"error": str(e)}

    def cmd_stop(self) -> dict:
        """Stop the daemon."""
        # Schedule shutdown after response is sent
        threading.Thread(target=self.shutdown, daemon=True).start()
        return {"stopped": True}

    def cmd_status(self) -> dict:
        """Return current session status."""
        return {
            "url": self.page.url,
            "title": self.page.title(),
            "viewport": {"width": self.viewport[0], "height": self.viewport[1]},
            "recording": self.recording,
            "recording_actions": self.recording_actions,
        }

    def cmd_open(self, url: str, timeout: int = None, no_wait_for_idle: bool = False) -> dict:
        """Navigate to a URL."""
        self._drain_recorded_actions()
        goto_kwargs = {}
        if timeout is not None:
            goto_kwargs["timeout"] = timeout
        self.page.goto(url, **goto_kwargs)
        wait_state = "domcontentloaded" if no_wait_for_idle else "networkidle"
        self.page.wait_for_load_state(wait_state)
        return {"url": self.page.url, "snapshot": self._page_snapshot()}

    def cmd_click(self, selector: str, native: bool = False) -> dict:
        """Click an element using synthetic events for framework compatibility."""
        if native:
            self.page.click(selector)
        else:
            self.page.locator(selector).evaluate(SYNTHETIC_CLICK_JS)
        return {"clicked": selector, "snapshot": self._page_snapshot()}

    def cmd_fill(self, selector: str, value: str) -> dict:
        """Fill a form field."""
        self.page.fill(selector, value)
        return {"filled": selector, "snapshot": self._page_snapshot()}

    def cmd_hover(self, selector: str) -> dict:
        """Hover over an element."""
        self.page.hover(selector)
        return {"hovered": selector, "snapshot": self._page_snapshot()}

    def cmd_press(self, key: str) -> dict:
        """Press a keyboard key."""
        self.page.keyboard.press(key)
        return {"pressed": key, "snapshot": self._page_snapshot()}

    def cmd_scroll(self, selector: str = None, container: str = None, top: int = None, by: int = None) -> dict:
        """Scroll an element into view, or scroll within a container."""
        if container:
            if by is not None:
                self.page.locator(container).evaluate(f"el => el.scrollTop += {by}")
                result = {"scrolled": container, "by": by}
            else:
                offset = top if top is not None else 0
                self.page.locator(container).evaluate(f"el => el.scrollTop = {offset}")
                result = {"scrolled": container, "top": offset}
        else:
            if selector is None:
                return {"error": "Either selector or --container is required"}
            self.page.locator(selector).scroll_into_view_if_needed()
            result = {"scrolled": selector}
        result["snapshot"] = self._page_snapshot()
        return result

    def cmd_resize(self, width: int, height: int) -> dict:
        """Resize the viewport without restarting the session."""
        self.page.set_viewport_size({"width": width, "height": height})
        self.viewport = (width, height)
        return {"viewport": {"width": width, "height": height}, "snapshot": self._page_snapshot()}

    def cmd_wait(self, selector: str, timeout: int = 30000, hidden: bool = False) -> dict:
        """Wait for an element to be visible (or hidden with --hidden)."""
        state = "hidden" if hidden else "visible"
        self.page.locator(selector).wait_for(state=state, timeout=timeout)
        return {state: selector, "snapshot": self._page_snapshot()}

    def cmd_screenshot(self, output: str = None, full_page: bool = False) -> dict:
        """Take a screenshot."""
        if output is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output = f"capture_{timestamp}.png"
        self.page.screenshot(path=output, full_page=full_page)
        console = list(self.console_messages)
        self.console_messages.clear()
        return {
            "screenshot": output,
            "url": self.page.url,
            "title": self.page.title(),
            "console": console,
        }

    def cmd_text(self, selector: str) -> dict:
        """Get text content of an element."""
        text = self.page.locator(selector).text_content()
        return {"text": text}

    def cmd_html(self, selector: str = None) -> dict:
        """Get HTML of an element or the full page."""
        if selector:
            html = self.page.locator(selector).inner_html()
        else:
            html = self.page.content()
        return {"html": html}

    def cmd_js(self, expression: str) -> dict:
        """Evaluate JavaScript and return the result."""
        result = self.page.evaluate(expression)
        return {"result": result}

    def _inject_axe(self) -> None:
        """Inject axe-core into the page, handling CSP restrictions."""
        try:
            self.page.add_script_tag(url=AXE_CDN_URL)
            return
        except Exception:
            pass  # CSP or network blocked CDN — fall back to inline injection

        # Download and cache axe-core locally, then inject via evaluate()
        if not AXE_CACHE_PATH.exists():
            AXE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(AXE_CDN_URL, AXE_CACHE_PATH)

        axe_source = AXE_CACHE_PATH.read_text()
        self.page.evaluate(axe_source)

    def cmd_a11y(self, level: str = "AA", severity: str = "moderate", verbose: bool = False) -> dict:
        """Run axe-core accessibility audit on the current page."""
        self._inject_axe()
        raw = self.page.evaluate("axe.run()")

        if verbose:
            return {"url": self.page.url, "results": raw}

        # Severity threshold — include this level and above
        severity_idx = SEVERITY_ORDER.index(severity.lower())
        allowed_severities = set(SEVERITY_ORDER[: severity_idx + 1])

        # WCAG level patterns to include
        level_upper = level.upper()
        if level_upper == "A":
            wcag_suffixes = ("a",)
        elif level_upper == "AA":
            wcag_suffixes = ("a", "aa")
        else:  # AAA
            wcag_suffixes = ("a", "aa", "aaa")

        def _matches_wcag_level(tags: list[str]) -> bool:
            """Check if any tag matches the allowed WCAG level pattern.

            Tags like 'wcag2a', 'wcag2aa', 'wcag2aaa' encode the WCAG level.
            Tags like 'wcag111', 'wcag143' are criterion numbers (digits after wcag2)
            and should be ignored for level filtering.
            """
            for t in tags:
                if not t.startswith("wcag2"):
                    continue
                suffix = t[5:]
                # Skip criterion numbers like wcag2111, wcag2143
                if suffix and suffix[0].isdigit():
                    continue
                # suffix should be 'a', 'aa', or 'aaa'
                if suffix in wcag_suffixes:
                    return True
            return False

        filtered = []
        for violation in raw.get("violations", []):
            if violation.get("impact") not in allowed_severities:
                continue
            if not _matches_wcag_level(violation.get("tags", [])):
                continue
            filtered.append(
                {
                    "id": violation["id"],
                    "impact": violation["impact"],
                    "description": violation["description"],
                    "wcag": [t for t in violation.get("tags", []) if t.startswith("wcag2") and not t[5:].isdigit()],
                    "nodes_count": len(violation.get("nodes", [])),
                    "selectors": [n["target"][0] for n in violation.get("nodes", []) if n.get("target")],
                }
            )

        return {
            "url": self.page.url,
            "violations_count": len(filtered),
            "violations": filtered,
        }

    def cmd_auth(self, auth_url: str, username: str, password: str) -> dict:
        """Authenticate using the standard login flow."""
        authenticate(self.page, auth_url, username, password)
        return {"authenticated": auth_url, "snapshot": self._page_snapshot()}

    def cmd_start_recording(self, output: str = None) -> dict:
        """Start video recording by creating a new context with video enabled."""
        if self.recording:
            return {"error": "Already recording"}

        # Save current state
        current_url = self.page.url
        cookies = self.context.cookies()
        # Remember desired output path
        self._recording_output = output

        # Save reference to base context
        self.base_context = self.context

        # Create recording context
        video_dir = Path(output).parent if output else Path(".")
        video_dir.mkdir(parents=True, exist_ok=True)
        self.recording_context = self.browser.new_context(
            viewport={"width": self.viewport[0], "height": self.viewport[1]},
            record_video_dir=str(video_dir),
            record_video_size={"width": self.viewport[0], "height": self.viewport[1]},
        )
        # Restore cookies
        if cookies:
            self.recording_context.add_cookies(cookies)

        # Switch to recording context
        self.context = self.recording_context
        self.page = self.context.new_page()
        self._setup_console_listener()

        # Navigate to where we were
        if current_url and current_url != "about:blank":
            self.page.goto(current_url)
            self.page.wait_for_load_state("networkidle")

        # Re-install action recorder on new context if active
        if self.recording_actions:
            self._install_recorder()

        self.recording = True
        return {"recording": True}

    def cmd_stop_recording(self) -> dict:
        """Stop video recording and return the video path."""
        if not self.recording:
            return {"error": "Not recording"}

        # Save current state before closing recording context
        current_url = self.page.url
        cookies = self.recording_context.cookies()

        # Get video path before closing
        video_path = self.page.video.path()

        # Close recording context (finalizes video file)
        self.recording_context.close()

        # Rename video if output was specified
        output = getattr(self, "_recording_output", None)
        if output and video_path:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            Path(video_path).rename(output_path)
            video_result = str(output_path)
        else:
            video_result = str(video_path)

        # Restore base context
        self.context = self.base_context
        self.page = self.context.new_page()
        self._setup_console_listener()

        # Restore cookies and navigate back
        if cookies:
            self.context.add_cookies(cookies)
        if current_url and current_url != "about:blank":
            self.page.goto(current_url)
            self.page.wait_for_load_state("networkidle")

        # Re-install action recorder on restored context if active
        if self.recording_actions:
            self._install_recorder()

        self.recording = False
        self.recording_context = None
        self.base_context = None
        self._recording_output = None

        return {"video": video_result}

    # --- Action recording (for headful sessions) ---

    def _drain_recorded_actions(self):
        """Collect actions from browser JS array into server-side accumulator.

        Called before navigation (which resets JS state) to preserve actions
        across page loads. No-op if not recording.
        """
        if not self.recording_actions:
            return
        try:
            page_actions = self.page.evaluate("window.__capturedActions || []")
            if page_actions:
                self._accumulated_actions.extend(page_actions)
                self.page.evaluate("window.__capturedActions = []")
        except Exception:
            pass  # Page may be navigating, JS context unavailable

    def _install_recorder(self):
        """Inject RECORDER_JS on current context/page."""
        self.context.add_init_script(RECORDER_JS)
        # Reset the guard so the IIFE actually runs on the current page
        # (add_init_script may have already set it for future pages)
        self.page.evaluate("window.__captureUIRecorderInstalled = false")
        self.page.evaluate(RECORDER_JS)

    def cmd_record(self, output: str = None) -> dict:
        """Start recording user actions via injected JavaScript."""
        if self.recording_actions:
            return {"error": "Already recording actions"}
        self.recording_actions = True
        self._record_output = output
        self._accumulated_actions = []
        # Clear any stale sessionStorage from previous recordings
        try:
            self.page.evaluate("sessionStorage.removeItem('__captureUIActions')")
        except Exception:
            pass
        self._install_recorder()
        return {"recording_actions": True}

    def cmd_stop_record(self) -> dict:
        """Stop recording actions and return them."""
        if not self.recording_actions:
            return {"error": "Not recording actions"}
        # Drain any remaining actions from the current page before stopping
        self._drain_recorded_actions()
        self.recording_actions = False
        actions = list(self._accumulated_actions)
        self._accumulated_actions = []
        save_path = self._record_output
        if save_path:
            Path(save_path).write_text(json.dumps(actions, indent=2))
        self._record_output = None
        return {"actions": actions, "count": len(actions)}


def _ensure_chromium():
    """Install Chromium browser binary if not already present."""
    subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        check=True,
        capture_output=True,
    )


def _serve(session_id: str, port: int, width: int, height: int, headful: bool = False):
    """Internal daemon entry point. Starts Playwright + HTTP server."""
    pw = sync_playwright().start()
    try:
        browser = pw.chromium.launch(headless=not headful)
    except Exception:
        pw.stop()
        _ensure_chromium()
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=not headful)
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()

    server = SessionServer(port, pw, browser, context, page, (width, height))
    try:
        server.serve_forever()
    finally:
        try:
            browser.close()
        except Exception:
            pass
        try:
            pw.stop()
        except Exception:
            pass


# --- Session client functions ---


def session_start(session_id: str, port: int = None, width: int = 1280, height: int = 720, headful: bool = False):
    """Start a new session daemon."""
    # Check for existing session
    state = _load_state(session_id)
    if state and _is_process_alive(state["pid"]):
        print(f"Error: Session '{session_id}' already running (PID {state['pid']}). Use 'stop' first.", file=sys.stderr)
        sys.exit(1)
    elif state:
        # Stale state, clean up
        _remove_state(session_id)

    if port is None:
        port = _find_available_port()
    elif not _is_port_available(port):
        print(f"Error: Port {port} is already in use", file=sys.stderr)
        sys.exit(1)

    # Ensure log directory exists
    log_dir = SESSIONS_DIR / session_id
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "daemon.log"

    cmd = [
        sys.executable,
        __file__,
        "_serve",
        "--session",
        session_id,
        "--port",
        str(port),
        "--width",
        str(width),
        "--height",
        str(height),
    ]
    if headful:
        cmd.append("--headful")

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=open(log_path, "w"),
        start_new_session=True,
    )

    _save_state(session_id, proc.pid, port)

    # Wait for daemon to be ready
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        try:
            req = urllib.request.Request(
                f"http://127.0.0.1:{port}",
                data=json.dumps({"command": "status", "args": {}}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=2)
            print(f'Started session "{session_id}" (PID {proc.pid}) on port {port}')
            return
        except (ConnectionRefusedError, urllib.error.URLError, OSError):
            if proc.poll() is not None:
                # Process exited
                _remove_state(session_id)
                log_content = log_path.read_text() if log_path.exists() else "(no log)"
                print(f"Error: Daemon exited immediately.\n{log_content}", file=sys.stderr)
                sys.exit(1)
            time.sleep(0.3)

    # Timeout
    proc.kill()
    _remove_state(session_id)
    print("Error: Daemon failed to start within 15 seconds", file=sys.stderr)
    sys.exit(1)


def session_stop(session_id: str):
    """Stop a running session daemon."""
    state = _load_state(session_id)
    if not state:
        print(f"Error: No active session '{session_id}'", file=sys.stderr)
        sys.exit(1)

    pid = state["pid"]
    if not _is_process_alive(pid):
        _remove_state(session_id)
        print(f'Session "{session_id}" was not running. State cleaned up.')
        return

    # Try graceful stop via HTTP (bypass _send_command to avoid sys.exit on error)
    try:
        payload = {"command": "stop", "args": {}}
        req = urllib.request.Request(
            f"http://127.0.0.1:{state['port']}",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass

    # Wait for process to exit
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and _is_process_alive(pid):
        time.sleep(0.2)

    # Force kill if still alive
    if _is_process_alive(pid):
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    _remove_state(session_id)
    print(f'Stopped session "{session_id}"')


def session_status(session_id: str = None):
    """Show session status."""
    if session_id:
        state = _load_state(session_id)
        if not state:
            print(f"Error: No active session '{session_id}'", file=sys.stderr)
            sys.exit(1)
        alive = _is_process_alive(state["pid"])
        if alive:
            result = _send_command(session_id, "status")
            result.update({"session_id": session_id, "pid": state["pid"], "port": state["port"]})
            print(json.dumps(result, indent=2))
        else:
            _remove_state(session_id)
            print(f"Session '{session_id}' is not running. State cleaned up.", file=sys.stderr)
            sys.exit(1)
    else:
        sessions = _list_sessions()
        if not sessions:
            print("No active sessions")
        else:
            print(json.dumps(sessions, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Action recording subcommands
    record_parser = subparsers.add_parser("record", help="Start recording user actions in the session")
    record_parser.add_argument("--session", help="Session ID (or set DRIVE_BROWSER_SESSION)")
    record_parser.add_argument("--output", "-o", help="Output JSON file path for recorded actions")

    stop_rec_actions_parser = subparsers.add_parser("stop-record", help="Stop recording user actions")
    stop_rec_actions_parser.add_argument("--session", help="Session ID (or set DRIVE_BROWSER_SESSION)")

    # Detect-servers subcommand
    detect_parser = subparsers.add_parser("detect-servers", help="Check common localhost ports for active dev servers")
    detect_parser.add_argument(
        "--ports", help="Comma-separated list of ports to check (default: 3000,4200,5000,5173,8000,8080,8888,9000)"
    )

    # Session lifecycle subcommands
    start_parser = subparsers.add_parser("start", help="Start a persistent browser session")
    start_parser.add_argument("--session", help="Session ID (or set DRIVE_BROWSER_SESSION)")
    start_parser.add_argument("--port", type=int, help="Port for session daemon (auto-assigned if omitted)")
    start_parser.add_argument("--width", type=int, default=1280, help="Viewport width")
    start_parser.add_argument("--height", type=int, default=720, help="Viewport height")
    start_parser.add_argument(
        "--headful", action="store_true", help="Show browser window (for human observation/collaboration)"
    )

    stop_parser = subparsers.add_parser("stop", help="Stop a persistent browser session")
    stop_parser.add_argument("--session", help="Session ID (or set DRIVE_BROWSER_SESSION)")

    status_parser = subparsers.add_parser("status", help="Show session status")
    status_parser.add_argument("--session", help="Session ID (omit to list all)")

    # Navigation & interaction subcommands
    def _add_session_arg(p):
        p.add_argument("--session", help="Session ID (or set DRIVE_BROWSER_SESSION)")

    open_parser = subparsers.add_parser("open", help="Navigate to a URL")
    _add_session_arg(open_parser)
    open_parser.add_argument("--timeout", type=int, default=None, help="Navigation timeout in ms")
    open_parser.add_argument(
        "--no-wait-for-idle", action="store_true", help="Don't wait for network idle (use domcontentloaded)"
    )
    open_parser.add_argument("url", help="URL to navigate to")

    click_parser = subparsers.add_parser("click", help="Click an element")
    _add_session_arg(click_parser)
    click_parser.add_argument(
        "--native", action="store_true", help="Use Playwright native click instead of synthetic events"
    )
    click_parser.add_argument("selector", help="CSS/text selector")

    fill_parser = subparsers.add_parser("fill", help="Fill a form field")
    _add_session_arg(fill_parser)
    fill_parser.add_argument("selector", help="CSS/text selector")
    fill_parser.add_argument("value", help="Value to fill")

    hover_parser = subparsers.add_parser("hover", help="Hover over an element")
    _add_session_arg(hover_parser)
    hover_parser.add_argument("selector", help="CSS/text selector")

    press_parser = subparsers.add_parser("press", help="Press a keyboard key")
    _add_session_arg(press_parser)
    press_parser.add_argument("key", help="Key to press (e.g., Enter, Escape)")

    scroll_parser = subparsers.add_parser("scroll", help="Scroll element into view or scroll within a container")
    _add_session_arg(scroll_parser)
    scroll_parser.add_argument("selector", nargs="?", default=None, help="CSS/text selector to scroll into view")
    scroll_parser.add_argument("--container", help="CSS selector for scrollable container")
    scroll_parser.add_argument("--top", type=int, default=None, help="Scroll container to this pixel offset")
    scroll_parser.add_argument("--by", type=int, default=None, help="Scroll container by this many pixels")

    resize_parser = subparsers.add_parser("resize", help="Resize viewport without restarting session")
    _add_session_arg(resize_parser)
    resize_parser.add_argument("--width", type=int, required=True, help="New viewport width")
    resize_parser.add_argument("--height", type=int, required=True, help="New viewport height")

    wait_parser = subparsers.add_parser("wait", help="Wait for an element to appear or disappear")
    _add_session_arg(wait_parser)
    wait_parser.add_argument("selector", help="CSS/text selector")
    wait_parser.add_argument("--hidden", action="store_true", help="Wait for element to disappear instead")
    wait_parser.add_argument("--timeout", type=int, default=30000, help="Timeout in ms")

    # Inspection & capture subcommands
    screenshot_parser = subparsers.add_parser("screenshot", help="Take a screenshot")
    _add_session_arg(screenshot_parser)
    screenshot_parser.add_argument("--output", "-o", help="Output file path")
    screenshot_parser.add_argument("--full-page", action="store_true", help="Capture full page")

    text_parser = subparsers.add_parser("text", help="Get text content of an element")
    _add_session_arg(text_parser)
    text_parser.add_argument("selector", help="CSS/text selector")

    html_parser = subparsers.add_parser("html", help="Get HTML content")
    _add_session_arg(html_parser)
    html_parser.add_argument("selector", nargs="?", help="CSS/text selector (omit for full page)")

    js_parser = subparsers.add_parser("js", help="Evaluate JavaScript")
    _add_session_arg(js_parser)
    js_parser.add_argument("expression", help="JavaScript expression")

    auth_parser = subparsers.add_parser("auth", help="Authenticate in the session")
    _add_session_arg(auth_parser)
    auth_parser.add_argument("--auth-url", required=True, help="Login page URL")
    auth_parser.add_argument("--username", required=True, help="Login username")
    auth_parser.add_argument("--password", required=True, help="Login password")

    # Accessibility auditing
    a11y_parser = subparsers.add_parser("a11y", help="Run axe-core accessibility audit")
    _add_session_arg(a11y_parser)
    a11y_parser.add_argument(
        "--level", default="AA", choices=["A", "AA", "AAA"], help="WCAG conformance level (default: AA)"
    )
    a11y_parser.add_argument(
        "--severity",
        default="moderate",
        choices=["critical", "serious", "moderate", "minor"],
        help="Minimum severity threshold (default: moderate)",
    )
    a11y_parser.add_argument("--verbose", action="store_true", help="Return full axe-core response (unfiltered)")

    # Video recording subcommands
    start_rec_parser = subparsers.add_parser("start-recording", help="Start video recording")
    _add_session_arg(start_rec_parser)
    start_rec_parser.add_argument("--output", "-o", help="Output video path")

    stop_rec_parser = subparsers.add_parser("stop-recording", help="Stop video recording")
    _add_session_arg(stop_rec_parser)

    # Internal daemon subcommand (hidden from help)
    serve_parser = subparsers.add_parser("_serve", help=argparse.SUPPRESS)
    serve_parser.add_argument("--session", required=True)
    serve_parser.add_argument("--port", type=int, required=True)
    serve_parser.add_argument("--width", type=int, default=1280)
    serve_parser.add_argument("--height", type=int, default=720)
    serve_parser.add_argument("--headful", action="store_true")

    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Execute commands from stdin sequentially")
    _add_session_arg(batch_parser)

    args = parser.parse_args()

    try:
        if args.command == "detect-servers":
            ports = [int(p) for p in args.ports.split(",")] if args.ports else None
            servers = detect_servers(ports=ports)
            print(json.dumps(servers))
            return

        elif args.command == "record":
            sid = _get_session_id(args)
            result = _send_command(sid, "record", output=args.output)
            print("Recording actions... interact with the browser, then run 'stop-record'")

        elif args.command == "stop-record":
            sid = _get_session_id(args)
            result = _send_command(sid, "stop_record")
            print(json.dumps(result))

        elif args.command == "start":
            sid = _get_session_id(args)
            session_start(sid, port=args.port, width=args.width, height=args.height, headful=args.headful)

        elif args.command == "stop":
            sid = _get_session_id(args)
            session_stop(sid)

        elif args.command == "status":
            session_status(getattr(args, "session", None) or os.environ.get("DRIVE_BROWSER_SESSION"))

        elif args.command == "_serve":
            _serve(args.session, args.port, args.width, args.height, headful=args.headful)

        elif args.command == "batch":
            sid = _get_session_id(args)
            _batch_specs = {
                "open": {
                    "positional": ["url"],
                    "flags": {"--timeout": ("timeout", int), "--no-wait-for-idle": ("no_wait_for_idle", None)},
                },
                "click": {"positional": ["selector"], "flags": {"--native": ("native", None)}},
                "fill": {"positional": ["selector", "value"], "flags": {}},
                "hover": {"positional": ["selector"], "flags": {}},
                "press": {"positional": ["key"], "flags": {}},
                "scroll": {
                    "positional": [],
                    "flags": {"--container": ("container", str), "--top": ("top", int), "--by": ("by", int)},
                },
                "resize": {"positional": [], "flags": {"--width": ("width", int), "--height": ("height", int)}},
                "screenshot": {
                    "positional": [],
                    "flags": {"--output": ("output", str), "--full-page": ("full_page", None)},
                },
                "text": {"positional": ["selector"], "flags": {}},
                "html": {"positional": [], "flags": {}},
                "js": {"positional": ["expression"], "flags": {}},
            }
            for line in sys.stdin:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = shlex.split(line)
                cmd_name = parts[0]
                cmd_args = parts[1:]

                if cmd_name == "wait":
                    ms = int(cmd_args[0]) if cmd_args else 1000
                    time.sleep(ms / 1000.0)
                    print(json.dumps({"waited": ms}))
                    continue

                if cmd_name == "scroll" and cmd_args and not cmd_args[0].startswith("--"):
                    result = _send_command(sid, "scroll", selector=cmd_args[0])
                    print(json.dumps(result))
                    continue

                spec = _batch_specs.get(cmd_name)
                if spec is None:
                    print(json.dumps({"error": f"Unknown batch command: {cmd_name}"}))
                    continue

                kwargs = {}
                positional_idx = 0
                i = 0
                while i < len(cmd_args):
                    arg = cmd_args[i]
                    if arg.startswith("--"):
                        flag_spec = spec["flags"].get(arg)
                        if flag_spec:
                            name, typ = flag_spec
                            if typ is None:
                                kwargs[name] = True
                            else:
                                i += 1
                                kwargs[name] = typ(cmd_args[i])
                    else:
                        if positional_idx < len(spec["positional"]):
                            kwargs[spec["positional"][positional_idx]] = arg
                            positional_idx += 1
                    i += 1

                result = _send_command(sid, cmd_name, **kwargs)
                print(json.dumps(result))

        # Session commands (thin wrappers around _send_command)
        elif args.command == "open":
            sid = _get_session_id(args)
            result = _send_command(
                sid, "open", url=args.url, timeout=args.timeout, no_wait_for_idle=args.no_wait_for_idle
            )
            print(result["url"])
            print(result.get("snapshot", ""))

        elif args.command == "click":
            sid = _get_session_id(args)
            result = _send_command(sid, "click", selector=args.selector, native=args.native)
            print(result["clicked"])
            print(result.get("snapshot", ""))

        elif args.command == "fill":
            sid = _get_session_id(args)
            result = _send_command(sid, "fill", selector=args.selector, value=args.value)
            print(result["filled"])
            print(result.get("snapshot", ""))

        elif args.command == "hover":
            sid = _get_session_id(args)
            result = _send_command(sid, "hover", selector=args.selector)
            print(result["hovered"])
            print(result.get("snapshot", ""))

        elif args.command == "press":
            sid = _get_session_id(args)
            result = _send_command(sid, "press", key=args.key)
            print(result["pressed"])
            print(result.get("snapshot", ""))

        elif args.command == "scroll":
            sid = _get_session_id(args)
            result = _send_command(
                sid,
                "scroll",
                container=args.container,
                top=args.top,
                by=args.by,
                selector=args.selector,
            )
            print(json.dumps({k: v for k, v in result.items() if k != "snapshot"}))
            print(result.get("snapshot", ""))

        elif args.command == "resize":
            sid = _get_session_id(args)
            result = _send_command(sid, "resize", width=args.width, height=args.height)
            print(json.dumps(result.get("viewport")))
            print(result.get("snapshot", ""))

        elif args.command == "wait":
            sid = _get_session_id(args)
            result = _send_command(sid, "wait", selector=args.selector, timeout=args.timeout, hidden=args.hidden)
            state = "hidden" if args.hidden else "visible"
            print(result[state])
            print(result.get("snapshot", ""))

        elif args.command == "screenshot":
            sid = _get_session_id(args)
            result = _send_command(sid, "screenshot", output=args.output, full_page=args.full_page)
            print(json.dumps(result, indent=2))

        elif args.command == "text":
            sid = _get_session_id(args)
            result = _send_command(sid, "text", selector=args.selector)
            print(result["text"])

        elif args.command == "html":
            sid = _get_session_id(args)
            result = _send_command(sid, "html", selector=args.selector)
            print(result["html"])

        elif args.command == "js":
            sid = _get_session_id(args)
            result = _send_command(sid, "js", expression=args.expression)
            print(json.dumps(result["result"]))

        elif args.command == "auth":
            sid = _get_session_id(args)
            result = _send_command(sid, "auth", auth_url=args.auth_url, username=args.username, password=args.password)
            print(f"Authenticated at {result['authenticated']}")
            print(result.get("snapshot", ""))

        elif args.command == "a11y":
            sid = _get_session_id(args)
            result = _send_command(sid, "a11y", level=args.level, severity=args.severity, verbose=args.verbose)
            print(json.dumps(result, indent=2))

        elif args.command == "start-recording":
            sid = _get_session_id(args)
            result = _send_command(sid, "start_recording", output=args.output)
            print("Recording started")

        elif args.command == "stop-recording":
            sid = _get_session_id(args)
            result = _send_command(sid, "stop_recording")
            print(json.dumps(result))

    except PlaywrightTimeout as e:
        print(f"Error: Timeout - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
