import { useEffect, useRef, useState } from 'react'
import { compareRoutes, findRoute, getGraphInfo } from './api/client.js'
import MapView from './components/MapView.jsx'
import AccountDialog from './components/AccountDialog.jsx'
import AddressSearch from './components/AddressSearch.jsx'
import ProfileDialog from './components/ProfileDialog.jsx'
import { resolvePlace, fromSearch } from './api/placeLookup.js'
import { currentUser, logout, listFavorites, addFavorite, deleteFavorite, ensureSampleAccounts, updateFavoriteDetails } from './api/demoAuth.js'
import brandLogo from './assets/logo-ban-do-so-icon.png'
import { ALGORITHMS, formatDistance } from './constants.js'

// TV4 giữ các state và bố cục; UI điều khiển dưới đây là bản tạm chạy demo.
// Khi TV5 hoàn thành ControlPanel/StatsPanel/CompareChart, thay phần UI tạm bằng component của TV5.
export default function App() {
  const [user, setUser] = useState(() => currentUser())
  const [authOpen, setAuthOpen] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const [placeDetails, setPlaceDetails] = useState(null)
  const [authMode, setAuthMode] = useState('login')
  const [favoritesOpen, setFavoritesOpen] = useState(false)
  const [favorites, setFavorites] = useState(() => currentUser() ? listFavorites(currentUser().email) : [])
  const [placeTarget, setPlaceTarget] = useState(null)
  const [startInfo, setStartInfo] = useState(null)
  const [endInfo, setEndInfo] = useState(null)
  const startLookup = useRef(0)
  const endLookup = useRef(0)
  const [notice, setNotice] = useState('')
  const [graphInfo, setGraphInfo] = useState(null)
  const [start, setStart] = useState(null)
  const [end, setEnd] = useState(null)
  const [algo, setAlgo] = useState('astar')
  const [results, setResults] = useState([])
  const [showVisited, setShowVisited] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [resetCount, setResetCount] = useState(0)
  // Mỗi yêu cầu có một phiên bản để phản hồi cũ không ghi đè kết quả mới.
  const requestId = useRef(0)
  const mockMode = import.meta.env.VITE_USE_MOCK === 'true'

  useEffect(() => { ensureSampleAccounts().catch(console.error) }, [])
  useEffect(() => {
    if (!favoritesOpen || !user) return
    let cancelled = false
    // Nâng cấp địa điểm đã lưu ở bản cũ (chỉ có tên/tọa độ) sang tên và địa chỉ.
    async function migrate() {
      for (const favorite of listFavorites(user.email)) {
        if (cancelled) return
        const oldCoordinate = /-?\d{1,3}\.\d{4,}\s*,\s*-?\d{1,3}\.\d{4,}/.test(favorite.name || '')
        if (favorite.address && !oldCoordinate) continue
        const place = await resolvePlace({ lat: favorite.lat, lng: favorite.lng })
        if (!cancelled) setFavorites(updateFavoriteDetails(user.email, favorite.id, place))
      }
    }
    migrate()
    return () => { cancelled = true }
  }, [favoritesOpen, user])
  useEffect(() => {
    let active = true
    getGraphInfo().then(value => { if (active) setGraphInfo(value) }).catch(e => { if (active) setError(e.message) })
    return () => { active = false }
  }, [])
  function cancelPendingRoute() {
    requestId.current += 1
    setResults([])
    setLoading(false)
    setError('')
  }
  function resolveFor(point, kind) {
    const ref = kind === 'start' ? startLookup : endLookup
    const setter = kind === 'start' ? setStartInfo : setEndInfo
    const version = ++ref.current
    setter(fromSearch(point))
    if (point.name && point.address) return
    resolvePlace(point).then(place => { if (ref.current === version) setter(place) })
  }
  function selectMapPoint(point) {
    cancelPendingRoute()
    if (!start || end) { setStart(point); resolveFor(point, 'start'); setEnd(null); setEndInfo(null); endLookup.current++ }
    else { setEnd(point); resolveFor(point, 'end') }
  }
  async function requestRoute(from, to, compare, algorithm) {
    if (!from || !to) return
    const id = ++requestId.current
    setLoading(true)
    setError('')
    setResults([]) // Không vẽ tuyến cũ khi ghim đã đổi vị trí.
    try {
      const value = compare
        ? (await compareRoutes(from, to)).results
        : [await findRoute(algorithm, from, to)]
      if (id === requestId.current) setResults(value)
    } catch (e) {
      if (id === requestId.current) setError(e.message || 'Không tìm được đường')
    } finally {
      if (id === requestId.current) setLoading(false)
    }
  }
  function moveStart(point) {
    resolveFor(point, 'start')
    const shouldReroute = results.length > 0 || loading
    const compare = results.length === 2 || (loading && currentCompare.current)
    setStart(point)
    if (shouldReroute && end) { currentCompare.current = compare; requestRoute(point, end, compare, algo) }
    else cancelPendingRoute()
  }
  function moveEnd(point) {
    resolveFor(point, 'end')
    const shouldReroute = results.length > 0 || loading
    const compare = results.length === 2 || (loading && currentCompare.current)
    setEnd(point)
    if (shouldReroute && start) { currentCompare.current = compare; requestRoute(start, point, compare, algo) }
    else cancelPendingRoute()
  }
  const currentCompare = useRef(false)
  function run(compare = false) {
    if (!start || !end || loading) return
    currentCompare.current = compare
    requestRoute(start, end, compare, algo)
  }
  function clearRoute() {
    cancelPendingRoute()
    setStart(null)
    setEnd(null)
    setStartInfo(null)
    setEndInfo(null)
    startLookup.current++
    endLookup.current++
    currentCompare.current = false
  }
  function choosePlace(place) {
    const selected = fromSearch({ ...place, display_name: place.address || place.name })
    setPlaceTarget({ lat: selected.lat, lng: selected.lng, key: Date.now() })
    selectMapPoint(selected)
  }
  function openLogin() { setAuthMode('login'); setAuthOpen(true) }
  async function saveFavorite(point, tag) {
    if (!point) { setNotice('Hãy chọn địa điểm trên bản đồ trước.'); return }
    if (!user) { setNotice('Đăng nhập để lưu địa điểm yêu thích.'); openLogin(); return }
    setNotice('Đang lấy địa chỉ để lưu…')
    const info = (tag === 'Điểm đi' ? startInfo : endInfo) || await resolvePlace(point)
    const detail = info.address?.startsWith('Chưa') ? await resolvePlace(point) : info
    const current = addFavorite(user.email, { lat: point.lat, lng: point.lng, name: detail.name || 'Vị trí đã chọn', address: detail.address || 'Chưa có địa chỉ chi tiết' })
    setFavorites(current)
    setNotice('Đã lưu địa điểm vào danh sách yêu thích.')
  }
  function doLogout() {
    logout(); setUser(null); setFavorites([]); setFavoritesOpen(false); setProfileOpen(false); setNotice('Đã đăng xuất.')
  }
  const canRun = Boolean(start && end && graphInfo)
  const single = results.length === 1 ? results[0] : null
  const summary = results.length > 0
  return <div className="app">
    <main className="map-area" aria-label="Bản đồ tương tác">
      {graphInfo ? <MapView graphInfo={graphInfo} start={start} end={end} results={results} showVisited={showVisited}
        onMapClick={selectMapPoint} onStartMove={moveStart} onEndMove={moveEnd} resetCount={resetCount} placeTarget={placeTarget} />
        : <div className="map-fallback">{error || 'Đang tải dữ liệu bản đồ…'}</div>}
      <div className="map-account-actions">
        <button type="button" onClick={() => { if (!user) { setNotice('Bạn cần đăng nhập để sử dụng địa điểm yêu thích.'); openLogin() } else setFavoritesOpen(true) }}>☆ Yêu thích</button>
        {user ? <><button type="button" className="profile-trigger" title="Chỉnh sửa tài khoản" onClick={() => setProfileOpen(true)}>{user.avatar ? <img src={user.avatar} alt="Avatar" /> : <span className="avatar-initial">{user.name.slice(0,1).toUpperCase()}</span>}<span>{user.name}</span></button><button type="button" onClick={doLogout}>Đăng xuất</button></> : <><button type="button" onClick={openLogin}>Đăng nhập</button><button type="button" className="join-action" onClick={() => { setAuthMode('register'); setAuthOpen(true) }}>Đăng ký</button></>}
      </div>
      <div className="map-location">✦ Việt Nam <span>/</span> TP. Hồ Chí Minh <span>/</span> <strong>Quận 1</strong></div>
      <div className="map-top-actions"><button type="button" onClick={() => setResetCount(n => n + 1)}>⌖ Về khu vực bản đồ</button></div>
      <div className="map-bottom-note">© OpenStreetMap contributors</div>

      {mockMode && results.some(r => r.route_source === 'straight-fallback') && <div className="mock-route-note">Không lấy được tuyến đường phố · Nét đứt chỉ nối hai vị trí</div>}
      {results.length === 2 && <div className="comparison-legend">{results.map(r => <span key={r.algorithm}><i style={{ background: ALGORITHMS[r.algorithm]?.color }} /> {ALGORITHMS[r.algorithm]?.label || r.algorithm}</span>)} <small>Cùng cặp điểm A/B</small></div>}
    </main>
    <aside className="sidebar">
      <header className="brand">
        <img className="brand-logo" src={brandLogo} alt="Biểu tượng Bản đồ số" />
        <div className="brand-content">
          <div className="brand-title-row"><span className="brand-title">Bản đồ số</span></div>
          <p className="brand-slogan">Mỗi hành trình, một khởi đầu.</p>
        </div>
      </header>
<div className="sidebar-heading">
  <h1>Tìm đường</h1>
</div>      <AddressSearch onChoose={choosePlace} />
      {notice && <div className="notice" role="status">{notice} <button type="button" aria-label="Đóng thông báo" onClick={() => setNotice('')}>×</button></div>}
      <section className="point-section">
        <label className="field-label" htmlFor="from-view">ĐIỂM ĐI</label>
        <div className={`point-field ${!start ? 'field-active' : ''}`} id="from-view"><b className="point-tag start-tag">A</b><button type="button" className="place-summary" disabled={!start} onClick={() => setPlaceDetails(startInfo)}><strong>{start ? (startInfo?.name || 'Đang xác định địa điểm…') : 'Chọn trên bản đồ'}</strong>{start && <small>{startInfo?.address || 'Đang lấy địa chỉ…'}</small>}</button><button type="button" className="favorite-star" title="Lưu điểm đi" aria-label="Lưu điểm đi vào yêu thích" onClick={() => saveFavorite(start, 'Điểm đi')}>☆</button></div>
        <label className="field-label" htmlFor="to-view">ĐIỂM ĐẾN</label>
        <div className="point-field" id="to-view"><b className="point-tag end-tag">B</b><button type="button" className="place-summary" disabled={!end} onClick={() => setPlaceDetails(endInfo)}><strong>{end ? (endInfo?.name || 'Đang xác định địa điểm…') : 'Chọn trên bản đồ'}</strong>{end && <small>{endInfo?.address || 'Đang lấy địa chỉ…'}</small>}</button><button type="button" className="favorite-star" title="Lưu điểm đến" aria-label="Lưu điểm đến vào yêu thích" onClick={() => saveFavorite(end, 'Điểm đến')}>☆</button></div>
        <p className="selection-hint">{!start ? 'Bấm lên bản đồ để chọn điểm đi' : !end ? 'Đã chọn điểm đi · Bấm để chọn điểm đến' : 'Đã chọn 2 điểm · Có thể kéo ghim để điều chỉnh'}</p>
      </section>
      <section className="algorithm-section"><h2>Thuật toán</h2><div className="algorithm-tabs">{Object.entries(ALGORITHMS).map(([key, data]) =>
        <button type="button" key={key} className={key === algo ? 'active' : ''} onClick={() => { setAlgo(key); cancelPendingRoute() }} aria-pressed={key === algo}>{data.label}</button>)}</div></section>
      <div className="action-area"><button className="primary-action" onClick={() => run(false)} disabled={!canRun || loading}>{loading ? 'Đang tìm đường…' : '⌁  Tìm đường'}</button>
        <div className="action-secondary"><button onClick={() => run(true)} disabled={!canRun || loading}>◇ So sánh cách tìm đường</button><button onClick={clearRoute} disabled={loading || (!start && !end)}>Xóa tuyến</button></div></div>
      {error && <div className="error" role="alert">{error}</div>}
      {summary && <section className="results-section"><div className="result-title">✓ Đã tìm thấy tuyến đường</div>
        {single && <div className="results-card"><div><span>Thuật toán vừa chạy</span><strong>{ALGORITHMS[single.algorithm]?.label || single.algorithm}</strong></div><div><span>Độ dài tuyến</span><strong className="distance-emphasis">{formatDistance(single.distance_m)}</strong></div>{!mockMode && <><div><span>Thời gian chạy</span><strong>{Number(single.runtime_ms).toFixed(2)} ms</strong></div><div><span>Số nút đã duyệt</span><strong>{Number(single.visited_count).toLocaleString('vi-VN')}</strong></div></>}</div>}
        {results.length === 2 && <div className="compare-cards">{results.map(r => <div className="compare-card" key={r.algorithm}><h3 style={{ borderColor: ALGORITHMS[r.algorithm]?.color }}>{ALGORITHMS[r.algorithm]?.label || r.algorithm}</h3><p>Độ dài: <strong>{formatDistance(r.distance_m)}</strong></p>{!mockMode && <><p>Thời gian: <strong>{Number(r.runtime_ms).toFixed(2)} ms</strong></p><p>Nút đã duyệt: <strong>{Number(r.visited_count).toLocaleString('vi-VN')}</strong></p></>}</div>)}</div>}
        {!mockMode && <label className="visited-control"><input type="checkbox" checked={showVisited} onChange={e => setShowVisited(e.target.checked)} /> Xem số nút đã duyệt trên bản đồ</label>}
      {mockMode && <p className="route-disclosure">Tuyến tham khảo từ OSRM công khai; kết quả chưa phải thuật toán của nhóm.</p>}
      </section>}
      {!summary && <div className="tip">✧ {canRun ? 'Đã chọn hai điểm. Nhấn Tìm đường để xem kết quả.' : 'Chọn điểm đi và điểm đến trên bản đồ.'}</div>}
      <footer className="sidebar-footer">Khảo sát bản đồ số & thuật toán tìm đường · ITS</footer>
    </aside>
    {authOpen && <AccountDialog initialMode={authMode} onClose={() => setAuthOpen(false)} onSuccess={account => { setUser(account); setFavorites(listFavorites(account.email)); setAuthOpen(false); setNotice(`Xin chào ${account.name}!`) }} />}
    {favoritesOpen && user && <div className="dialog-backdrop" onMouseDown={e => { if (e.target === e.currentTarget) setFavoritesOpen(false) }}><section className="account-dialog favorites-dialog" role="dialog" aria-modal="true" aria-label="Địa điểm yêu thích">
      <button type="button" className="dialog-close" aria-label="Đóng" onClick={() => setFavoritesOpen(false)}>×</button>
      <h2>☆ Địa điểm yêu thích</h2><p className="dialog-subtitle">Danh sách đã lưu của {user.name}</p>
      {favorites.length ? <div className="favorite-list">{favorites.map(f => <div className="favorite-item" key={f.id}><button type="button" onClick={() => { choosePlace(f); setFavoritesOpen(false) }}><strong>{f.name}</strong><small>{f.address || 'Chưa có địa chỉ chi tiết'}</small></button><button type="button" className="remove-favorite" title="Xóa khỏi yêu thích" onClick={() => setFavorites(deleteFavorite(user.email, f.id))}>×</button></div>)}</div> : <p className="empty-favorites">Chưa có địa điểm nào. Chọn điểm A hoặc B rồi nhấn ☆ để lưu.</p>}
    </section></div>}
    {profileOpen && user && <ProfileDialog user={user} onClose={() => setProfileOpen(false)} onSave={updated => { setUser(updated); setFavorites(listFavorites(updated.email)); setProfileOpen(false); setNotice('Đã cập nhật thông tin tài khoản.') }} />}
    {placeDetails && <div className="dialog-backdrop" onMouseDown={e => { if (e.target === e.currentTarget) setPlaceDetails(null) }}><section className="account-dialog place-detail-dialog" role="dialog" aria-modal="true" aria-label="Chi tiết địa điểm"><button type="button" className="dialog-close" onClick={() => setPlaceDetails(null)}>×</button><h2>{placeDetails.name}</h2><p className="dialog-subtitle">{placeDetails.address}</p><button type="button" className="primary-action" onClick={() => setPlaceDetails(null)}>Đóng</button></section></div>}
  </div>
}
