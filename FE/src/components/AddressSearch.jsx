import { useRef, useState } from 'react'
const names = [
  { display_name: 'Chợ Bến Thành, Quận 1, TP. Hồ Chí Minh', lat: '10.7725', lon: '106.6980' },
  { display_name: 'Nhà thờ Đức Bà Sài Gòn, Quận 1', lat: '10.7798', lon: '106.6990' },
  { display_name: 'Dinh Độc Lập, Quận 1, TP. Hồ Chí Minh', lat: '10.7770', lon: '106.6953' },
  { display_name: 'Nhà hát Thành phố Hồ Chí Minh, Quận 1', lat: '10.7767', lon: '106.7031' },
]
export default function AddressSearch({ onChoose }) {
  const lastSearch = useRef(0)
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  async function search(e) {
    e.preventDefault(); if (!query.trim() || loading) return
    if (Date.now() - lastSearch.current < 1200) { setError('Vui lòng đợi ít nhất 1 giây giữa hai lần tìm kiếm.'); return }
    lastSearch.current = Date.now()
    setLoading(true); setError(''); setResults([])
    try {
      // Manual submit ONLY. The public Nominatim service forbids autocomplete requests.
      const url = new URL('https://nominatim.openstreetmap.org/search')
      url.search = new URLSearchParams({ q: query.trim(), format: 'jsonv2', limit: '5', addressdetails: '1', 'accept-language': 'vi', countrycodes: 'vn' })
      const response = await fetch(url, { headers: { Accept: 'application/json' } })
      if (!response.ok) throw new Error('Dịch vụ tìm kiếm địa chỉ đang bận. Vui lòng thử lại sau.')
      const data = await response.json()
      setResults(data)
      if (!data.length) setError('Không tìm thấy địa chỉ phù hợp tại Việt Nam.')
    } catch (err) { setError(err.message || 'Không thể tìm địa chỉ.') }
    finally { setLoading(false) }
  }
  return <section className="address-search"><h2>⌕ Tìm kiếm địa chỉ</h2>
    <form className="search-form" onSubmit={search}><input aria-label="Nhập địa chỉ" value={query} onChange={e => setQuery(e.target.value)} placeholder="Ví dụ: Chợ Bến Thành" /><button disabled={loading} type="submit">{loading ? 'Đang tìm…' : 'Tìm'}</button></form>
    {error && <p className="search-error" role="status">{error}</p>}
    {!!results.length && <div className="search-results">{results.map((place, i) => <button type="button" key={`${place.lat}-${place.lon}-${i}`} onClick={() => { onChoose({ lat: Number(place.lat), lng: Number(place.lon), name: place.display_name.split(',')[0], address: place.display_name }); setResults([]) }}><span>⌖</span><span className="search-result-text"><strong>{place.name || place.display_name.split(',')[0]}</strong><small>{place.display_name}</small></span></button>)}</div>}
    <div className="quick-places">{names.map(place => <button type="button" key={place.display_name} onClick={() => onChoose({ lat: Number(place.lat), lng: Number(place.lon), name: place.display_name.split(',')[0], address: place.display_name })}>{place.display_name.split(',')[0]}</button>)}</div>
    <small>Dữ liệu địa chỉ: © OpenStreetMap · <a href="https://operations.osmfoundation.org/policies/nominatim/" target="_blank" rel="noreferrer">Quy định Nominatim</a>. Chỉ tìm khi bấm nút.</small>
  </section>
}
