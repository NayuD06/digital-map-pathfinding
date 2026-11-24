import { useState } from 'react'
import { changeEmail, updateProfile } from '../api/demoAuth.js'
export default function ProfileDialog({ user, onClose, onSave }) {
  const [name,setName]=useState(user.name)
  const [email,setEmail]=useState(user.email)
  const [phone,setPhone]=useState(user.phone || '')
  const [avatar,setAvatar]=useState(user.avatar || '')
  const [error,setError]=useState('')
  const [busy,setBusy]=useState(false)
  function chooseImage(e) {
    const file=e.target.files?.[0]
    if (!file) return
    if (!['image/png','image/jpeg','image/webp'].includes(file.type)) { setError('Chỉ nhận PNG, JPG hoặc WebP.'); return }
    if (file.size > 350000) { setError('Ảnh quá lớn. Chọn ảnh dưới 350 KB.'); return }
    const reader=new FileReader()
    reader.onload=()=>{ setAvatar(String(reader.result)); setError('') }
    reader.readAsDataURL(file)
  }
  async function save(e) {
    e.preventDefault();setBusy(true);setError('')
    try {
      updateProfile({ name, phone, avatar })
      const updated=await changeEmail(email)
      onSave(updated)
    } catch(ex) { setError(ex.message) } finally { setBusy(false) }
  }
  return <div className="dialog-backdrop" onMouseDown={e=>{if(e.target===e.currentTarget)onClose()}}>
    <section className="account-dialog profile-dialog" role="dialog" aria-modal="true" aria-label="Chỉnh sửa tài khoản">
      <button className="dialog-close" type="button" onClick={onClose} aria-label="Đóng">×</button>
      <h2>Thông tin tài khoản</h2><p className="dialog-subtitle">Chỉnh sửa thông tin cá nhân và ảnh đại diện.</p>
      <form onSubmit={save} className="account-form">
        <div className="avatar-editor">{avatar?<img src={avatar} alt="Ảnh đại diện"/>:<span>{name.slice(0,1).toUpperCase()}</span>}<label className="avatar-upload">Thay ảnh đại diện<input type="file" accept="image/png,image/jpeg,image/webp" onChange={chooseImage}/></label></div>
        <label>Họ và tên<input required maxLength="60" value={name} onChange={e=>setName(e.target.value)}/></label>
        <label>Email<input type="email" required value={email} onChange={e=>setEmail(e.target.value)}/></label>
        <label>Số điện thoại<input type="tel" value={phone} onChange={e=>setPhone(e.target.value)} placeholder="Nhập số điện thoại"/></label>
        {error&&<p className="auth-error" role="alert">{error}</p>}
        <button className="primary-action" disabled={busy} type="submit">{busy?'Đang lưu…':'Lưu thay đổi'}</button>
      </form>
      <p className="profile-hint">Tài khoản thử chỉ lưu trên trình duyệt này, chưa đồng bộ máy chủ.</p>
    </section>
  </div>
}
