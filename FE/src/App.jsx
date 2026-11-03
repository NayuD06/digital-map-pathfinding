// Bố cục chính: bản đồ bên trái, bảng điều khiển bên phải
import { useCallback, useEffect, useState } from 'react'
import { compareRoutes, findRoute, getGraphInfo, getHistory } from './api/client.js'
import BenchmarkPanel from './components/BenchmarkPanel.jsx'
import CompareChart from './components/CompareChart.jsx'
import ControlPanel from './components/ControlPanel.jsx'
import HistoryPanel from './components/HistoryPanel.jsx'
import MapView from './components/MapView.jsx'
import StatsPanel from './components/StatsPanel.jsx'

const TABS = [
  { key: 'route', label: 'Tìm đường' },
  { key: 'benchmark', label: 'Benchmark' },
]

export default function App() {
  const [graphInfo, setGraphInfo] = useState(null)
  const [graphError, setGraphError] = useState(null)
  const [tab, setTab] = useState('route')
  const [start, setStart] = useState(null)
  const [end, setEnd] = useState(null)
  const [algo, setAlgo] = useState('astar')
  const [results, setResults] = useState([])
  const [showVisited, setShowVisited] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])
  const [historyError, setHistoryError] = useState(null)

  const databaseEnabled = Boolean(graphInfo?.database_enabled)

  const loadGraphInfo = useCallback(() => {
    setGraphError(null)
    getGraphInfo()
      .then(setGraphInfo)
      .catch((e) => setGraphError(e.message))
  }, [])

  const loadHistory = useCallback(() => {
    getHistory(10)
      .then((items) => {
        setHistory(items)
        setHistoryError(null)
      })
      .catch((e) => setHistoryError(e.message))
  }, [])

  useEffect(loadGraphInfo, [loadGraphInfo])

  useEffect(() => {
    if (databaseEnabled) loadHistory()
  }, [databaseEnabled, loadHistory])

  function resetResults() {
    setResults([])
    setError(null)
  }

  // Click lần 1 chọn điểm đi, lần 2 chọn điểm đến, lần 3 chọn lại từ đầu
  function handleMapClick(latlng) {
    if (!start || end) {
      setStart(latlng)
      setEnd(null)
    } else {
      setEnd(latlng)
    }
    resetResults()
  }

  function handleMove(setPoint) {
    return (latlng) => {
      setPoint(latlng)
      resetResults()
    }
  }

  async function run(request) {
    setLoading(true)
    setError(null)
    try {
      setResults(await request())
      if (databaseEnabled) loadHistory()
    } catch (e) {
      setResults([])
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleFind = () => run(async () => [await findRoute(algo, start, end)])
  const handleCompare = () => run(async () => (await compareRoutes(start, end)).results)

  // Chọn một dòng lịch sử: đặt lại 2 điểm, thuật toán và chạy lại
  function handleHistorySelect(item) {
    const from = { lat: item.from_lat, lng: item.from_lng }
    const to = { lat: item.to_lat, lng: item.to_lng }
    setStart(from)
    setEnd(to)
    setAlgo(item.algorithm)
    run(async () => [await findRoute(item.algorithm, from, to)])
  }

  function handleClear() {
    setStart(null)
    setEnd(null)
    resetResults()
  }

  let hint = 'Click lên bản đồ để chọn điểm đi.'
  if (start && !end) hint = 'Click để chọn điểm đến.'
  if (start && end) hint = 'Kéo marker để đổi điểm, click bản đồ để chọn lại từ đầu.'

  return (
    <div className="app">
      <main className="map-area">
        {graphInfo ? (
          <MapView
            graphInfo={graphInfo}
            start={start}
            end={end}
            results={results}
            showVisited={showVisited}
            onMapClick={handleMapClick}
            onStartMove={handleMove(setStart)}
            onEndMove={handleMove(setEnd)}
          />
        ) : (
          <div className="map-placeholder">
            {graphError ? (
              <>
                <p className="error">{graphError}</p>
                <button onClick={loadGraphInfo}>Thử lại</button>
              </>
            ) : (
              <p>Đang tải thông tin bản đồ…</p>
            )}
          </div>
        )}
      </main>

      <aside className="sidebar">
        <header>
          <h1>Tìm đường trên bản đồ số</h1>
          {graphInfo && (
            <p className="muted">
              {graphInfo.place_name} · {graphInfo.node_count.toLocaleString('vi-VN')} node ·{' '}
              {graphInfo.edge_count.toLocaleString('vi-VN')} cạnh
            </p>
          )}
        </header>

        <nav className="tabs" role="tablist">
          {TABS.map(({ key, label }) => (
            <button key={key} role="tab" aria-selected={tab === key} onClick={() => setTab(key)}>
              {label}
            </button>
          ))}
        </nav>

        {/* Giữ cả 2 tab trong DOM để không mất kết quả khi chuyển tab */}
        <div className="tab-panel" hidden={tab !== 'route'}>
          <ControlPanel
            algo={algo}
            onAlgoChange={setAlgo}
            canRun={Boolean(graphInfo && start && end)}
            loading={loading}
            showVisited={showVisited}
            onShowVisitedChange={setShowVisited}
            onFind={handleFind}
            onCompare={handleCompare}
            onClear={handleClear}
            hint={hint}
            error={error}
          />

          <StatsPanel results={results} />
          {results.length > 1 && <CompareChart results={results} />}
          {databaseEnabled && <HistoryPanel items={history} error={historyError} onSelect={handleHistorySelect} />}
        </div>

        <div className="tab-panel" hidden={tab !== 'benchmark'}>
          {graphInfo && <BenchmarkPanel databaseEnabled={databaseEnabled} />}
        </div>
      </aside>
    </div>
  )
}
