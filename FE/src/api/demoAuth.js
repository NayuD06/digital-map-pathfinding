import { SAMPLE_ACCOUNTS } from './sampleAccounts.js'
// DEMO ONLY: identity and favorites are stored in this browser, not on the server.
const ACCOUNT_KEY = 'its-map-demo-accounts-v1'
const SESSION_KEY = 'its-map-demo-session-v1'
const FAVORITES_KEY = 'its-map-demo-favorites-v1'
const read = (key, fallback) => { try { return JSON.parse(localStorage.getItem(key)) ?? fallback } catch { return fallback } }
const write = (key, value) => localStorage.setItem(key, JSON.stringify(value))
const bytesToHex = bytes => Array.from(new Uint8Array(bytes), x => x.toString(16).padStart(2, '0')).join('')
async function derive(password, saltHex) {
  const salt = new Uint8Array(saltHex.match(/../g).map(part => parseInt(part, 16)))
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits'])
  return bytesToHex(await crypto.subtle.deriveBits({ name: 'PBKDF2', salt, iterations: 160000, hash: 'SHA-256' }, key, 256))
}
export function currentUser() { const email = sessionStorage.getItem(SESSION_KEY); if (!email) return null; const record = read(ACCOUNT_KEY, []).find(a => a.email === email); return record ? publicAccount(record) : null }
const publicAccount = a => ({ name: a.name, email: a.email, phone: a.phone || '', avatar: a.avatar || '' })
export async function register({ name, email, password }) {
  const cleanEmail = email.trim().toLowerCase()
  if (!name.trim() || !/^\S+@\S+\.\S+$/.test(cleanEmail) || password.length < 8) throw new Error('Nhập tên, email hợp lệ và mật khẩu tối thiểu 8 ký tự.')
  const accounts = read(ACCOUNT_KEY, [])
  if (accounts.some(a => a.email === cleanEmail)) throw new Error('Email này đã được đăng ký trong bản demo.')
  if (!crypto?.subtle) throw new Error('Cần mở ứng dụng qua localhost hoặc HTTPS để đăng ký.')
  const salt = bytesToHex(crypto.getRandomValues(new Uint8Array(16)))
  accounts.push({ name: name.trim(), email: cleanEmail, salt, hash: await derive(password, salt) })
  write(ACCOUNT_KEY, accounts)
  sessionStorage.setItem(SESSION_KEY, cleanEmail)
  return publicAccount(accounts[accounts.length - 1])
}
export async function login({ email, password }) {
  // Bảo đảm tài khoản mẫu đã khởi tạo xong kể cả khi người dùng đăng nhập
  // ngay sau khi trang mở; không phụ thuộc vào useEffect trong App.jsx.
  await ensureSampleAccounts()
  const cleanEmail = email.trim().toLowerCase()
  let user = read(ACCOUNT_KEY, []).find(a => a.email === cleanEmail)
  // Sửa dữ liệu mẫu của những bản frontend trước: chỉ đồng bộ đúng tài
  // khoản mẫu khi nhập chính mật khẩu thử, không sửa tài khoản khác.
  const sample = SAMPLE_ACCOUNTS.find(a => a.email === cleanEmail)
  if (sample && password === sample.password && (!user || !user.salt || !user.hash || await derive(password, user.salt) !== user.hash)) {
    const accounts = read(ACCOUNT_KEY, [])
    user = accounts.find(a => a.email === cleanEmail)
    const salt = bytesToHex(crypto.getRandomValues(new Uint8Array(16)))
    const hash = await derive(password, salt)
    if (user) Object.assign(user, { salt, hash })
    else { user = { name: sample.name, email: sample.email, phone: sample.phone, avatar: '', salt, hash }; accounts.push(user) }
    write(ACCOUNT_KEY, accounts)
  }
  if (!user || !user.salt || !user.hash || await derive(password, user.salt) !== user.hash) throw new Error('Email hoặc mật khẩu không đúng.')
  sessionStorage.setItem(SESSION_KEY, user.email)
  return publicAccount(user)
}
export function logout() { sessionStorage.removeItem(SESSION_KEY) }
export function listFavorites(email) { return read(FAVORITES_KEY, {})[email] || [] }
export function addFavorite(email, entry) {
  if (!email) throw new Error('Vui lòng đăng nhập trước khi lưu địa điểm yêu thích.')
  const all = read(FAVORITES_KEY, {})
  const current = all[email] || []
  if (current.some(item => Math.abs(item.lat - entry.lat) < 0.000001 && Math.abs(item.lng - entry.lng) < 0.000001)) return current
  all[email] = [{ ...entry, id: crypto.randomUUID?.() || String(Date.now()) }, ...current]
  write(FAVORITES_KEY, all)
  return all[email]
}
export function deleteFavorite(email, id) { const all = read(FAVORITES_KEY, {}); all[email] = (all[email] || []).filter(item => item.id !== id); write(FAVORITES_KEY, all); return all[email] }

// Đồng bộ tài khoản thử khi khởi động. Chỉ cập nhật mật khẩu mẫu một lần
// theo phiên bản để giữ nguyên hồ sơ và danh sách yêu thích của tài khoản.
const SAMPLE_VERSION_KEY = 'its-map-demo-sample-version'
const SAMPLE_VERSION = 'password-123456789-v2'
export async function ensureSampleAccounts() {
  const accounts = read(ACCOUNT_KEY, [])
  const mustSyncPassword = localStorage.getItem(SAMPLE_VERSION_KEY) !== SAMPLE_VERSION
  let changed = false
  for (const demo of SAMPLE_ACCOUNTS) {
    const existing = accounts.find(a => a.email === demo.email)
    if (existing && !mustSyncPassword) continue
    const salt = bytesToHex(crypto.getRandomValues(new Uint8Array(16)))
    const hash = await derive(demo.password, salt)
    if (existing) {
      // Không đụng đến tên, email, avatar hoặc số điện thoại người dùng đã sửa.
      existing.salt = salt
      existing.hash = hash
    } else {
      accounts.push({ name: demo.name, email: demo.email, phone: demo.phone, avatar: '', salt, hash })
    }
    changed = true
  }
  if (changed) write(ACCOUNT_KEY, accounts)
  localStorage.setItem(SAMPLE_VERSION_KEY, SAMPLE_VERSION)
}
export function updateProfile({ name, phone, avatar }) {
  const current = currentUser()
  if (!current) throw new Error('Vui lòng đăng nhập.')
  const accounts = read(ACCOUNT_KEY, [])
  const account = accounts.find(a => a.email === current.email)
  if (!account) throw new Error('Không tìm thấy tài khoản.')
  if (!name.trim()) throw new Error('Tên không được để trống.')
  if (phone && !/^[+\d() .-]{8,20}$/.test(phone)) throw new Error('Số điện thoại không hợp lệ.')
  Object.assign(account, { name: name.trim(), phone: phone.trim(), avatar: avatar || '' })
  write(ACCOUNT_KEY, accounts)
  return publicAccount(account)
}
export async function changeEmail(newEmail) {
  const current = currentUser()
  if (!current) throw new Error('Vui lòng đăng nhập.')
  const email = newEmail.trim().toLowerCase()
  if (!/^\S+@\S+\.\S+$/.test(email)) throw new Error('Email không hợp lệ.')
  const accounts = read(ACCOUNT_KEY, [])
  if (accounts.some(a => a.email === email && a.email !== current.email)) throw new Error('Email đã được sử dụng.')
  const account = accounts.find(a => a.email === current.email)
  if (!account) throw new Error('Không tìm thấy tài khoản.')
  account.email = email
  write(ACCOUNT_KEY, accounts)
  const all = read(FAVORITES_KEY, {})
  all[email] = all[current.email] || []
  if (email !== current.email) delete all[current.email]
  write(FAVORITES_KEY, all)
  sessionStorage.setItem(SESSION_KEY, email)
  return publicAccount(account)
}

export function updateFavoriteDetails(email, id, details) {
  const all = read(FAVORITES_KEY, {})
  all[email] = (all[email] || []).map(f => f.id === id ? { ...f, name: details.name, address: details.address } : f)
  write(FAVORITES_KEY, all)
  return all[email]
}
