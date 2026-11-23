import brandLogo from '../assets/logo-ban-do-so-icon.png'
import { useState } from 'react'
import { login, register } from '../api/demoAuth.js'
export default function AccountDialog({ onClose, onSuccess, initialMode = 'login' }) {
  const [mode, setMode] = useState(initialMode)
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  async function submit(event) {
    event.preventDefault(); setBusy(true); setError('')
    try { const user = await (mode === 'register' ? register({ name, email, password }) : login({ email, password })); onSuccess(user) }
    catch (e) { setError(e.message) } finally { setBusy(false) }
  }
  return <div className="dialog-backdrop" onMouseDown={e => { if (e.target === e.currentTarget) onClose() }}>
    <section className="account-dialog" role="dialog" aria-modal="true" aria-label={mode === 'login' ? 'Đăng nhập' : 'Đăng ký'}>
      <button type="button" className="dialog-close" onClick={onClose} aria-label="Đóng">×</button>
      <img className="dialog-brand-logo" src={brandLogo} alt="Logo Bản đồ số" /><h2>{mode === 'login' ? 'Chào mừng trở lại' : 'Tạo tài khoản'}</h2>
      <p className="dialog-subtitle">{mode === 'login' ? 'Đăng nhập để lưu các địa điểm bạn yêu thích.' : 'Đăng ký để quản lý địa điểm yêu thích của bạn.'}</p>
      <form onSubmit={submit} className="account-form">
        {mode === 'register' && <label>Họ và tên<input autoComplete="name" required value={name} maxLength={60} onChange={e => setName(e.target.value)} placeholder="Tên của bạn" /></label>}
        <label>Email<input type="email" required autoComplete="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="ten@email.com" /></label>
        <label>Mật khẩu<input type="password" required minLength={mode === 'register' ? 8 : 1} autoComplete={mode === 'register' ? 'new-password' : 'current-password'} value={password} onChange={e => setPassword(e.target.value)} placeholder="Ít nhất 8 ký tự khi đăng ký" /></label>
        {error && <p role="alert" className="auth-error">{error}</p>}
        <button type="submit" className="primary-action" disabled={busy}>{busy ? 'Đang xử lý…' : mode === 'login' ? 'Đăng nhập' : 'Đăng ký'}</button>
      </form>
      <p className="switch-auth">{mode === 'login' ? 'Chưa có tài khoản?' : 'Đã có tài khoản?'} <button type="button" onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}>{mode === 'login' ? 'Đăng ký ngay' : 'Đăng nhập'}</button></p>
      <p className="demo-disclosure">Tài khoản được lưu cục bộ trong trình duyệt, chưa đồng bộ máy chủ.</p>
    </section>
  </div>
}
