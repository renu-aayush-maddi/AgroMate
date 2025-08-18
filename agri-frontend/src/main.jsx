// import "./i18n";
// import React, { useState } from 'react'
// import ReactDOM from 'react-dom/client'
// import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom'
// import App from './pages/Chat.jsx'
// import Login from './pages/Login.jsx'
// import Signup from './pages/Signup.jsx'
// import Profile from './pages/Profile.jsx'
// import { AuthProvider, useAuth } from './state/AuthContext.jsx'

// function Nav() {
//   const { token, logout } = useAuth()
//   const [isMenuOpen, setIsMenuOpen] = useState(false)
//   const toggleMenu = () => setIsMenuOpen(!isMenuOpen)
//   const closeMenu = () => setIsMenuOpen(false)

//   return (
//     <nav style={styles.nav}>
//       <div style={styles.container}>
//         <div style={styles.brand}>
//           <Link to="/" style={styles.brandLink} onClick={closeMenu}>
//             <span style={styles.logo}>🌾</span>
//             <div style={styles.brandText}>
//               <span style={styles.brandName}>Agri Advisor</span>
//               <span style={styles.brandTagline}>Smart Farming Solutions</span>
//             </div>
//           </Link>
//         </div>

//         {/* Desktop */}
//         <div style={styles.desktopNav}>
//           <Link to="/" style={styles.navLink}>💬 Chat</Link>
//           <Link to="/profile" style={styles.navLink}>👤 Profile</Link>

//           {token ? (
//             <div style={styles.userSection}>
//               <span style={styles.welcomeText}>Welcome, Farmer!</span>
//               <button onClick={logout} style={styles.logoutBtn}>
//                 <span style={styles.btnIcon}>🚪</span> Logout
//               </button>
//             </div>
//           ) : (
//             <div style={styles.authLinks}>
//               <Link to="/login" style={styles.authLink}>🔑 Login</Link>
//               <Link to="/signup" style={styles.signupBtn}>🌱 Join Farm</Link>
//             </div>
//           )}
//         </div>

//         {/* Mobile trigger */}
//         <button style={styles.mobileMenuBtn} onClick={toggleMenu}>
//           <span style={isMenuOpen ? styles.hamburgerOpen : styles.hamburger}>
//             {isMenuOpen ? '✕' : '☰'}
//           </span>
//         </button>
//       </div>

//       {/* Mobile menu */}
//       {isMenuOpen && (
//         <div style={styles.mobileOverlay} onClick={closeMenu}>
//           <div style={styles.mobileMenu} onClick={(e) => e.stopPropagation()}>
//             <div style={styles.mobileHeader}>
//               <span style={styles.mobileTitle}>Navigation</span>
//               <button style={styles.closeBtn} onClick={closeMenu}>✕</button>
//             </div>

//             <div style={styles.mobileLinks}>
//               <Link to="/" style={styles.mobileLink} onClick={closeMenu}>
//                 <span>💬</span><span>Chat with AI</span><span style={styles.arrow}>→</span>
//               </Link>
//               <Link to="/profile" style={styles.mobileLink} onClick={closeMenu}>
//                 <span>👤</span><span>Profile</span><span style={styles.arrow}>→</span>
//               </Link>

//               {token ? (
//                 <>
//                   <div style={styles.mobileUserInfo}>
//                     <span style={styles.mobileWelcome}>👨‍🌾 Welcome, Farmer!</span>
//                   </div>
//                   <button onClick={() => { logout(); closeMenu(); }} style={styles.mobileLogoutBtn}>
//                     <span>🚪</span><span>Logout</span>
//                   </button>
//                 </>
//               ) : (
//                 <>
//                   <Link to="/login" style={styles.mobileLink} onClick={closeMenu}>
//                     <span>🔑</span><span>Login</span><span style={styles.arrow}>→</span>
//                   </Link>
//                   <Link to="/signup" style={styles.mobileSignupLink} onClick={closeMenu}>
//                     <span>🌱</span><span>Join the Farm</span><span style={styles.arrow}>→</span>
//                   </Link>
//                 </>
//               )}
//             </div>
//           </div>
//         </div>
//       )}
//     </nav>
//   )
// }

// function Root() {
//   return (
//     <AuthProvider>
//       <BrowserRouter>
//         <Nav />
//         <Routes>
//           <Route path="/" element={<App />} />
//           <Route path="/profile" element={<Profile />} />
//           <Route path="/login" element={<Login />} />
//           <Route path="/signup" element={<Signup />} />
//           <Route path="/profile" element={<Profile />} />
//           <Route path="*" element={<Navigate to="/" />} />
//         </Routes>
//       </BrowserRouter>
//     </AuthProvider>
//   )
// }


// const styles = {
//   nav: {
//     background: 'linear-gradient(135deg, #2E7D32 0%, #388E3C 50%, #4CAF50 100%)',
//     boxShadow: '0 2px 20px rgba(46, 125, 50, 0.3)',
//     position: 'sticky',
//     top: 0,
//     zIndex: 1000,
//     borderBottom: '3px solid rgba(255, 255, 255, 0.1)'
//   },

//   container: {
//     maxWidth: '1200px',
//     margin: '0 auto',
//     padding: '0 20px',
//     display: 'flex',
//     alignItems: 'center',
//     justifyContent: 'space-between',
//     height: '70px'
//   },

//   brand: {
//     display: 'flex',
//     alignItems: 'center'
//   },

//   brandLink: {
//     display: 'flex',
//     alignItems: 'center',
//     textDecoration: 'none',
//     color: 'white'
//   },

//   logo: {
//     fontSize: '32px',
//     marginRight: '12px',
//     animation: 'gentle-sway 4s ease-in-out infinite'
//   },

//   brandText: {
//     display: 'flex',
//     flexDirection: 'column'
//   },

//   brandName: {
//     fontSize: '24px',
//     fontWeight: '700',
//     color: 'white',
//     textShadow: '0 2px 4px rgba(0,0,0,0.3)',
//     lineHeight: '1.2'
//   },

//   brandTagline: {
//     fontSize: '12px',
//     color: 'rgba(255, 255, 255, 0.8)',
//     fontWeight: '400',
//     marginTop: '2px'
//   },

//   desktopNav: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '24px'
//   },

//   navLink: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '6px',
//     color: 'rgba(255, 255, 255, 0.9)',
//     textDecoration: 'none',
//     padding: '8px 12px',
//     borderRadius: '8px',
//     transition: 'all 0.3s ease',
//     fontSize: '16px',
//     fontWeight: '500'
//   },

//   navIcon: {
//     fontSize: '18px'
//   },

//   userSection: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '16px'
//   },

//   welcomeText: {
//     color: 'rgba(255, 255, 255, 0.9)',
//     fontSize: '14px',
//     fontWeight: '500'
//   },

//   authLinks: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '16px'
//   },

//   authLink: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '6px',
//     color: 'rgba(255, 255, 255, 0.9)',
//     textDecoration: 'none',
//     padding: '8px 12px',
//     borderRadius: '8px',
//     transition: 'all 0.3s ease',
//     fontSize: '16px',
//     fontWeight: '500'
//   },

//   signupBtn: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '6px',
//     background: 'rgba(255, 255, 255, 0.15)',
//     backdropFilter: 'blur(10px)',
//     color: 'white',
//     textDecoration: 'none',
//     padding: '10px 16px',
//     borderRadius: '25px',
//     border: '1px solid rgba(255, 255, 255, 0.2)',
//     transition: 'all 0.3s ease',
//     fontSize: '15px',
//     fontWeight: '600'
//   },

//   logoutBtn: {
//     display: 'flex',
//     alignItems: 'center',
//     gap: '6px',
//     background: 'rgba(255, 255, 255, 0.1)',
//     color: 'white',
//     border: '1px solid rgba(255, 255, 255, 0.3)',
//     padding: '8px 14px',
//     borderRadius: '20px',
//     cursor: 'pointer',
//     transition: 'all 0.3s ease',
//     fontSize: '14px',
//     fontWeight: '500'
//   },

//   btnIcon: {
//     fontSize: '16px'
//   },

//   mobileMenuBtn: {
//     display: 'none',
//     background: 'rgba(255, 255, 255, 0.1)',
//     border: '1px solid rgba(255, 255, 255, 0.2)',
//     color: 'white',
//     padding: '8px',
//     borderRadius: '8px',
//     cursor: 'pointer',
//     fontSize: '20px',
//     width: '44px',
//     height: '44px',
//     alignItems: 'center',
//     justifyContent: 'center'
//   },

//   hamburger: {
//     transition: 'all 0.3s ease'
//   },

//   hamburgerOpen: {
//     transition: 'all 0.3s ease',
//     transform: 'rotate(90deg)'
//   },

//   mobileOverlay: {
//     position: 'fixed',
//     top: '70px',
//     left: 0,
//     right: 0,
//     bottom: 0,
//     background: 'rgba(0, 0, 0, 0.5)',
//     backdropFilter: 'blur(5px)',
//     zIndex: 999
//   },

//   mobileMenu: {
//     background: 'linear-gradient(180deg, #FFFFFF 0%, #F1F8E9 100%)',
//     margin: '0',
//     height: '100%',
//     overflowY: 'auto',
//     boxShadow: '0 4px 20px rgba(0,0,0,0.15)'
//   },

//   mobileHeader: {
//     padding: '20px',
//     borderBottom: '1px solid #E8F5E8',
//     display: 'flex',
//     justifyContent: 'space-between',
//     alignItems: 'center',
//     background: 'linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%)',
//     color: 'white'
//   },

//   mobileTitle: {
//     fontSize: '18px',
//     fontWeight: '600'
//   },

//   closeBtn: {
//     background: 'none',
//     border: 'none',
//     color: 'white',
//     fontSize: '24px',
//     cursor: 'pointer',
//     padding: '4px',
//     borderRadius: '4px'
//   },

//   mobileLinks: {
//     padding: '20px 0'
//   },

//   mobileLink: {
//     display: 'flex',
//     alignItems: 'center',
//     padding: '16px 24px',
//     color: '#2E7D32',
//     textDecoration: 'none',
//     borderBottom: '1px solid #E8F5E8',
//     transition: 'all 0.3s ease',
//     fontSize: '16px',
//     fontWeight: '500'
//   },

//   mobileSignupLink: {
//     display: 'flex',
//     alignItems: 'center',
//     padding: '16px 24px',
//     color: 'white',
//     textDecoration: 'none',
//     background: 'linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%)',
//     margin: '16px 24px',
//     borderRadius: '12px',
//     fontSize: '16px',
//     fontWeight: '600',
//     boxShadow: '0 4px 12px rgba(76, 175, 80, 0.3)'
//   },

//   arrow: {
//     marginLeft: 'auto',
//     fontSize: '18px',
//     color: '#81C784'
//   },

//   mobileUserInfo: {
//     padding: '16px 24px',
//     background: 'linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%)',
//     margin: '16px 24px',
//     borderRadius: '12px',
//     border: '1px solid #A5D6A7'
//   },

//   mobileWelcome: {
//     color: '#2E7D32',
//     fontSize: '16px',
//     fontWeight: '600'
//   },

//   mobileLogoutBtn: {
//     display: 'flex',
//     alignItems: 'center',
//     padding: '16px 24px',
//     color: '#D32F2F',
//     background: 'none',
//     border: 'none',
//     borderBottom: '1px solid #E8F5E8',
//     fontSize: '16px',
//     fontWeight: '500',
//     width: '100%',
//     textAlign: 'left',
//     cursor: 'pointer'
//   },

//   mobileFooter: {
//     padding: '20px 24px',
//     borderTop: '1px solid #E8F5E8',
//     textAlign: 'center',
//     background: '#F1F8E9'
//   },

//   footerText: {
//     color: '#558B2F',
//     fontSize: '14px',
//     margin: 0,
//     fontWeight: '500'
//   }
// }

// // Media queries and additional styles
// const mediaStyles = document.createElement("style")
// mediaStyles.type = "text/css"
// mediaStyles.innerText = `
//   @keyframes gentle-sway {
//     0%, 100% { transform: rotate(-3deg); }
//     50% { transform: rotate(3deg); }
//   }
  
//   /* Desktop hover effects */
//   @media (min-width: 769px) {
//     .nav-link:hover {
//       background: rgba(255, 255, 255, 0.1) !important;
//       transform: translateY(-1px);
//     }
    
//     .signup-btn:hover {
//       background: rgba(255, 255, 255, 0.25) !important;
//       transform: translateY(-2px);
//       box-shadow: 0 4px 12px rgba(0,0,0,0.2);
//     }
    
//     .logout-btn:hover {
//       background: rgba(255, 255, 255, 0.2) !important;
//       transform: translateY(-1px);
//     }
//   }
  
//   /* Mobile styles */
//   @media (max-width: 768px) {
//     .desktop-nav {
//       display: none !important;
//     }
    
//     .mobile-menu-btn {
//       display: flex !important;
//     }
    
//     .brand-name {
//       font-size: 20px !important;
//     }
    
//     .brand-tagline {
//       font-size: 11px !important;
//     }
    
//     .logo {
//       font-size: 28px !important;
//       margin-right: 8px !important;
//     }
    
//     .container {
//       padding: 0 16px !important;
//       height: 60px !important;
//     }
    
//     .mobile-overlay {
//       top: 60px !important;
//     }
    
//     .mobile-link:hover {
//       background: #F1F8E9 !important;
//       padding-left: 32px !important;
//     }
    
//     .mobile-signup-link:hover {
//       transform: translateY(-1px) !important;
//       box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4) !important;
//     }
//   }
  
//   /* Small mobile devices */
//   @media (max-width: 480px) {
//     .brand-text {
//       display: none !important;
//     }
    
//     .logo {
//       font-size: 32px !important;
//       margin-right: 0 !important;
//     }
//   }
// `
// document.head.appendChild(mediaStyles)

// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <Root />
//   </React.StrictMode>
// )


import "./i18n";
import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom'
import App from './pages/Chat.jsx'
import Login from './pages/Login.jsx'
import Signup from './pages/Signup.jsx'
import Profile from './pages/Profile.jsx'
import { AuthProvider, useAuth } from './state/AuthContext.jsx'

function Nav() {
  const { token, logout } = useAuth()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const toggleMenu = () => setIsMenuOpen(!isMenuOpen)
  const closeMenu = () => setIsMenuOpen(false)

  return (
    <nav className="nav">
      <div className="container">
        <div className="brand">
          <Link to="/" className="brand-link" onClick={closeMenu}>
            <span className="logo">🌾</span>
            <div className="brand-text">
              <span className="brand-name">Agri Advisor</span>
              <span className="brand-tagline">Smart Farming Solutions</span>
            </div>
          </Link>
        </div>

        {/* Desktop Navigation */}
        <div className="desktop-nav">
          <Link to="/" className="nav-link">💬 Chat</Link>
          <Link to="/profile" className="nav-link">👤 Profile</Link>

          {token ? (
            <div className="user-section">
              <span className="welcome-text">Welcome, Farmer!</span>
              <button onClick={logout} className="logout-btn">
                <span className="btn-icon">🚪</span> Logout
              </button>
            </div>
          ) : (
            <div className="auth-links">
              <Link to="/login" className="auth-link">🔑 Login</Link>
              <Link to="/signup" className="signup-btn">🌱 Join Farm</Link>
            </div>
          )}
        </div>

        {/* Mobile Hamburger Button */}
        <button className="mobile-menu-btn" onClick={toggleMenu}>
          <span className={isMenuOpen ? 'hamburger-open' : 'hamburger'}>
            {isMenuOpen ? '✕' : '☰'}
          </span>
        </button>
      </div>

      {/* Mobile Menu Overlay */}
      {isMenuOpen && (
        <div className="mobile-overlay" onClick={closeMenu}>
          <div className="mobile-menu" onClick={(e) => e.stopPropagation()}>
            <div className="mobile-header">
              <span className="mobile-title">Navigation</span>
              <button className="close-btn" onClick={closeMenu}>✕</button>
            </div>

            <div className="mobile-links">
              <Link to="/" className="mobile-link" onClick={closeMenu}>
                <span>💬</span><span>Chat with AI</span><span className="arrow">→</span>
              </Link>
              <Link to="/profile" className="mobile-link" onClick={closeMenu}>
                <span>👤</span><span>Profile</span><span className="arrow">→</span>
              </Link>

              {token ? (
                <>
                  <div className="mobile-user-info">
                    <span className="mobile-welcome">👨‍🌾 Welcome, Farmer!</span>
                  </div>
                  <button onClick={() => { logout(); closeMenu(); }} className="mobile-logout-btn">
                    <span>🚪</span><span>Logout</span>
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="mobile-link" onClick={closeMenu}>
                    <span>🔑</span><span>Login</span><span className="arrow">→</span>
                  </Link>
                  <Link to="/signup" className="mobile-signup-link" onClick={closeMenu}>
                    <span>🌱</span><span>Join the Farm</span><span className="arrow">→</span>
                  </Link>
                </>
              )}
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
          <Route path="/profile" element={<Profile />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

// CSS Styles
const styles = `
@keyframes gentle-sway {
  0%, 100% { transform: rotate(-3deg); }
  50% { transform: rotate(3deg); }
}

.nav {
  background: linear-gradient(135deg, #2E7D32 0%, #388E3C 50%, #4CAF50 100%);
  box-shadow: 0 2px 20px rgba(46, 125, 50, 0.3);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 3px solid rgba(255, 255, 255, 0.1);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.brand {
  display: flex;
  align-items: center;
}

.brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
}

.logo {
  font-size: 32px;
  margin-right: 12px;
  animation: gentle-sway 4s ease-in-out infinite;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 24px;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
  line-height: 1.2;
}

.brand-tagline {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
  margin-top: 2px;
}

.desktop-nav {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-link, .auth-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-size: 16px;
  font-weight: 500;
}

.nav-link:hover, .auth-link:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.user-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.welcome-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-weight: 500;
}

.auth-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.signup-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  text-decoration: none;
  padding: 10px 16px;
  border-radius: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  font-size: 15px;
  font-weight: 600;
}

.signup-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 8px 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.btn-icon {
  font-size: 16px;
}

.mobile-menu-btn {
  display: none;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 20px;
  width: 44px;
  height: 44px;
  align-items: center;
  justify-content: center;
}

.hamburger {
  transition: all 0.3s ease;
}

.hamburger-open {
  transition: all 0.3s ease;
  transform: rotate(90deg);
}

.mobile-overlay {
  position: fixed;
  top: 70px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 999;
}

.mobile-menu {
  background: linear-gradient(180deg, #FFFFFF 0%, #F1F8E9 100%);
  margin: 0;
  height: 100%;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.mobile-header {
  padding: 20px;
  border-bottom: 1px solid #E8F5E8;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  color: white;
}

.mobile-title {
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.mobile-links {
  padding: 20px 0;
}

.mobile-link {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  color: #2E7D32;
  text-decoration: none;
  border-bottom: 1px solid #E8F5E8;
  transition: all 0.3s ease;
  font-size: 16px;
  font-weight: 500;
}

.mobile-link:hover {
  background: #F1F8E8;
  padding-left: 32px;
}

.mobile-signup-link {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  color: white;
  text-decoration: none;
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  margin: 16px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
  transition: all 0.3s ease;
}

.mobile-signup-link:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

.arrow {
  margin-left: auto;
  font-size: 18px;
  color: #81C784;
}

.mobile-user-info {
  padding: 16px 24px;
  background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
  margin: 16px 24px;
  border-radius: 12px;
  border: 1px solid #A5D6A7;
}

.mobile-welcome {
  color: #2E7D32;
  font-size: 16px;
  font-weight: 600;
}

.mobile-logout-btn {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  color: #D32F2F;
  background: none;
  border: none;
  border-bottom: 1px solid #E8F5E8;
  font-size: 16px;
  font-weight: 500;
  width: 100%;
  text-align: left;
  cursor: pointer;
  gap: 12px;
}

/* Mobile Responsive Styles */
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
}

/* Small Mobile Devices */
@media (max-width: 480px) {
  .brand-text {
    display: none !important;
  }
  
  .logo {
    font-size: 32px !important;
    margin-right: 0 !important;
  }
  
  .container {
    padding: 0 12px !important;
  }
}

/* Large Desktop */
@media (min-width: 1200px) {
  .container {
    padding: 0 40px;
  }
  
  .desktop-nav {
    gap: 32px;
  }
}
`

// Inject styles
const styleSheet = document.createElement("style")
styleSheet.type = "text/css"
styleSheet.innerText = styles
document.head.appendChild(styleSheet)

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>
)