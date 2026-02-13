import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, ShoppingBag, Leaf, User } from 'lucide-react';

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <nav className="glass" style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            zIndex: 50
        }}>
            <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1rem 1.5rem' }}>
                <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', textDecoration: 'none' }} onClick={() => setIsOpen(false)}>
                    <Leaf size={24} style={{ color: 'var(--primary)' }} />
                    <span style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--primary)' }}>
                        Daily<span style={{ color: 'var(--text-main)' }}>Fresh</span>
                    </span>
                </Link>

                {/* Desktop Menu */}
                <div className="hidden-mobile" style={{ gap: '2rem', alignItems: 'center' }}>
                    <Link to="/menu" className="btn" style={{ padding: '0.5rem', background: 'transparent', color: 'var(--text-main)' }}>Menu</Link>
                    <Link to="/subscribe" className="btn" style={{ padding: '0.5rem', background: 'transparent', color: 'var(--text-main)' }}>Plans</Link>
                    <Link to="/track" className="btn" style={{ padding: '0.5rem', background: 'transparent', color: 'var(--text-main)' }}>Track Order</Link>
                </div>

                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <Link to="/subscribe" className="btn btn-primary hidden-mobile">
                        Order Now
                    </Link>

                    <button
                        className="btn"
                        style={{ background: 'transparent', padding: '0.5rem', color: 'var(--text-main)' }}
                        onClick={() => setIsOpen(!isOpen)}
                        aria-label="Toggle menu"
                    >
                        {isOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>
            </div>

            {/* Mobile Menu Overlay */}
            {isOpen && (
                <div className="glass" style={{
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    right: 0,
                    padding: '2rem',
                    borderTop: '1px solid var(--border-color)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '1.5rem',
                    height: 'calc(100vh - 80px)', // adjust based on navbar height
                }}>
                    <Link to="/menu" className="btn" style={{ justifyContent: 'flex-start', fontSize: '1.2rem' }} onClick={() => setIsOpen(false)}>Menu</Link>
                    <Link to="/subscribe" className="btn" style={{ justifyContent: 'flex-start', fontSize: '1.2rem' }} onClick={() => setIsOpen(false)}>Plans</Link>
                    <Link to="/track" className="btn" style={{ justifyContent: 'flex-start', fontSize: '1.2rem' }} onClick={() => setIsOpen(false)}>Track Order</Link>
                    <Link to="/admin" className="btn" style={{ justifyContent: 'flex-start', fontSize: '1.2rem' }} onClick={() => setIsOpen(false)}>Admin Log In</Link>
                    <hr style={{ borderColor: 'var(--border-color)' }} />
                    <Link to="/subscribe" className="btn btn-primary" style={{ width: '100%' }} onClick={() => setIsOpen(false)}>
                        Order Now
                    </Link>
                </div>
            )}
        </nav>
    );
}
