// Server locale per la demo: serve l'app e inoltra le chiamate dei 4 agenti a Claude.
//
// Modalità predefinita: Claude Agent SDK con il login di Claude Code già presente sul computer.
//   Nessuna chiave API: si usa la licenza Claude Code della persona che avvia il server.
//   Uso:  cd app && npm install && npm start      poi apri http://localhost:8080
//
// Modalità alternativa: chiave API della Claude Platform.
//   Uso:  MODALITA=api ANTHROPIC_API_KEY=sk-ant-... npm start
//
// Le credenziali restano sul computer: il browser non le vede mai.
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORTA = process.env.PORT || 8080;
const MODALITA = process.env.MODALITA === "api" ? "api" : "sdk";
const MODELLO = process.env.MODELLO || (MODALITA === "sdk" ? "sonnet" : "claude-sonnet-4-6");
const TIPI = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".jpg": "image/jpeg", ".png": "image/png", ".css": "text/css" };

/* ---------- Modalità SDK: login di Claude Code ---------- */
let sdk = null;
async function caricaSdk() {
  if (!sdk) sdk = await import("@anthropic-ai/claude-agent-sdk"); // l'SDK è un modulo ESM
  return sdk;
}

// Gli agenti dell'app non devono usare strumenti (file, terminale, web): solo leggere e rispondere.
const negaStrumenti = async () => ({ behavior: "deny", message: "Gli agenti di Un passo alla volta non usano strumenti." });

async function chiamaConSdk({ system, messages, model }) {
  const { query } = await caricaSdk();
  const content = messages[0].content;
  async function* ingresso() {
    yield { type: "user", message: { role: "user", content }, parent_tool_use_id: null };
  }
  // Togliamo un'eventuale chiave API dall'ambiente: così l'SDK usa il login di Claude Code.
  const { ANTHROPIC_API_KEY, ...ambiente } = process.env;
  const risposta = query({
    prompt: ingresso(),
    options: {
      systemPrompt: system,       // sostituisce il prompt di sistema di Claude Code con quello dell'agente
      model: model || MODELLO,
      maxTurns: 1,                // una domanda, una risposta
      allowedTools: [],
      canUseTool: negaStrumenti,
      settingSources: [],         // non carica CLAUDE.md o impostazioni del progetto
      env: ambiente,
    },
  });
  let testo = "", modelloUsato = model || MODELLO;
  for await (const m of risposta) {
    if (m.type === "assistant" && m.message?.model) modelloUsato = m.message.model;
    if (m.type === "result") {
      if (m.subtype !== "success" || m.is_error) throw new Error(`Claude Agent SDK: ${m.subtype}${m.result ? " - " + m.result : ""}`);
      testo = m.result;
    }
  }
  // Stesso formato dell'API Messages: l'app non deve sapere quale modalità è attiva
  return { status: 200, body: JSON.stringify({ model: modelloUsato, content: [{ type: "text", text: testo }] }) };
}

/* ---------- Modalità API: chiave della Claude Platform ---------- */
async function chiamaConApi(dati) {
  const chiave = process.env.ANTHROPIC_API_KEY;
  if (!chiave) return { status: 503, body: "MODALITA=api richiede ANTHROPIC_API_KEY" };
  dati.model = MODELLO;
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "content-type": "application/json", "x-api-key": chiave, "anthropic-version": "2023-06-01" },
    body: JSON.stringify(dati),
  });
  return { status: r.status, body: await r.text() };
}

/* ---------- Server ---------- */
function leggiCorpo(req) {
  return new Promise((ok, ko) => { let c = ""; req.on("data", x => (c += x)); req.on("end", () => ok(c)); req.on("error", ko); });
}

http.createServer(async (req, res) => {
  if (req.method === "POST" && req.url === "/api/messages") {
    const t0 = Date.now();
    try {
      const dati = JSON.parse(await leggiCorpo(req));
      if (MODALITA === "sdk") dati.model = MODELLO; // il modello lo decide il server, non il browser
      const r = MODALITA === "sdk" ? await chiamaConSdk(dati) : await chiamaConApi(dati);
      console.log(`[${MODALITA}] risposta ${r.status} in ${Date.now() - t0} ms`);
      res.writeHead(r.status, { "content-type": "application/json" });
      res.end(r.body);
    } catch (e) {
      console.error(`[${MODALITA}] errore:`, e.message);
      res.writeHead(502, { "content-type": "text/plain; charset=utf-8" });
      res.end(String(e.message || e));
    }
    return;
  }
  const rel = req.url === "/" ? "index.html" : decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "");
  const file = path.join(__dirname, rel);
  if (!file.startsWith(__dirname) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end("Non trovato"); }
  res.writeHead(200, { "content-type": TIPI[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
}).listen(PORTA, async () => {
  console.log(`Un passo alla volta: http://localhost:${PORTA}`);
  if (MODALITA === "sdk") {
    try { await caricaSdk(); console.log(`Modalità: Claude Agent SDK con il login di Claude Code (modello: ${MODELLO})`); }
    catch { console.warn("Claude Agent SDK non installato. Eseguire 'npm install' nella cartella app/. Intanto l'app userà le risposte preparate."); }
  } else {
    console.log(`Modalità: chiave API (modello: ${MODELLO})${process.env.ANTHROPIC_API_KEY ? "" : " - ATTENZIONE: ANTHROPIC_API_KEY non impostata"}`);
  }
});
