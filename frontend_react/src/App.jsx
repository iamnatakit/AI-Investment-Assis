import { useState, useRef, useEffect, useCallback } from 'react'

const EXAMPLE_PROMPTS = [
  'วิเคราะห์หุ้น AAPL ให้หน่อย',
  'พอร์ตความเสี่ยงต่ำควรลงทุนอะไร?',
  'RSI กับ MACD ต่างกันอย่างไร?',
  'ทองคำกับหุ้นอะไรดีกว่าในช่วงนี้?',
]

const SESSION_ID = `session-${Math.random().toString(36).slice(2)}`
const USER_ID = 'user-demo-001'

function formatTime(ms) {
  if (ms == null) return '—'
  return ms < 1000 ? `${ms}ms` : `${(ms / 1000).toFixed(1)}s`
}

function formatCost(usd) {
  if (usd == null) return '—'
  if (usd === 0) return '$0.00 (free)'
  return usd < 0.001 ? `$${(usd * 1000).toFixed(4)}m` : `$${usd.toFixed(5)}`
}

export default function App() {
  const [mode, setMode] = useState('baseline') // 'baseline' | 'intent'
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [lastMeta, setLastMeta] = useState(null)
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  // Clear conversation when switching modes
  useEffect(() => {
    setMessages([])
    setLastMeta(null)
  }, [mode])

  const sendMessage = useCallback(async (text) => {
    const msgText = (text || input).trim()
    if (!msgText || loading) return

    setInput('')
    setLoading(true)

    const userMsg = { role: 'user', content: msgText, ts: Date.now() }
    setMessages(prev => [...prev, userMsg])

    try {
      const endpoint = mode === 'baseline'
        ? '/investment-ai-agent/chat'
        : '/investment-ai-agent-intent/chat'

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: SESSION_ID, user_id: USER_ID, message: msgText }),
      })

      if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`)

      const data = await res.json()

      const botContent = mode === 'baseline' ? data.message : data.answer
      const botMsg = { role: 'bot', content: botContent, ts: Date.now() }
      setMessages(prev => [...prev, botMsg])

      // Extract metadata for analytics panel
      if (mode === 'baseline') {
        setLastMeta({
          mode: 'baseline',
          tokens: data.usage?.total_tokens,
          prompt_tokens: data.usage?.prompt_tokens,
          completion_tokens: data.usage?.completion_tokens,
          cost_usd: data.cost_usd,
          latency_ms: data.latency_ms,
        })
      } else {
        setLastMeta({
          mode: 'intent',
          tokens: data.usage?.total_tokens,
          prompt_tokens: data.usage?.prompt_tokens,
          completion_tokens: data.usage?.completion_tokens,
          cost_usd: data.billing?.cost_usd,
          cost_thb: data.billing?.cost_thb,
          latency_ms: data.latency_ms,
          intent: data.intent,
          selected_agent: data.selected_agent,
          selected_model: data.selected_model,
        })
      }
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'bot',
        content: `⚠️ เกิดข้อผิดพลาด: ${err.message}\n\nกรุณาตรวจสอบว่า Backend กำลังทำงานอยู่บน port ${mode === 'baseline' ? '8801' : '8802'}`,
        ts: Date.now(),
        isError: true,
      }])
    } finally {
      setLoading(false)
    }
  }, [input, loading, mode])

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <>
      {/* Header */}
      <header className="header">
        <div className="header-logo">
          <div className="logo-icon">📈</div>
          <h1>Investment AI Agent</h1>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div className="status-dot" />
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            {mode === 'baseline' ? 'Baseline · Port 8801' : 'Intent Optimized · Port 8802'}
          </span>
        </div>
      </header>

      {/* Main */}
      <div className="main-layout">
        {/* Mode Selector */}
        <div className="mode-selector">
          <button
            id="btn-baseline"
            className={`mode-btn ${mode === 'baseline' ? 'active' : ''}`}
            onClick={() => setMode('baseline')}
          >
            <span>🤖</span>
            <div>
              <div>Baseline Agent</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Single LLM · Large Prompt</div>
            </div>
            <span className="mode-badge badge-baseline">Project 1</span>
          </button>
          <button
            id="btn-intent"
            className={`mode-btn ${mode === 'intent' ? 'active-intent' : ''}`}
            onClick={() => setMode('intent')}
          >
            <span>🧠</span>
            <div>
              <div>Intent Optimized</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Multi-Agent · Dynamic Routing</div>
            </div>
            <span className="mode-badge badge-intent">Project 2</span>
          </button>
        </div>

        {/* Chat Panel */}
        <div className="chat-panel">
          <div className="chat-messages">
            {messages.length === 0 && !loading ? (
              <div className="empty-state">
                <div className="empty-icon">💬</div>
                <h3>เริ่มต้นถามเกี่ยวกับการลงทุน</h3>
                <p style={{ fontSize: '0.83rem' }}>ลองถามเกี่ยวกับหุ้น, พอร์ตโฟลิโอ, หรือกลยุทธ์การลงทุน</p>
                <div className="example-prompts">
                  {EXAMPLE_PROMPTS.map((p, i) => (
                    <button key={i} className="example-chip" onClick={() => sendMessage(p)}>{p}</button>
                  ))}
                </div>
              </div>
            ) : (
              <>
                {messages.map((msg, i) => (
                  <div key={i} className={`message ${msg.role}`}>
                    <div className={`msg-avatar ${msg.role === 'user' ? 'user-av' : 'bot-av'}`}>
                      {msg.role === 'user' ? '👤' : msg.role === 'bot' && msg.isError ? '⚠️' : '🤖'}
                    </div>
                    <div>
                      <div className="msg-bubble" style={msg.isError ? { borderColor: 'rgba(239,68,68,0.4)', background: 'rgba(239,68,68,0.05)' } : {}}>
                        {msg.content}
                      </div>
                      <div className="msg-meta">
                        {new Date(msg.ts).toLocaleTimeString('th-TH')}
                      </div>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="message bot">
                    <div className="msg-avatar bot-av">🤖</div>
                    <div className="msg-bubble">
                      <div className="typing-indicator">
                        <div className="typing-dot" />
                        <div className="typing-dot" />
                        <div className="typing-dot" />
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="chat-input-area">
            <div className="input-row">
              <textarea
                id="chat-input"
                ref={textareaRef}
                className="chat-input"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="พิมพ์คำถามเกี่ยวกับการลงทุน... (Enter เพื่อส่ง)"
                rows={1}
                disabled={loading}
              />
              <button
                id="send-btn"
                className="send-btn"
                onClick={() => sendMessage()}
                disabled={!input.trim() || loading}
                title="ส่งข้อความ"
              >
                ➤
              </button>
            </div>
          </div>
        </div>

        {/* Analytics Panel */}
        <div className="analytics-panel">
          <p className="analytics-title">📊 Analytics &amp; Metrics</p>

          {!lastMeta ? (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', padding: '2rem 0' }}>
              ส่งข้อความเพื่อดู metrics
            </div>
          ) : (
            <>
              <div className="metric-grid">
                <div className="metric-card">
                  <div className="metric-label">Total Tokens</div>
                  <div className="metric-value blue">
                    {lastMeta.tokens?.toLocaleString() ?? '—'}
                    <span className="metric-unit"> tok</span>
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Latency</div>
                  <div className="metric-value amber">
                    {formatTime(lastMeta.latency_ms)}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Prompt Tokens</div>
                  <div className="metric-value" style={{ fontSize: '1.2rem' }}>
                    {lastMeta.prompt_tokens?.toLocaleString() ?? '—'}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Completion Tokens</div>
                  <div className="metric-value" style={{ fontSize: '1.2rem' }}>
                    {lastMeta.completion_tokens?.toLocaleString() ?? '—'}
                  </div>
                </div>
              </div>

              <div className="metric-card">
                <div className="metric-label">Cost (USD)</div>
                <div className="metric-value green" style={{ fontSize: '1.3rem' }}>
                  {formatCost(lastMeta.cost_usd)}
                </div>
                {lastMeta.cost_thb != null && (
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                    ≈ ฿{lastMeta.cost_thb?.toFixed(4)} THB
                  </div>
                )}
              </div>

              {lastMeta.mode === 'intent' && lastMeta.intent && (
                <>
                  <p className="analytics-title">🧠 Intent Classification</p>
                  <div className="intent-card">
                    <div className="intent-row">
                      <span className="intent-key">Domain</span>
                      <span className="intent-val">
                        <span className="tag tag-purple">{lastMeta.intent.domain ?? '—'}</span>
                      </span>
                    </div>
                    <div className="intent-row">
                      <span className="intent-key">Complexity</span>
                      <span className="intent-val">
                        <span className="tag tag-blue">{lastMeta.intent.complexity ?? '—'}</span>
                      </span>
                    </div>
                    <div className="intent-row">
                      <span className="intent-key">Selected Agent</span>
                      <span className="intent-val">{lastMeta.selected_agent ?? '—'}</span>
                    </div>
                    <div className="intent-row">
                      <span className="intent-key">Selected Model</span>
                      <span className="intent-val" style={{ fontSize: '0.75rem', wordBreak: 'break-all' }}>
                        {lastMeta.selected_model ?? '—'}
                      </span>
                    </div>
                    {lastMeta.intent.ticker && (
                      <div className="intent-row">
                        <span className="intent-key">Ticker</span>
                        <span className="intent-val">
                          <span className="tag tag-green">{lastMeta.intent.ticker}</span>
                        </span>
                      </div>
                    )}
                    {lastMeta.intent.reason && (
                      <div style={{ marginTop: '0.75rem', padding: '0.625rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        💡 {lastMeta.intent.reason}
                      </div>
                    )}
                  </div>
                </>
              )}

              <div style={{
                background: 'var(--bg-card)',
                border: '1px solid var(--border-color)',
                borderRadius: '12px',
                padding: '0.875rem',
                fontSize: '0.78rem',
                color: 'var(--text-muted)',
                marginTop: 'auto',
              }}>
                <span style={{ color: 'var(--accent-amber)' }}>⚡ Mode: </span>
                {lastMeta.mode === 'baseline' ? 'Baseline (Single LLM)' : 'Intent Optimized (Multi-Agent)'}
              </div>
            </>
          )}
        </div>
      </div>
    </>
  )
}
