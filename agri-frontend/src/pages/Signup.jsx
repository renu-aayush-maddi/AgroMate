import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { API_BASE } from '../api.js'
import { useAuth } from '../state/AuthContext.jsx'

export default function Signup() {
  const nav = useNavigate()
  const { setToken } = useAuth()
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [err, setErr] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    setErr('')
    try {
      const res = await axios.post(`${API_BASE}/signup`, { email, password, name })
      setToken(res.data.access_token)
      nav('/')
    } catch (e) {
      setErr(e?.response?.data?.detail || e.message)
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.backgroundPattern}></div>
      <div style={styles.wrap}>
        <div style={styles.header}>
          <div style={styles.iconContainer}>
            🌾
          </div>
          <h2 style={styles.title}>Join the Harvest</h2>
          <p style={styles.subtitle}>Create your farmer account</p>
        </div>
        
        {err && (
          <div style={styles.err}>
            <span style={styles.errIcon}>⚠️</span>
            {err}
          </div>
        )}
        
        <form onSubmit={submit} style={styles.form}>
          <div style={styles.inputGroup}>
            <div style={styles.inputIcon}>📧</div>
            <input 
              placeholder="Email Address" 
              value={email} 
              onChange={(e)=>setEmail(e.target.value)} 
              style={styles.input}
              type="email"
              required
            />
          </div>
          
          <div style={styles.inputGroup}>
            <div style={styles.inputIcon}>👨‍🌾</div>
            <input 
              placeholder="Your Name (optional)" 
              value={name} 
              onChange={(e)=>setName(e.target.value)} 
              style={styles.input} 
            />
          </div>
          
          <div style={styles.inputGroup}>
            <div style={styles.inputIcon}>🔒</div>
            <input 
              placeholder="Password" 
              type="password" 
              value={password} 
              onChange={(e)=>setPassword(e.target.value)} 
              style={styles.input}
              required
            />
          </div>
          
          <button type="submit" style={styles.btn}>
            <span style={styles.btnIcon}>🌱</span>
            Plant Your Roots
          </button>
        </form>
        
        <div style={styles.footer}>
          <p style={styles.footerText}>
            Already have an account? 
            <span style={styles.loginLink} onClick={() => nav('/login')}>
              Sign in here
            </span>
          </p>
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #8BC34A 0%, #4CAF50 50%, #2E7D32 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
    position: 'relative',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
  },
  
  backgroundPattern: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundImage: `
      radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%),
      radial-gradient(circle at 40% 40%, rgba(255,255,255,0.05) 0%, transparent 50%)
    `,
    pointerEvents: 'none'
  },

  wrap: {
    background: 'rgba(255, 255, 255, 0.95)',
    backdropFilter: 'blur(10px)',
    borderRadius: '20px',
    padding: '40px',
    boxShadow: '0 20px 40px rgba(0,0,0,0.1), 0 0 0 1px rgba(255,255,255,0.2)',
    width: '100%',
    maxWidth: '420px',
    position: 'relative',
    border: '3px solid rgba(139, 195, 74, 0.3)'
  },

  header: {
    textAlign: 'center',
    marginBottom: '30px'
  },

  iconContainer: {
    fontSize: '48px',
    marginBottom: '15px',
    display: 'inline-block',
    animation: 'sway 3s ease-in-out infinite'
  },

  title: {
    color: '#2E7D32',
    fontSize: '28px',
    fontWeight: '700',
    margin: '0 0 8px 0',
    textShadow: '0 2px 4px rgba(0,0,0,0.1)'
  },

  subtitle: {
    color: '#558B2F',
    fontSize: '16px',
    margin: 0,
    fontWeight: '400'
  },

  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px'
  },

  inputGroup: {
    position: 'relative',
    display: 'flex',
    alignItems: 'center'
  },

  inputIcon: {
    position: 'absolute',
    left: '15px',
    fontSize: '18px',
    zIndex: 1,
    pointerEvents: 'none'
  },

  input: {
    width: '100%',
    padding: '15px 15px 15px 50px',
    border: '2px solid #C8E6C9',
    borderRadius: '12px',
    fontSize: '16px',
    background: '#FAFAFA',
    color: '#2E7D32',
    transition: 'all 0.3s ease',
    boxSizing: 'border-box',
    outline: 'none',
    '::placeholder': {
      color: '#81C784'
    }
  },

  btn: {
    width: '100%',
    padding: '16px',
    border: 'none',
    borderRadius: '12px',
    background: 'linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%)',
    color: 'white',
    fontSize: '18px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    boxShadow: '0 4px 15px rgba(76, 175, 80, 0.3)',
    textTransform: 'none'
  },

  btnIcon: {
    fontSize: '20px'
  },

  err: {
    background: 'linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%)',
    color: '#C62828',
    padding: '12px 16px',
    borderRadius: '10px',
    marginBottom: '20px',
    border: '1px solid #FFCDD2',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '14px'
  },

  errIcon: {
    fontSize: '16px'
  },

  footer: {
    textAlign: 'center',
    marginTop: '25px',
    paddingTop: '20px',
    borderTop: '1px solid #E8F5E8'
  },

  footerText: {
    color: '#558B2F',
    fontSize: '14px',
    margin: 0
  },

  loginLink: {
    color: '#4CAF50',
    fontWeight: '600',
    cursor: 'pointer',
    marginLeft: '5px',
    textDecoration: 'underline'
  }
}

// Add CSS keyframes for animation (you can add this to your global CSS file)
const styleSheet = document.createElement("style")
styleSheet.type = "text/css"
styleSheet.innerText = `
  @keyframes sway {
    0%, 100% { transform: rotate(-5deg); }
    50% { transform: rotate(5deg); }
  }
  
  input:focus {
    border-color: #4CAF50 !important;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1) !important;
    transform: translateY(-1px);
  }
  
  button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
  }
  
  button:active {
    transform: translateY(0px) !important;
  }
`
document.head.appendChild(styleSheet)
