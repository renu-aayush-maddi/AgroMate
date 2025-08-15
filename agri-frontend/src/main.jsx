// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
// import './index.css'
// import App from './App.jsx'

// createRoot(document.getElementById('root')).render(
//   <StrictMode>
//     <App />
//   </StrictMode>,
// )
import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom'
import App from './pages/Chat.jsx'
import Login from './pages/Login.jsx'
import Signup from './pages/Signup.jsx'
import { AuthProvider, useAuth } from './state/AuthContext.jsx'

function Nav() {
  const { token, logout } = useAuth()
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen)
  const closeMenu = () => setIsMenuOpen(false)

  return (
    <nav style={styles.nav}>
      <div style={styles.container}>
        {/* Logo/Brand Section */}
        <div style={styles.brand}>
          <Link to="/" style={styles.brandLink} onClick={closeMenu}>
            <span style={styles.logo}>🌾</span>
            <div style={styles.brandText}>
              <span style={styles.brandName}>Agri Advisor</span>
              <span style={styles.brandTagline}>Smart Farming Solutions</span>
            </div>
          </Link>
        </div>

        {/* Desktop Navigation */}
        <div style={styles.desktopNav}>
          <Link to="/" style={styles.navLink}>
            <span style={styles.navIcon}>💬</span>
            Chat
          </Link>
          
          {token ? (
            <div style={styles.userSection}>
              <span style={styles.welcomeText}>Welcome, Farmer!</span>
              <button onClick={logout} style={styles.logoutBtn}>
                <span style={styles.btnIcon}>🚪</span>
                Logout
              </button>
            </div>
          ) : (
            <div style={styles.authLinks}>
              <Link to="/login" style={styles.authLink}>
                <span style={styles.navIcon}>🔑</span>
                Login
              </Link>
              <Link to="/signup" style={styles.signupBtn}>
                <span style={styles.btnIcon}>🌱</span>
                Join Farm
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button style={styles.mobileMenuBtn} onClick={toggleMenu}>
          <span style={isMenuOpen ? styles.hamburgerOpen : styles.hamburger}>
            {isMenuOpen ? '✕' : '☰'}
          </span>
        </button>
      </div>

      {/* Mobile Menu Overlay */}
      {isMenuOpen && (
        <div style={styles.mobileOverlay} onClick={closeMenu}>
          <div style={styles.mobileMenu} onClick={(e) => e.stopPropagation()}>
            <div style={styles.mobileHeader}>
              <span style={styles.mobileTitle}>Navigation</span>
              <button style={styles.closeBtn} onClick={closeMenu}>✕</button>
            </div>
            
            <div style={styles.mobileLinks}>
              <Link to="/" style={styles.mobileLink} onClick={closeMenu}>
                <span style={styles.navIcon}>💬</span>
                <span>Chat with AI</span>
                <span style={styles.arrow}>→</span>
              </Link>
              
              {token ? (
                <>
                  <div style={styles.mobileUserInfo}>
                    <span style={styles.mobileWelcome}>👨‍🌾 Welcome, Farmer!</span>
                  </div>
                  <button onClick={() => {logout(); closeMenu();}} style={styles.mobileLogoutBtn}>
                    <span style={styles.navIcon}>🚪</span>
                    <span>Logout</span>
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" style={styles.mobileLink} onClick={closeMenu}>
                    <span style={styles.navIcon}>🔑</span>
                    <span>Login</span>
                    <span style={styles.arrow}>→</span>
                  </Link>
                  <Link to="/signup" style={styles.mobileSignupLink} onClick={closeMenu}>
                    <span style={styles.navIcon}>🌱</span>
                    <span>Join the Farm</span>
                    <span style={styles.arrow}>→</span>
                  </Link>
                </>
              )}
            </div>
            
            <div style={styles.mobileFooter}>
              <p style={styles.footerText}>🇮🇳 Built for Indian Farmers</p>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}

function Root() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Nav />
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

const styles = {
  nav: {
    background: 'linear-gradient(135deg, #2E7D32 0%, #388E3C 50%, #4CAF50 100%)',
    boxShadow: '0 2px 20px rgba(46, 125, 50, 0.3)',
    position: 'sticky',
    top: 0,
    zIndex: 1000,
    borderBottom: '3px solid rgba(255, 255, 255, 0.1)'
  },

  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: '70px'
  },

  brand: {
    display: 'flex',
    alignItems: 'center'
  },

  brandLink: {
    display: 'flex',
    alignItems: 'center',
    textDecoration: 'none',
    color: 'white'
  },

  logo: {
    fontSize: '32px',
    marginRight: '12px',
    animation: 'gentle-sway 4s ease-in-out infinite'
  },

  brandText: {
    display: 'flex',
    flexDirection: 'column'
  },

  brandName: {
    fontSize: '24px',
    fontWeight: '700',
    color: 'white',
    textShadow: '0 2px 4px rgba(0,0,0,0.3)',
    lineHeight: '1.2'
  },

  brandTagline: {
    fontSize: '12px',
    color: 'rgba(255, 255, 255, 0.8)',
    fontWeight: '400',
    marginTop: '2px'
  },

  desktopNav: {
    display: 'flex',
    alignItems: 'center',
    gap: '24px'
  },

  navLink: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    color: 'rgba(255, 255, 255, 0.9)',
    textDecoration: 'none',
    padding: '8px 12px',
    borderRadius: '8px',
    transition: 'all 0.3s ease',
    fontSize: '16px',
    fontWeight: '500'
  },

  navIcon: {
    fontSize: '18px'
  },

  userSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px'
  },

  welcomeText: {
    color: 'rgba(255, 255, 255, 0.9)',
    fontSize: '14px',
    fontWeight: '500'
  },

  authLinks: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px'
  },

  authLink: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    color: 'rgba(255, 255, 255, 0.9)',
    textDecoration: 'none',
    padding: '8px 12px',
    borderRadius: '8px',
    transition: 'all 0.3s ease',
    fontSize: '16px',
    fontWeight: '500'
  },

  signupBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    background: 'rgba(255, 255, 255, 0.15)',
    backdropFilter: 'blur(10px)',
    color: 'white',
    textDecoration: 'none',
    padding: '10px 16px',
    borderRadius: '25px',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    transition: 'all 0.3s ease',
    fontSize: '15px',
    fontWeight: '600'
  },

  logoutBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    background: 'rgba(255, 255, 255, 0.1)',
    color: 'white',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    padding: '8px 14px',
    borderRadius: '20px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    fontSize: '14px',
    fontWeight: '500'
  },

  btnIcon: {
    fontSize: '16px'
  },

  mobileMenuBtn: {
    display: 'none',
    background: 'rgba(255, 255, 255, 0.1)',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    color: 'white',
    padding: '8px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '20px',
    width: '44px',
    height: '44px',
    alignItems: 'center',
    justifyContent: 'center'
  },

  hamburger: {
    transition: 'all 0.3s ease'
  },

  hamburgerOpen: {
    transition: 'all 0.3s ease',
    transform: 'rotate(90deg)'
  },

  mobileOverlay: {
    position: 'fixed',
    top: '70px',
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0, 0, 0, 0.5)',
    backdropFilter: 'blur(5px)',
    zIndex: 999
  },

  mobileMenu: {
    background: 'linear-gradient(180deg, #FFFFFF 0%, #F1F8E9 100%)',
    margin: '0',
    height: '100%',
    overflowY: 'auto',
    boxShadow: '0 4px 20px rgba(0,0,0,0.15)'
  },

  mobileHeader: {
    padding: '20px',
    borderBottom: '1px solid #E8F5E8',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    background: 'linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%)',
    color: 'white'
  },

  mobileTitle: {
    fontSize: '18px',
    fontWeight: '600'
  },

  closeBtn: {
    background: 'none',
    border: 'none',
    color: 'white',
    fontSize: '24px',
    cursor: 'pointer',
    padding: '4px',
    borderRadius: '4px'
  },

  mobileLinks: {
    padding: '20px 0'
  },

  mobileLink: {
    display: 'flex',
    alignItems: 'center',
    padding: '16px 24px',
    color: '#2E7D32',
    textDecoration: 'none',
    borderBottom: '1px solid #E8F5E8',
    transition: 'all 0.3s ease',
    fontSize: '16px',
    fontWeight: '500'
  },

  mobileSignupLink: {
    display: 'flex',
    alignItems: 'center',
    padding: '16px 24px',
    color: 'white',
    textDecoration: 'none',
    background: 'linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%)',
    margin: '16px 24px',
    borderRadius: '12px',
    fontSize: '16px',
    fontWeight: '600',
    boxShadow: '0 4px 12px rgba(76, 175, 80, 0.3)'
  },

  arrow: {
    marginLeft: 'auto',
    fontSize: '18px',
    color: '#81C784'
  },

  mobileUserInfo: {
    padding: '16px 24px',
    background: 'linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%)',
    margin: '16px 24px',
    borderRadius: '12px',
    border: '1px solid #A5D6A7'
  },

  mobileWelcome: {
    color: '#2E7D32',
    fontSize: '16px',
    fontWeight: '600'
  },

  mobileLogoutBtn: {
    display: 'flex',
    alignItems: 'center',
    padding: '16px 24px',
    color: '#D32F2F',
    background: 'none',
    border: 'none',
    borderBottom: '1px solid #E8F5E8',
    fontSize: '16px',
    fontWeight: '500',
    width: '100%',
    textAlign: 'left',
    cursor: 'pointer'
  },

  mobileFooter: {
    padding: '20px 24px',
    borderTop: '1px solid #E8F5E8',
    textAlign: 'center',
    background: '#F1F8E9'
  },

  footerText: {
    color: '#558B2F',
    fontSize: '14px',
    margin: 0,
    fontWeight: '500'
  }
}

// Media queries and additional styles
const mediaStyles = document.createElement("style")
mediaStyles.type = "text/css"
mediaStyles.innerText = `
  @keyframes gentle-sway {
    0%, 100% { transform: rotate(-3deg); }
    50% { transform: rotate(3deg); }
  }
  
  /* Desktop hover effects */
  @media (min-width: 769px) {
    .nav-link:hover {
      background: rgba(255, 255, 255, 0.1) !important;
      transform: translateY(-1px);
    }
    
    .signup-btn:hover {
      background: rgba(255, 255, 255, 0.25) !important;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .logout-btn:hover {
      background: rgba(255, 255, 255, 0.2) !important;
      transform: translateY(-1px);
    }
  }
  
  /* Mobile styles */
  @media (max-width: 768px) {
    .desktop-nav {
      display: none !important;
    }
    
    .mobile-menu-btn {
      display: flex !important;
    }
    
    .brand-name {
      font-size: 20px !important;
    }
    
    .brand-tagline {
      font-size: 11px !important;
    }
    
    .logo {
      font-size: 28px !important;
      margin-right: 8px !important;
    }
    
    .container {
      padding: 0 16px !important;
      height: 60px !important;
    }
    
    .mobile-overlay {
      top: 60px !important;
    }
    
    .mobile-link:hover {
      background: #F1F8E9 !important;
      padding-left: 32px !important;
    }
    
    .mobile-signup-link:hover {
      transform: translateY(-1px) !important;
      box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4) !important;
    }
  }
  
  /* Small mobile devices */
  @media (max-width: 480px) {
    .brand-text {
      display: none !important;
    }
    
    .logo {
      font-size: 32px !important;
      margin-right: 0 !important;
    }
  }
`
document.head.appendChild(mediaStyles)

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>
)
