import React, { useState } from 'react';
import { Calendar, Check } from 'lucide-react';

export default function Subscribe() {
    const [selectedPlan, setSelectedPlan] = useState('office');

    const getPrice = () => {
        switch (selectedPlan) {
            case 'office': return '70.00';
            case 'daily': return '100.00';
            case 'starter': return '10.00';
            default: return '0.00';
        }
    };

    return (
        <div className="container" style={{ paddingTop: '6rem', paddingBottom: '4rem' }}>
            <h1 style={{ textAlign: 'center', marginBottom: '1rem' }}>Choose Your Habit</h1>
            <p style={{ textAlign: 'center', maxWidth: '600px', margin: '0 auto 3rem' }}>
                Subscribe to health discipline. Pause or cancel anytime.
            </p>

            <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginBottom: '4rem' }}>

                {/* Plan 1: Office Pack */}
                <div
                    className="card"
                    style={{
                        border: selectedPlan === 'office' ? '2px solid var(--primary)' : '1px solid var(--border-color)',
                        scale: selectedPlan === 'office' ? '1.05' : '1',
                        cursor: 'pointer'
                    }}
                    onClick={() => setSelectedPlan('office')}
                >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h3 style={{ margin: 0 }}>Office Pack</h3>
                        <span style={{ background: 'var(--primary)', color: 'white', padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.8rem', fontWeight: 'bold' }}>Most Popular</span>
                    </div>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>GH₵ 70 <span style={{ fontSize: '1rem', fontWeight: 'normal', color: 'var(--text-muted)' }}>/ week</span></p>
                    <p style={{ marginBottom: '1.5rem' }}>5 Bottles (Mon-Fri)</p>

                    <ul style={{ listStyle: 'none', marginBottom: '2rem' }}>
                        <li style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}><Check size={18} color="var(--primary)" /> Delivered to Desk</li>
                        <li style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}><Check size={18} color="var(--primary)" /> Morning Guarantee (8 AM)</li>
                        <li style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}><Check size={18} color="var(--primary)" /> Free Delivery</li>
                    </ul>
                    <button className={`btn ${selectedPlan === 'office' ? 'btn-primary' : ''}`} style={{ width: '100%', border: selectedPlan !== 'office' ? '1px solid var(--border-color)' : 'none' }}>Select Plan</button>
                </div>

                {/* Plan 2: Home Essentials */}
                <div
                    className="card"
                    style={{
                        border: selectedPlan === 'daily' ? '2px solid var(--primary)' : '1px solid var(--border-color)',
                        cursor: 'pointer'
                    }}
                    onClick={() => setSelectedPlan('daily')}
                >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h3 style={{ margin: 0 }}>Home Essentials</h3>
                    </div>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>GH₵ 100 <span style={{ fontSize: '1rem', fontWeight: 'normal', color: 'var(--text-muted)' }}>/ week</span></p>
                    <p style={{ marginBottom: '1.5rem' }}>7 Bottles (Mon-Sun)</p>

                    <ul style={{ listStyle: 'none', marginBottom: '2rem' }}>
                        <li style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}><Check size={18} color="var(--primary)" /> Delivered to Doorstep</li>
                        <li style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}><Check size={18} color="var(--primary)" /> Early Drop (6 AM)</li>
                        <li style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}><Check size={18} color="var(--primary)" /> Family Size Options</li>
                    </ul>
                    <button className={`btn ${selectedPlan === 'daily' ? 'btn-primary' : ''}`} style={{ width: '100%', border: selectedPlan !== 'daily' ? '1px solid var(--border-color)' : 'none' }}>Select Plan</button>
                </div>

                {/* Plan 3: Daily Starter (New) */}
                <div
                    className="card"
                    style={{
                        border: selectedPlan === 'starter' ? '2px solid var(--primary)' : '1px solid var(--border-color)',
                        scale: selectedPlan === 'starter' ? '1.05' : '1',
                        cursor: 'pointer'
                    }}
                    onClick={() => setSelectedPlan('starter')}
                >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h3 style={{ margin: 0 }}>Daily Starter</h3>
                        <span style={{ background: '#fef3c7', color: '#92400e', padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.8rem', fontWeight: 'bold' }}>One-Off</span>
                    </div>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>GH₵ 10.00 <span style={{ fontSize: '1rem', fontWeight: 'normal', color: 'var(--text-muted)' }}>/ day</span></p>
                    <p style={{ marginBottom: '1.5rem' }}>1 Bottle (Any Flavor)</p>

                    <ul style={{ listStyle: 'none', marginBottom: '2rem' }}>
                        <li style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}><Check size={18} color="var(--primary)" /> Try Before You Commit</li>
                        <li style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}><Check size={18} color="var(--primary)" /> Standard Delivery</li>
                        <li style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}><Check size={18} color="var(--primary)" /> No Subscription</li>
                    </ul>
                    <button className={`btn ${selectedPlan === 'starter' ? 'btn-primary' : ''}`} style={{ width: '100%', border: selectedPlan !== 'starter' ? '1px solid var(--border-color)' : 'none' }}>Select Plan</button>
                </div>

            </div>

            <div className="card" style={{ maxWidth: '600px', margin: '0 auto', background: 'var(--bg-secondary)' }}>
                <h3 style={{ textAlign: 'center', marginBottom: '1rem' }}>Start Your Subscription</h3>
                <form style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }} onSubmit={(e) => e.preventDefault()}>
                    <input type="text" placeholder="Full Name" />
                    <input type="email" placeholder="Email Address" />
                    <input type="tel" placeholder="WhatsApp Number" />
                    <input type="text" placeholder="Delivery Address / Landmark" />

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
                        <div>
                            <span style={{ display: 'block', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Total to Pay</span>
                            <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>GH₵ {getPrice()}</span>
                        </div>
                        <button type="submit" className="btn btn-primary" style={{ padding: '0.75rem 2rem' }}>
                            Pay & Subscribe
                        </button>
                    </div>
                    <p style={{ fontSize: '0.8rem', textAlign: 'center', marginTop: '0.5rem' }}>Secured by Paystack</p>
                </form>
            </div>
        </div>
    );
}
