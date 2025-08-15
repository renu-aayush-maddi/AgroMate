// import React, { useState } from 'react'
// import { useNavigate } from 'react-router-dom'
// import axios from 'axios'
// import { API_BASE } from '../api.js'
// import { useAuth } from '../state/AuthContext.jsx'

// export default function Login() {
//   const nav = useNavigate()
//   const { setToken } = useAuth()
//   const [email, setEmail] = useState('')
//   const [password, setPassword] = useState('')
//   const [err, setErr] = useState('')

//   const submit = async (e) => {
//     e.preventDefault()
//     setErr('')
//     try {
//       const res = await axios.post(`${API_BASE}/login`, { email, password })
//       setToken(res.data.access_token)
//       nav('/')
//     } catch (e) {
//       setErr(e?.response?.data?.detail || e.message)
//     }
//   }

//   return (
//     <div style={styles.wrap}>
//       <h2>Login</h2>
//       {err && <div style={styles.err}>{err}</div>}
//       <form onSubmit={submit} style={styles.form}>
//         <input placeholder="Email" value={email} onChange={(e)=>setEmail(e.target.value)} style={styles.input} />
//         <input placeholder="Password" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} style={styles.input} />
//         <button style={styles.btn}>Login</button>
//       </form>
//     </div>
//   )
// }

// const styles = {
//   wrap: { padding: 24, color: '#e7eef7' },
//   form: { display: 'flex', flexDirection: 'column', gap: 8, maxWidth: 360 },
//   input: { padding: '10px 12px', borderRadius: 8, border: '1px solid #1f2b3b', background: '#0f1b2d', color: '#e7eef7' },
//   btn: { padding: '10px 16px', borderRadius: 8, border: 'none', background: '#7aa2f7', color: '#0b1726', fontWeight: 700, cursor: 'pointer' },
//   err: { color: '#ffb4a9', marginBottom: 8 },
// }


import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { API_BASE } from '../api.js'
import { useAuth } from '../state/AuthContext.jsx'

export default function Login() {
  const nav = useNavigate()
  const { setToken } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [err, setErr] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setErr('')
    setIsLoading(true)
    try {
      const res = await axios.post(`${API_BASE}/login`, { email, password })
      setToken(res.data.access_token)
      nav('/')
    } catch (e) {
      setErr(e?.response?.data?.detail || e.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.bgPattern}></div>
      <div style={styles.bgGradient}></div>
      <div style={styles.leafTop}>🌿</div>
      <div style={styles.leafBottom}>🌾</div>
      <div style={styles.sun}>☀️</div>

      <div style={styles.loginCard}>
        <div style={styles.header}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>🚜</span>
            <h1 style={styles.title}>FarmConnect</h1>
          </div>
          <p style={styles.subtitle}>Welcome back to your farm dashboard</p>
        </div>

        {err && (
          <div style={styles.errorBox}>
            <span style={styles.errorIcon}>⚠️</span>
            {err}
          </div>
        )}

        <form style={styles.form} onSubmit={submit}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>📧 Email</label>
            <input
              type="email"
              placeholder="your@farm-email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={styles.input}
            />
          </div>

          <div style={styles.inputGroup}>
            <label style={styles.label}>🔒 Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
            />
          </div>

          <button
            type="submit"
            style={{
              ...styles.submitBtn,
              ...(isLoading ? styles.submitBtnLoading : {})
            }}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span style={styles.spinner}></span>
                Signing In...
              </>
            ) : (
              <>
                🌱 Sign In to Farm
              </>
            )}
          </button>
        </form>

        <div style={styles.footer}>
          <p style={styles.footerText}>
            New to farming? <span style={styles.link}>Start your journey</span>
          </p>
          <div style={styles.features}>
            <span style={styles.feature}>🌾 Crop Management</span>
            <span style={styles.feature}>📊 Analytics</span>
            <span style={styles.feature}>🤝 Community</span>
          </div>
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    minHeight: '100vh',
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
    overflow: 'hidden',
    background: 'linear-gradient(135deg, #4a7c59 0%, #6b8e23 50%, #8fbc8f 100%)',
  },
  
  bgPattern: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundImage: `
      radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 2px, transparent 2px),
      radial-gradient(circle at 75% 75%, rgba(255,255,255,0.1) 1px, transparent 1px)
    `,
    backgroundSize: '60px 60px',
    animation: 'float 20s ease-in-out infinite',
  },
  
  bgGradient: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'radial-gradient(ellipse at center, rgba(255,255,255,0.1) 0%, transparent 70%)',
  },
  
  leafTop: {
    position: 'absolute',
    top: '10%',
    left: '10%',
    fontSize: '3rem',
    opacity: 0.3,
    animation: 'sway 4s ease-in-out infinite',
    zIndex: 1,
  },
  
  leafBottom: {
    position: 'absolute',
    bottom: '15%',
    right: '15%',
    fontSize: '2.5rem',
    opacity: 0.3,
    animation: 'sway 4s ease-in-out infinite reverse',
    zIndex: 1,
  },
  
  sun: {
    position: 'absolute',
    top: '5%',
    right: '10%',
    fontSize: '2rem',
    opacity: 0.4,
    animation: 'glow 3s ease-in-out infinite alternate',
    zIndex: 1,
  },
  
  loginCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    backdropFilter: 'blur(20px)',
    borderRadius: '24px',
    padding: '40px',
    maxWidth: '480px',
    width: '100%',
    boxShadow: `
      0 20px 40px rgba(0,0,0,0.1),
      0 10px 20px rgba(0,0,0,0.05),
      inset 0 1px 0 rgba(255,255,255,0.8)
    `,
    border: '1px solid rgba(255,255,255,0.2)',
    position: 'relative',
    zIndex: 2,
    animation: 'slideUp 0.6s ease-out',
  },
  
  header: {
    textAlign: 'center',
    marginBottom: '32px',
  },
  
  logo: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '12px',
    marginBottom: '8px',
  },
  
  logoIcon: {
    fontSize: '2.5rem',
    animation: 'bounce 2s ease-in-out infinite',
  },
  
  title: {
    fontSize: '2.2rem',
    fontWeight: '800',
    margin: 0,
    background: 'linear-gradient(135deg, #2d5016 0%, #4a7c59 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
  },
  
  subtitle: {
    color: '#5a6c57',
    fontSize: '1rem',
    margin: '8px 0 0 0',
    fontWeight: '500',
  },
  
  errorBox: {
    backgroundColor: '#fef2f2',
    border: '1px solid #fecaca',
    borderRadius: '12px',
    padding: '12px 16px',
    marginBottom: '24px',
    color: '#dc2626',
    fontSize: '0.9rem',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontWeight: '500',
  },
  
  errorIcon: {
    fontSize: '1.1rem',
  },
  
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '24px',
  },
  
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  
  label: {
    fontSize: '0.9rem',
    fontWeight: '600',
    color: '#374151',
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  },
  
  input: {
    padding: '14px 16px',
    borderRadius: '12px',
    border: '2px solid #e5e7eb',
    backgroundColor: '#fafafa',
    fontSize: '1rem',
    color: '#374151',
    outline: 'none',
    transition: 'all 0.2s ease',
    fontFamily: 'inherit',
  },
  
  submitBtn: {
    padding: '16px 24px',
    borderRadius: '12px',
    border: 'none',
    background: 'linear-gradient(135deg, #4a7c59 0%, #6b8e23 100%)',
    color: 'white',
    fontSize: '1.1rem',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    boxShadow: '0 4px 12px rgba(74, 124, 89, 0.3)',
    marginTop: '8px',
  },
  
  submitBtnLoading: {
    background: 'linear-gradient(135deg, #9ca3af 0%, #6b7280 100%)',
    cursor: 'not-allowed',
  },
  
  spinner: {
    width: '16px',
    height: '16px',
    border: '2px solid rgba(255,255,255,0.3)',
    borderTop: '2px solid white',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  
  footer: {
    textAlign: 'center',
    marginTop: '32px',
    paddingTop: '24px',
    borderTop: '1px solid #e5e7eb',
  },
  
  footerText: {
    color: '#6b7280',
    fontSize: '0.9rem',
    margin: '0 0 16px 0',
  },
  
  link: {
    color: '#4a7c59',
    textDecoration: 'none',
    fontWeight: '600',
    cursor: 'pointer',
  },
  
  features: {
    display: 'flex',
    justifyContent: 'center',
    gap: '16px',
    flexWrap: 'wrap',
  },
  
  feature: {
    fontSize: '0.8rem',
    color: '#9ca3af',
    padding: '4px 8px',
    backgroundColor: '#f9fafb',
    borderRadius: '6px',
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
  },
}

// Add CSS animations
const styleSheet = document.createElement('style')
styleSheet.textContent = `
  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
  }
  
  @keyframes sway {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(2deg); }
    75% { transform: rotate(-2deg); }
  }
  
  @keyframes glow {
    from { opacity: 0.4; }
    to { opacity: 0.8; }
  }
  
  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-5px); }
    60% { transform: translateY(-3px); }
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  input:focus {
    border-color: #4a7c59 !important;
    box-shadow: 0 0 0 3px rgba(74, 124, 89, 0.1) !important;
    background-color: white !important;
  }
  
  button:hover:not(:disabled) {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(74, 124, 89, 0.4) !important;
  }
  
  button:active:not(:disabled) {
    transform: translateY(0) !important;
  }
  
  .link:hover {
    text-decoration: underline !important;
  }
`
document.head.appendChild(styleSheet)