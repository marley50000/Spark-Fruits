import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, Heart, Truck, Check } from 'lucide-react';

export default function Home() {
    return (
        <div style={{ paddingTop: '5rem' }}>
            {/* Hero */}
            <section className="container" style={{ padding: '4rem 1rem', textAlign: 'center', minHeight: '80vh', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                <h1 style={{ fontSize: 'clamp(2.5rem, 5vw, 4rem)', marginBottom: '1rem', lineHeight: 1.1 }}>
                    Pressed at dawn. <br />
                    <span style={{ color: 'var(--primary)' }}>Delivered by morning.</span>
                </h1>
                <p style={{ fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto 2rem', color: 'var(--text-muted)' }}>
                    The automatic daily habit. No shopping, no prep, just fresh vitality at your door.
                </p>
                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '4rem' }}>
                    <Link to="/subscribe" className="btn btn-primary" style={{ padding: '1rem 2rem', fontSize: '1.1rem', textDecoration: 'none' }}>
                        Start My Habit
                    </Link>
                    <Link to="/menu" className="btn" style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', color: 'var(--text-main)', textDecoration: 'none' }}>
                        View Menu
                    </Link>
                </div>

                {/* Trust Badges */}
                <div className="grid" style={{
                    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                    gap: '2rem'
                }}>
                    <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
                        <div style={{ padding: '1rem', borderRadius: '50%', background: '#fef3c7', marginBottom: '1rem' }}>
                            <Clock size={32} style={{ color: 'var(--accent)' }} />
                        </div>
                        <h3>Save Time</h3>
                        <p>No shopping or juicing. We do the work while you sleep.</p>
                    </div>
                    <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
                        <div style={{ padding: '1rem', borderRadius: '50%', background: '#dcfce7', marginBottom: '1rem' }}>
                            <Heart size={32} style={{ color: 'var(--primary)' }} />
                        </div>
                        <h3>Health Discipline</h3>
                        <p>Automatic consistency. Your daily vitamins, guaranteed.</p>
                    </div>
                    <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
                        <div style={{ padding: '1rem', borderRadius: '50%', background: '#e0e7ff', marginBottom: '1rem' }}>
                            <Truck size={32} style={{ color: '#4f46e5' }} />
                        </div>
                        <h3>Neighborhood Trust</h3>
                        <p>Delivered by the same rider, every morning.</p>
                    </div>
                </div>
            </section>

            {/* Product Highlight */}
            <section style={{ backgroundColor: 'var(--bg-secondary)', padding: '6rem 0' }}>
                <div className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1.5rem' }}>
                    <h2 style={{ textAlign: 'center', marginBottom: '3rem' }}>Our Signature Lines</h2>
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                        gap: '2rem'
                    }}>
                        {/* Product 1 */}
                        <div className="card">
                            <div style={{
                                height: '250px',
                                background: 'linear-gradient(135deg, #dcfce7 0%, #ffffff 100%)',
                                borderRadius: '0.5rem',
                                marginBottom: '1.5rem',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                position: 'relative',
                                overflow: 'hidden'
                            }}>
                                <span style={{ fontSize: '6rem' }}>🍍</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                                <h3>Daily Core</h3>
                                <span style={{ background: '#dcfce7', color: '#166534', padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.8rem', fontWeight: 'bold' }}>TOP SELLER</span>
                            </div>
                            <p style={{ marginBottom: '1.5rem' }}>The mass market favorite. Pineapple + Ginger for instant vitality.</p>

                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
                                <div>
                                    <span style={{ display: 'block', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Price</span>
                                    <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>GH₵ 15.00</span>
                                </div>
                                <button className="btn btn-primary" style={{ padding: '0.5rem 1rem' }}>Add to Plan</button>
                            </div>
                        </div>

                        {/* Product 2 */}
                        <div className="card">
                            <div style={{
                                height: '250px',
                                background: 'linear-gradient(135deg, #fef3c7 0%, #ffffff 100%)',
                                borderRadius: '0.5rem',
                                marginBottom: '1.5rem',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center'
                            }}>
                                <span style={{ fontSize: '6rem' }}>🥕</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                                <h3>Immunity Boost</h3>
                                <span style={{ background: '#fef3c7', color: '#92400e', padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.8rem', fontWeight: 'bold' }}>PREMIUM</span>
                            </div>
                            <p style={{ marginBottom: '1.5rem' }}>Orange + Carrot + Lime. Perfect for flu season and daily defense.</p>

                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
                                <div>
                                    <span style={{ display: 'block', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Price</span>
                                    <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>GH₵ 20.00</span>
                                </div>
                                <button className="btn btn-primary" style={{ padding: '0.5rem 1rem' }}>Add to Plan</button>
                            </div>
                        </div>

                        {/* Product 3 */}
                        <div className="card" style={{ border: '2px solid var(--primary)' }}>
                            <div style={{
                                height: '250px',
                                background: 'linear-gradient(135deg, #e0e7ff 0%, #ffffff 100%)',
                                borderRadius: '0.5rem',
                                marginBottom: '1.5rem',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center'
                            }}>
                                <div style={{ position: 'relative' }}>
                                    <span style={{ fontSize: '4rem', position: 'absolute', top: -20, left: -20 }}>🍍</span>
                                    <span style={{ fontSize: '4rem', position: 'absolute', top: -20, right: -20 }}>🥕</span>
                                    <span style={{ fontSize: '4rem', zIndex: 1 }}>🎒</span>
                                </div>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                                <h3>Office Pack</h3>
                                <span style={{ background: 'var(--primary)', color: 'white', padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.8rem', fontWeight: 'bold' }}>BEST VALUE</span>
                            </div>
                            <p style={{ marginBottom: '1.5rem' }}>5-day morning delivery. Set it and forget it for the work week.</p>
                            <ul style={{ marginBottom: '1.5rem', listStyle: 'none' }}>
                                <li style={{ display: 'flex', gap: '0.5rem', fontSize: '0.9rem', marginBottom: '0.25rem' }}><Check size={16} color="var(--primary)" /> Morning Delivery (6AM)</li>
                                <li style={{ display: 'flex', gap: '0.5rem', fontSize: '0.9rem', marginBottom: '0.25rem' }}><Check size={16} color="var(--primary)" /> Free Delivery</li>
                            </ul>

                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
                                <div>
                                    <span style={{ display: 'block', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Weekly</span>
                                    <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>GH₵ 70.00</span>
                                </div>
                                <button className="btn btn-primary" style={{ padding: '0.5rem 1rem' }}>Subscribe</button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
