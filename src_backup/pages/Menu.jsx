import React from 'react';
import { ShoppingBag } from 'lucide-react';

export default function Menu() {
    const products = [
        { title: 'Daily Core', description: 'Pineapple + Ginger', price: 15, tag: 'Vitality' },
        { title: 'Green Habit', description: 'Spinach + Apple + Cucumber', price: 18, tag: 'Detox' },
        { title: 'Recovery', description: 'Carrot + Orange + Lime', price: 20, tag: 'Immunity' },
    ];

    const functional = [
        { title: 'Blood Sugar Balance', description: 'Bitter Leaf + Cucumber + Apple', price: 25, tag: 'Health' },
        { title: 'Office Focus', description: 'Pineapple + Turmeric + Ginger', price: 22, tag: 'Energy' },
    ];

    return (
        <div className="container" style={{ paddingTop: '6rem', paddingBottom: '4rem' }}>
            <h1 style={{ textAlign: 'center', marginBottom: '1rem' }}>Our Menu</h1>
            <p style={{ textAlign: 'center', maxWidth: '600px', margin: '0 auto 3rem' }}>
                Freshly pressed at 4:30 AM every morning. No preservatives, no added sugar. Just raw vitality.
            </p>

            <h2 style={{ marginBottom: '1.5rem', borderBottom: '2px solid var(--primary-light)', paddingBottom: '0.5rem', display: 'inline-block' }}>Signature Lines</h2>
            <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginBottom: '4rem' }}>
                {products.map((p, i) => (
                    <div key={i} className="card">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                            <h3 style={{ fontSize: '1.25rem' }}>{p.title}</h3>
                            <span style={{ background: 'var(--bg-secondary)', padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.8rem', fontWeight: 'bold', color: 'var(--text-muted)' }}>{p.tag}</span>
                        </div>
                        <p style={{ marginBottom: '1.5rem' }}>{p.description}</p>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>GH₵ {p.price.toFixed(2)}</span>
                            <button className="btn btn-primary" style={{ padding: '0.5rem 1rem' }}>
                                <ShoppingBag size={18} style={{ marginRight: '0.5rem' }} /> Add
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <h2 style={{ marginBottom: '1.5rem', borderBottom: '2px solid var(--accent)', paddingBottom: '0.5rem', display: 'inline-block' }}>Functional Blends</h2>
            <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
                {functional.map((p, i) => (
                    <div key={i} className="card">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                            <h3 style={{ fontSize: '1.25rem' }}>{p.title}</h3>
                            <span style={{ background: '#fef3c7', padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.8rem', fontWeight: 'bold', color: '#92400e' }}>{p.tag}</span>
                        </div>
                        <p style={{ marginBottom: '1.5rem' }}>{p.description}</p>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>GH₵ {p.price.toFixed(2)}</span>
                            <button className="btn btn-primary" style={{ padding: '0.5rem 1rem' }}>
                                <ShoppingBag size={18} style={{ marginRight: '0.5rem' }} /> Add
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
