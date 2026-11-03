// Bản đồ Leaflet: click chọn điểm đi/đến, vẽ đường đi và các node đã duyệt
import L from 'leaflet'
import { CircleMarker, MapContainer, Marker, Polyline, Rectangle, TileLayer, useMapEvents } from 'react-leaflet'
import { ALGORITHMS } from '../constants.js'

// Dùng divIcon thay icon ảnh mặc định của Leaflet (ảnh bị mất đường dẫn khi build bằng Vite)
const pinIcon = (className) => L.divIcon({ className: `pin ${className}`, iconSize: [18, 18], iconAnchor: [9, 9] })
const START_ICON = pinIcon('pin-start')
const END_ICON = pinIcon('pin-end')

function ClickHandler({ onClick }) {
  useMapEvents({ click: (e) => onClick(e.latlng) })
  return null
}

function DraggablePin({ position, icon, title, onMove }) {
  return (
    <Marker
      position={position}
      icon={icon}
      title={title}
      draggable
      eventHandlers={{ dragend: (e) => onMove(e.target.getLatLng()) }}
    />
  )
}

export default function MapView({ graphInfo, start, end, results, showVisited, onMapClick, onStartMove, onEndMove }) {
  const [south, west, north, east] = graphInfo.bbox
  const bounds = [
    [south, west],
    [north, east],
  ]
  // Vẽ thuật toán duyệt nhiều node trước để thuật toán duyệt ít nằm đè lên trên
  const ordered = [...results].sort((a, b) => b.visited_count - a.visited_count)

  return (
    // preferCanvas: vẽ hàng nghìn node đã duyệt bằng canvas thay vì SVG cho mượt
    <MapContainer bounds={bounds} preferCanvas className="map">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Rectangle
        bounds={bounds}
        interactive={false}
        pathOptions={{ color: '#495057', weight: 1.5, dashArray: '6 6', fill: false }}
      />
      <ClickHandler onClick={onMapClick} />

      {showVisited &&
        ordered.map((r) =>
          r.visited.map((point, i) => (
            <CircleMarker
              key={`${r.algorithm}-${i}`}
              center={point}
              radius={2.5}
              interactive={false}
              pathOptions={{ stroke: false, fillColor: ALGORITHMS[r.algorithm].color, fillOpacity: 0.35 }}
            />
          )),
        )}

      {ordered.map((r, i) => (
        <Polyline
          key={r.algorithm}
          positions={r.path}
          interactive={false}
          // Khi so sánh, đường bên dưới vẽ dày hơn để vẫn thấy được nếu 2 đường trùng nhau
          pathOptions={{ color: ALGORITHMS[r.algorithm].color, weight: ordered.length > 1 && i === 0 ? 10 : 5, opacity: 0.9 }}
        />
      ))}

      {start && end && results.length > 0 && (
        // Điểm click được bắt về node gần nhất trên đồ thị: nối bằng nét đứt cho dễ thấy
        <Polyline
          positions={[
            [start, results[0].path[0]],
            [results[0].path.at(-1), end],
          ]}
          interactive={false}
          pathOptions={{ color: '#495057', weight: 2, dashArray: '4 6' }}
        />
      )}

      {start && <DraggablePin position={start} icon={START_ICON} title="Điểm đi" onMove={onStartMove} />}
      {end && <DraggablePin position={end} icon={END_ICON} title="Điểm đến" onMove={onEndMove} />}
    </MapContainer>
  )
}
