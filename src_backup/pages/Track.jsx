import React from 'react';
import { MapPin, Phone } from 'lucide-react';

export default function Track() {
    return (
        <div className="container" style={{ paddingTop: '8rem', paddingBottom: '4rem', textAlign: 'center' }}>
            <h1>Track Your Freshness</h1>
            <div className="card" style={{ maxWidth: '400px', margin: '2rem auto', padding: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>Order #1003</span>
                    <span style={{ background: '#dcfce7', color: 'var(--primary-dark)', padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.8rem', fontWeight: 'bold' }}>IN TRANSIT</span>
                </div>

                <div style={{
                    height: '250px',
                    background: '#f1f5f9',
                    borderRadius: '1rem',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '1.5rem',
                    border: '2px dashed var(--border-color)'
                }}>
                    <MapPin size={48} color="var(--primary)" style={{ marginBottom: '1rem' }} />
                    <span style={{ color: 'var(--text-muted)' }}>Map Loading...</span>
                    <small style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>(Google Maps API Integration Pending)</small>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
                    <div style={{ width: '50px', height: '50px', borderRadius: '50%', background: '#cbd5e1', marginRight: '1rem' }}></div>
                    <div style={{ textAlign: 'left', flex: 1 }}>
                        <p style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>Kwame A.</p>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                            <span style={{ color: '#f59e0b' }}>★</span>
                            <span style={{ fontSize: '0.9rem' }}>4.9</span>
                        </div>
                    </div>
                    <button className="btn" style={{ padding: '0.75rem', borderRadius: '50%', background: '#dcfce7', color: 'var(--primary-dark)' }}>
                        <Phone size={20} />
                    </button>
                </div>

                <p style={{ fontWeight: 'bold', fontSize: '1.2rem', color: 'var(--text-main)' }}>Arriving in 12 mins</p>
                <div style={{ height: '4px', background: '#e2e8f0', borderRadius: '2px', marginTop: '1rem', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: '75%', background: 'var(--primary)' }}></div>
                </div>
            </div>
        </div>
    );
}
